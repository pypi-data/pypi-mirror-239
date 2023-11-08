'''
Utility functions for the compression
'''
import os
import gc
import pathlib
import numpy as np
import pandas as pd
import h5py
import scanpy as sc


def store_approximation(
        fn_out,
        compressed_atlas,
        celltype_order,
        measurement_type='gene_expression',
        compression=22,
        quantisation="chromatin_accessibility",
        #chunked=True,
        ):
    '''Store compressed atlas into h5 file.

    Args:
        fn_out: The h5 file with the compressed atlas.
        compressed_atlas: The dict with the result.
        celltype_order: The order of cell types.
        measurement_type: What type of data this is (gene expression, chromatin accessibility, etc.).
        quantisation: If not None, average measurement is quantised with these bins.
        compression: Use zstd compression of the data arrays (avg and frac). Levels are 1-22,
            whereas 0 or False means no compression. No performace decrease is observed.
    '''
    add_kwargs = {}

    # Optional zstd compression using hdf5plugin
    if compression:
        try:
            import hdf5plugin
            # NOTE: decompressing zstd is equally fast no matter how much compression.
            # As for compression speed, levels 1-19 are normal, 20-22 "ultra".
            # A quick runtime test shows *faster* access for clevel=22 than clevel=3,
            # while the file size is around 10% smaller. Compression speed is significantly
            # slower, but (i) still somewhat faster than actually averaging the data and
            # (ii) compresses whole human RNA+ATAC is less than 1 minute. That's nothing
            # considering these approximations do not change that often.
            comp_kwargs = hdf5plugin.Zstd(clevel=compression)
        except ImportError:
            # TODO: throw some warning
            compression = False
            comp_kwargs = {}
    else:
        comp_kwargs = {}

    # Data can be quantised for further compression (typically ATAC-Seq)
    if (quantisation == True) or (quantisation == measurement_type):
        if measurement_type == "chromatin_accessibility":
            # NOTE: tried using quantiles for this, but they are really messy
            # and subject to aliasing effects. 8 bits are more than enough for
            # most biological questions given the noise in the data
            qbits = 8
            bins = np.array([-0.001, 1e-8] + np.logspace(-4, 0, 2**qbits - 1).tolist()[:-1] + [1.1])
            # bin "centers", aka data quantisation
        elif measurement_type == "gene_expression":
            # Counts per ten thousand quantisation
            qbits = 16
            bins = np.array([-0.001, 1e-8] + np.logspace(-2, 4, 2**qbits - 1).tolist()[:-1] + [1.1e4])
        else:
            raise ValueError(f"Quantisation for {measurement_type} not set.")

        quantisation_array = [0] + np.sqrt(bins[1:-2] * bins[2:-1]).tolist() + [1]

        qbytes = qbits // 8
        # Add a byte if the quantisation is not optimal
        if qbits not in (8, 16, 32, 64):
            qbytes += 1
        avg_dtype = f"u{qbytes}"
        quantisation = True
    else:
        avg_dtype = "f4"
        quantisation = False

    features = compressed_atlas['features'].tolist()

    with h5py.File(fn_out, 'a') as h5_data:
        # Version
        import scquill
        h5_data.attrs['scquill_version'] = scquill.__version__

        # Umbrella group for measurments (not metadata)
        me_all = h5_data.create_group('measurements')

        # Subgroup for a specific measurement type (multi-omics will have multiple)
        me = me_all.create_group(measurement_type)
    
        me.attrs['compression'] = compression

        me.create_dataset('features', data=np.array(features).astype('S'))
        if quantisation:
            me.create_dataset('quantisation', data=np.array(quantisation_array).astype('f4'))

        #for groupby in ['celltype', 'celltype_dataset_timepoint']:
        for groupby in ['celltype']:
            group = me.create_group(groupby)

            # Number of cells
            ncells = compressed_atlas[groupby]['ncells']
            group.create_dataset(
                'cell_count', data=ncells.values, dtype='i8')

            # Average in a cell type
            avg = compressed_atlas[groupby]['avg']
            if quantisation:
                # pd.cut wants one dimensional arrays so we ravel -> cut -> reshape
                avg_vals = (pd.cut(avg.values.ravel(), bins=bins, labels=False)
                            .reshape(avg.shape)
                            .astype(avg_dtype))
                avg = pd.DataFrame(
                    avg_vals, columns=avg.columns, index=avg.index,
                )

            # TODO: manual chunking might increase performance a bit, the data is
            # typically accessed only vertically (each feature its own island)
            #if chunked:
            #    # Chunk each feature on its own: this is perfect for ATAC-Seq 
            #    add_kwargs['chunks'] = (1, len(features))

            # Cell types
            group.create_dataset(
                'index', data=avg.columns.values.astype('S'))
            group.create_dataset(
                'average', data=avg.T.values, dtype=avg_dtype,
                **add_kwargs,
                **comp_kwargs,
            )
            if measurement_type == 'gene_expression':
                # Fraction detected in a cell type
                frac = compressed_atlas[groupby]['frac']
                group.create_dataset(
                    'fraction', data=frac.T.values, dtype='f4',
                    **add_kwargs,
                    **comp_kwargs,
                )

            # Local neighborhoods
            neid = compressed_atlas[groupby]['neighborhood']
            neigroup = group.create_group('neighborhood')
            ncells = neid['ncells']
            neigroup.create_dataset(
                'cell_count', data=ncells.values, dtype='i8')

            avg = neid['avg']
            if quantisation:
                # pd.cut wants one dimensional arrays so we ravel -> cut -> reshape
                avg_vals = (pd.cut(avg.values.ravel(), bins=bins, labels=False)
                            .reshape(avg.shape)
                            .astype(avg_dtype))
                avg = pd.DataFrame(
                    avg_vals, columns=avg.columns, index=avg.index,
                )
            neigroup.create_dataset(
                'index', data=avg.columns.values.astype('S'))
            neigroup.create_dataset(
                'average', data=avg.T.values, dtype=avg_dtype,
                **add_kwargs,
                **comp_kwargs,
            )
            if measurement_type == 'gene_expression':
                # Fraction detected in a cell type
                frac = neid['frac']
                neigroup.create_dataset(
                    'fraction', data=frac.T.values, dtype='f4',
                    **add_kwargs,
                    **comp_kwargs,
                )

            # Centroid coordinates
            coords_centroids = neid['coords_centroid']
            neigroup.create_dataset(
                'coords_centroid',
                data=coords_centroids.T.values, dtype=avg_dtype,
                **add_kwargs,
                **comp_kwargs,
            )

            # Convex hulls
            convex_hulls = neid['convex_hull']
            hullgroup = neigroup.create_group('convex_hull')
            for ih, hull in enumerate(convex_hulls):
                hullgroup.create_dataset(
                    str(ih), data=hull, dtype='f4',
                    **add_kwargs,
                    **comp_kwargs,
                )

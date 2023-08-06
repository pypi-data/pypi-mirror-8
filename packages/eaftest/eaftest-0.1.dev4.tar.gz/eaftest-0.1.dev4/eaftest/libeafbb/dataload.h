#pragma once

typedef unsigned int uint;

typedef struct _data_t {
    int nvars, nmasks, npoints;
    int **masks, **points;
} data_t;

data_t * load_data(char * points_file, char * masks_file);
int binarrays_to_uint_units(int cols);
uint* binarrays_to_uint(int **binarrays, int lines, int cols);
data_t * load_data_from_arrays(int * points, int * masks,
        int npoints, int nmasks, int columns);
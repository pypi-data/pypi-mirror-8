#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "algorithm.h"
#include "dataload.h"
#include "heuristic.h"

int DEBUG_LEVEL = 0;

/* Main vars */
node_t * tree;
data_t * data;
/* Vars for binarrays */
int units;
uint* darray;
uint* marray;


void init() {
    tree = make_tree(data);
    /* Bin arrays */
    units = binarrays_to_uint_units(data->nvars);
    darray = binarrays_to_uint(data->points, data->npoints, data->nvars);
    marray = binarrays_to_uint(data->masks, data->nmasks, data->nvars);
    if (DEBUG_LEVEL >= 1) {
        puts("# DEBUG: Init CPU Test");
        printf("- Data loaded: Nvars: %d, Nmasks: %d, Npoints: %d\n",
            data->nvars, data->nmasks, data->npoints);
        printf("- Memory: %d Bytes, %d KiBytes\n", tree_memory,
            tree_memory/1024);
        printf("- Total Nodes: %d\n", tree_nodes);
    }
}

void init_from_files(char * points_file, char * masks_file,
        int * nvars, int * nmasks, int * npoints) {
    data = load_data(points_file, masks_file);
    if (nvars)
        *nvars = data->nvars;
    if (nmasks)
        *nmasks = data->nmasks;
    if (npoints)
        *npoints = data->npoints;
    init();
}

void init_from_arrays(int * points, int * masks, 
        int nvars, int nmasks, int npoints) {
    data = load_data_from_arrays(points, masks, npoints, nmasks, nvars);
    init();
}

void set_debug_level(int level) {
    DEBUG_LEVEL = level;
}

int run_test_mask(int i) {
    int result, max, min, n = data->nvars;
    int heuristic = eaf_test_2_heur(darray, marray + units * i, 
                                data->npoints, n, units, 650, NULL);
    test_mask(tree, data->masks[i], n, &max, &min, heuristic);
    result = MAX(max-n/2, -min+n/2);

    if (DEBUG_LEVEL == 1) {
        putchar('.');
        fflush(stdout);
    }
    else if (DEBUG_LEVEL >= 2) {
        printf("[heur:%d] ", heuristic);
        printf("%4d:  %2d  (%2d/%2d)\t", i, result, max-n/2, -min+n/2);
        printf("(Calls: %9d, %7d)\n", calls_y, calls_xy);
        fflush(stdout);
    }

    return result;
}


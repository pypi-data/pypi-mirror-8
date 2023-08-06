#pragma once

void init_from_files(char * points_file, char * masks_file,
        int * nvars, int * nmasks, int * npoints);
void init_from_arrays(int * points, int * masks,
        int nvars, int nmasks, int npoints);
void set_debug_level(int level);
int run_test_mask(int i);

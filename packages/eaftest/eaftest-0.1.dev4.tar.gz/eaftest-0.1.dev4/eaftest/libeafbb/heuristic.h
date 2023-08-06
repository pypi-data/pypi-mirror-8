#pragma once

int eaf_test_1(uint *array, uint *mask, int npoints, int nvars, int units);
int eaf_test_2(uint *array, uint *mask, int npoints, int nvars, int units);
void sort_popcnt_xor(uint *array, uint *mask, int npoints, int units);
int eaf_test_2_heur(uint *array, uint *mask, int npoints, int nvars, int units,
                    int npoints_heur, uint *order);

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "dataload.h"
#include <assert.h>

#define popcount __builtin_popcount


/* ---------------- SORT ---------------- */
static uint *gmask;
static int gunits;
static int gnvars;

inline int keyfunc(const uint * point) {
    int sum = 0, i;
    for (i = 0; i < gunits; i++)
        sum += popcount(point[i] ^ gmask[i]);
    sum = abs(sum - gnvars/2);
    return sum;
}

int cmpfunc(const void *a, const void *b) {
   const uint *da = a, *db = b;
   int comp = keyfunc(da) - keyfunc(db);
   return -comp;        /* descending */
   /*return comp;*/       /* ascending */
}

void sort_popcnt_xor(uint *array, uint *mask, int npoints, int units) {
    gmask = mask;
    gunits = units;
    qsort(array, npoints, sizeof(uint)*units, cmpfunc);
}

/* ------------------------------------------------*/

/* Collect */

int collect_popcnt_xor(uint *array, uint *mask, int npoints, int nvars,
                       int units, uint *aux, uint *order) {
    int i;
    int bins = nvars / 2 + 1;
    int * count = calloc(bins, sizeof(int));
    int * counti = calloc(bins, sizeof(int));
    int * pc = malloc(npoints * sizeof(int));
    
    for (i = 0; i < npoints; i++) {
        int d = 0, u;
        for (u = 0; u < units; u++)
            d += popcount(array[i * units + u] ^ mask[u]);
        d = abs(d - nvars/2);
        
        pc[i] = d;
        count[d]++;
    }
    
    /* Cummulative sum */
    for (i = bins-1; i > 0; i--)
        count[i-1] += count[i];
    for (i = 0; i < bins-1; i++)
        counti[i] = count[i+1];
    
    /* Fill the bins */
    for (i = 0; i < npoints; i++) {
        int d = pc[i], u;
        /* Copy point */
        if (order)
            order[counti[d]] = i;
        for (u = 0; u < units; u++)
            aux[counti[d] * units + u] = array[i * units + u];
        counti[d]++;
    }

    for (i = 0; i < bins; i++)
        assert(counti[i] == count[i]);  /* Bins filled test */

    free(count);
    free(counti);
    free(pc);
    return 0;
}

/* ------- */

int eaf_test_1(uint *array, uint *mask, int npoints, int nvars, int units) {
    int i, u, maxd = 0;
    for (i = 0; i < npoints; i++) {
        int d = 0;
        for (u = 0; u < units; u++)
            d += popcount(array[i * units + u] ^ mask[u]);
        d = abs(d - nvars/2);
        if (maxd < d) {
            /* printf("max1: %d %d\n", i, d); */
            maxd = d;
        }
    }
    return maxd;
}

int eaf_test_2(uint *array, uint *mask, int npoints, int nvars, int units) {
    int i, j, u, maxd = 0;
    for (i = 0; i < npoints; i++) {
        for (j = 0; j <= i && j < npoints; j++) {
            int d = 0;
            for (u = 0; u < units; u++) {
                uint data = array[i * units + u] & array[j * units + u];
                d += popcount(data ^ mask[u]);
            }
            d = abs(d - nvars/2);
            if (maxd < d) {
                maxd = d;
                /* printf("max2: %d,%d: %d\n", i, j, d); */
            }
        }
    }
    return maxd;
}

int eaf_test_2_heur(uint *array, uint *mask, int npoints, int nvars, int units,
                    int npoints_heur, uint *order) {
    int maxd2;
    uint *collectaux = malloc(npoints * units * sizeof(uint));
    collect_popcnt_xor(array, mask, npoints, nvars, units, collectaux, order);
    maxd2 = eaf_test_2(collectaux, mask, npoints_heur, nvars, units);
    free(collectaux);
    return maxd2;
}

int main_s() {
    data_t* data = load_data("data/local2-25-b.AB.u", "data/rmasks50.txt");
    /* Make uint bit arrays */
    int units = binarrays_to_uint_units(data->nvars);
    uint* darray = binarrays_to_uint(data->points, data->npoints, data->nvars);
    uint* marray = binarrays_to_uint(data->masks, data->nmasks, data->nvars);
    int m, maxd1 = 0, maxd2 = 0;
    uint* order = malloc(sizeof(uint) * data->npoints);
    
    gnvars = data->nvars;
    
    for (m = 0; m < 20; m++) {
        /*sort_popcnt_xor(darray, marray + units * m, data->npoints, units);*/
        
        /*maxd1 = eaf_test_1(darray, marray + units * m,
                              data->npoints, data->nvars, units);*/
        
        maxd2 = eaf_test_2_heur(darray, marray + units * m,
                              data->npoints, data->nvars, units, 1024, order);
        printf("- mask %d: %d %d\n", m, maxd1, maxd2);
        printf("order %d\n", order[0]);
        
    }
    return 0;
}

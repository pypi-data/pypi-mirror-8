#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "dataload.h"

int get_matrix_cols(char * filename) {
    FILE * file;
    char * line = NULL;
    int ret, _, read, offset, nums;
    size_t len;
    
    file = fopen(filename, "r");
    assert(file);
    
    ret = getline(&line, &len, file);
    assert(ret > 0);
    
    for (offset = nums = 0;
        sscanf(line + offset, "%d%n", &_, &read) > 0;
        offset += read, nums++);
    
    free(line);
    fclose(file);
    return nums;
}

int * load_line(FILE* file, int n) {
    int * array = malloc(n * sizeof(int));
    int j;
    for (j = 0; j < n; j++) {
        if (fscanf(file, "%d,", array + j) < 1) {
            free(array);
            return NULL;
        }
    }
    return array;
}

int ** load_matrix_from_file(char * filename, int * lines, int * columns) {
    int ** matrix = NULL, _;
    FILE * file = fopen(filename, "r");
    
    *columns = get_matrix_cols(filename);
    
    for (*lines = 0 ; ; ) {
        int * array = load_line(file, *columns);
        if (!array)
            break;
        /* TODO: isto é lento! */
        matrix = realloc(matrix, ++*lines * sizeof(int *));
        matrix[*lines-1] = array;
    }
    assert(fscanf(file, "%d,", &_) == EOF);
    fclose(file);
    
    return matrix;
}

int ** load_matrix_from_int_array(int * array, int lines, int columns) {
    int i, j, ** matrix = calloc(lines, sizeof(int*));

    for (i = 0; i < lines; i++) {
        matrix[i] = malloc(columns * sizeof(int));
        for (j = 0; j < columns; j++)
            matrix[i][j] = array[i * columns + j];
    }

    return matrix;
}

data_t * load_data(char * points_file, char * masks_file) {
    data_t * d = calloc(1, sizeof(data_t));
    int cols;
    
    d->masks = load_matrix_from_file(masks_file, &d->nmasks, &d->nvars);
    d->points = load_matrix_from_file(points_file, &d->npoints, &cols);
    
    /* TODO: data validation (ie: correct masks... 1 and 0) */
    assert(d->nvars == cols);
    
    return d;
}

data_t * load_data_from_arrays(int * points, int * masks,
        int npoints, int nmasks, int columns) {
    data_t * d = calloc(1, sizeof(data_t));

    d->points = load_matrix_from_int_array(points, npoints, columns);
    d->masks = load_matrix_from_int_array(masks, nmasks, columns);
    d->npoints = npoints;
    d->nmasks = nmasks;
    d->nvars = columns;

    return d;
}

uint* binarrays_to_uint(int **binarrays, int lines, int cols) {
    const int bits = sizeof(uint) * 8;
    const int units = (cols-1)/bits + 1;
    
    uint *array = calloc(lines * units, sizeof(uint));
    
    int i, b;
    for (i = 0; i < lines; i++)
        for (b = 0; b < cols; b++)
            if (binarrays[i][b])
                array[i*units + b/bits] |= 1 << b;
    
    return array;
}

int binarrays_to_uint_units(int cols) {
    const int bits = sizeof(uint)*8;
    return (cols-1)/bits + 1;
}


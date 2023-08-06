#pragma once

#include "dataload.h"

#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

typedef struct _node_t {
    struct _node_t * ns[2];
    short maxsim, maxdif;
} node_t;

extern int tree_memory;
extern int tree_nodes;
extern int calls_y;
extern int calls_xy;

node_t * make_tree(data_t * data);
void test_mask(node_t * tree, int * m, int n, int * max, int * min, int heur);

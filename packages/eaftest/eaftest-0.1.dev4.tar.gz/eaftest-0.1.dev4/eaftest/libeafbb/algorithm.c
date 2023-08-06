#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#include "algorithm.h"
#include "dataload.h"
#include "heuristic.h"


/* ---- Tree management ---- */

int tree_memory = 0;
int tree_nodes = 0;

node_t * new_node() {
    tree_memory += sizeof(node_t);
    tree_nodes++;
    return calloc(1, sizeof(node_t));
}

node_t * get_node(node_t * node, int index) {
    if (!node->ns[index])
        node->ns[index] = new_node();
    return node->ns[index];
}

void insert_bitarray(node_t * tree, const int array[], int n) {
    node_t * node = tree;
    int i;
    for (i = 0; i < n; i++) {
        assert(array[i] == 0 || array[i] == 1);
        node = get_node(node, array[i]);
    }
}

node_t * make_tree(data_t * data) {
    node_t * tree = new_node();
    int i;
    for (i = 0; i < data->npoints; i++)
        insert_bitarray(tree, data->points[i], data->nvars);
    return tree;
}


/* ---- Algorithm ---- */

const int * mask;       /* current mask */
int * xarr;             /* current x-array */
int bestmax, bestmin;         /* best max, best min */
int calls_y, calls_xy;  /* number of function calls */

void search_y(const node_t * node, int n, int i, int max, int min, int path) {
    int bit;
    
    calls_y++;
    
    /* The achievable limits are worse than current best ones */
    if ((min >= bestmin || max - node->maxsim >= bestmin) &&
        (max <= bestmax || min + node->maxdif <= bestmax))
        return;
    
    if (i == n) {
        bestmax = max > bestmax ? max : bestmax;
        bestmin = min < bestmin ? min : bestmin;
        /* Sync bestmin <=> bestmax */
        if (bestmin > n - bestmax)
            bestmin = n - bestmax;
        if (bestmax < n - bestmin)
            bestmax = n - bestmin;
        return;
    }

    for (bit = 0; bit <= 1; bit++) {
        if (node->ns[bit]) {
            int newpath = path;
            
            /* Only need to search for half of the total combinations */
            if (path == 0 && bit < xarr[i])
                continue;
            if (path == 0 && bit > xarr[i])
                newpath = 1;
            
            
            if (xarr[i] && bit == mask[i])
                search_y(node->ns[bit], n, i+1, max-1, min, newpath);
            else if (xarr[i])
                search_y(node->ns[bit], n, i+1, max, min+1, newpath);
            else
                search_y(node->ns[bit], n, i+1, max, min, newpath);
        }
    }
    
}


void search_xy(node_t * tree, node_t * node, int n, int i, int max, int min) {
    int bit;
    
    calls_xy++;
    
    /* If the limits are already worse than current best ones */
    if (min >= bestmin && max <= bestmax)
        return;
    
    if (i == n) {
        search_y(tree, n, 0, max, min, 0);
        return;
    }
    
    for (bit = 1; bit >= 0; bit--) {
        if (node->ns[bit]) {
            xarr[i] = bit;
            if (bit == 0 && mask[i] == 0)
                search_xy(tree, node->ns[bit], n, i+1, max-1, min);
            else if (bit == 0)
                search_xy(tree, node->ns[bit], n, i+1, max, min+1);
            else
                search_xy(tree, node->ns[bit], n, i+1, max, min);
        }
    }
    
}

void calculate_future_limits(node_t * node, int n, int i) {
    int bit, maxsim = 0, maxdif = 0;
    int newsim, newdif;
    
    if (n == i) {
        node->maxsim = node->maxdif = 0;
        return;
    }
    
    for (bit = 0; bit <= 1; bit++) {
        if (node->ns[bit]) {
            calculate_future_limits(node->ns[bit], n, i+1);
            
            newsim = node->ns[bit]->maxsim + (bit == mask[i]);
            newdif = node->ns[bit]->maxdif + (bit != mask[i]);
            
            if (newsim > maxsim)
                maxsim = newsim;
            if (newdif > maxdif)
                maxdif = newdif;
        }

    }
    node->maxsim = maxsim;
    node->maxdif = maxdif;
}

void test_mask(node_t * tree, int * m, int n, int * max, int * min, int heur) {
    int bmax = n, bmin = 0;
    
    /* Set-up global vars */
    bestmin = bestmax = n / 2;
    xarr = calloc(n, sizeof(int));
    mask = m;
    calls_y = calls_xy = 0;
    
    /* Heuristic */
    bestmin -= heur;
    bestmax += heur;
    
    calculate_future_limits(tree, n, 0);
    search_xy(tree, tree, n, 0, bmax, bmin);
    
    free(xarr);
    
    /* Return best limits */
    *max = bestmax;
    *min = bestmin;
}

/*
void set_order(node_t * node, int * array, int n, int i) {
    int bit;
    
    if (i == n)
        return;
    
    bit = array[i];
    node->order = bit;
    set_order(node->ns[bit], array, n, i+1);
}
*/



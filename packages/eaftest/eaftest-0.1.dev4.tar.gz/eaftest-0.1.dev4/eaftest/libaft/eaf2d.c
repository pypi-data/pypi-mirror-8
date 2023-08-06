/*************************************************************************

 eaf2d: Compute the empirical attainment function from a sequence of
        non-dominated point sets (two-objective case)

 ---------------------------------------------------------------------

    Copyright (c) 2005
            Carlos M. Fonseca <cmfonsec@ualg.pt>
    Copyright (c) 2010-2011
            Carlos M. Fonseca <cmfonsec@dei.uc.pt>
            Andreia Guerreiro <andreia.guerreiro@ist.utl.pt>
    Copyright (c) 2013
            Humberto Alves    <hjalves@student.dei.uc.pt>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, you can obtain a copy of the GNU
 General Public License at:
                 http://www.gnu.org/copyleft/gpl.html
 or by writing to:
           Free Software Foundation, Inc., 59 Temple Place,
                 Suite 330, Boston, MA 02111-1307 USA

 ----------------------------------------------------------------------

*************************************************************************/

#define NOBJ 2
#include <stdlib.h>
#include <math.h>
#include <string.h>

// attainment level data
typedef struct leveldata {
    int nlevels;   // levels
    int *len;      // number of points per level
    double **p;    // points
    char **ind;    // indicators
} leveldata;


static int compare_x_desc(const void *p1, const void *p2)
{
    double x1=**(double **)p1;
    double x2=**(double **)p2;
    
    if (x1 != x2)
        return (x1 > x2) ? -1 : 1;
    else
        return 0;
}

static int compare_y_asc(const void *p1, const void *p2)
{
    double y1 = *(*(double **)p1+1);
    double y2 = *(*(double **)p2+1);
    
    if (y1 != y2)
        return (y1 < y2) ? -1 : 1;
    else
        return 0;
}

/* 
 * eaf2d - Compute attainment surfaces from points in objective space,
 *    using dimension sweeping
 *
 * Input arguments:
 *    data -    a pointer to the data matrix, stored as a linear array of double
 *        in row major order
 *    cumsize - an array containing the cumulative number of rows in each non-dominated
 *         front (must be non-decreasing)
 *    nruns -    the number of independent non-dominated fronts
 *    attlevel - an array containing the attainment levels to compute.
 *    nlevel - number of attainment levels to compute
 * 
 * Returns NULL if an error occurs or the attainment levels points and indicators
 */

leveldata* eaf2d(double *data, int *cumsize, int nruns,
                 int *attlevel, int nlevels, int indicators)
{
    double **ix, **iy;  /* used to access the data sorted according to x or y */
    int gx, gy;         /* running indices for ix and iy */
    int ntotal;         /* total number of points in data */
    int run, *runtab, tee, t;
    int i, j;           /* iteration counters */
    int *attained, level, *save_attained;
    int totalp = 0;
    int llen, ilen;
    
    for (i = 1; i < nruns; i++)
        if (cumsize[i] <= cumsize[i-1])
            return NULL;
    ntotal = cumsize[nruns-1];
    
    /* Allocation of attainment levels data */
    leveldata *lvdata = calloc(1, sizeof(leveldata));
    lvdata->nlevels = nlevels;
    lvdata->len = calloc(nlevels, sizeof(int));
    lvdata->p = calloc(nlevels, sizeof(double*));
    if (indicators)
        lvdata->ind = calloc(nlevels, sizeof(char*));
    /* -------------------------------- */
    
    /* Access to the data is made via two arrays of pointers: ix, iy
     * These are sorted, to allow for dimension sweeping */
    
    ix = malloc((ntotal + 1) * sizeof(double*)); //p
    iy = malloc(ntotal * sizeof(double*)); //q

    double p[2] = {INFINITY, -INFINITY};
    ix[0] = p;
    
    for (i = 0, j = 1; i < ntotal ; i++, j++)
        ix[j] = iy[i] = data + 2*i;

    qsort(ix+1, ntotal, sizeof *ix, &compare_x_desc);
    qsort(iy, ntotal, sizeof *iy, &compare_y_asc);

    /* Setup a lookup table to go from a point to the front to which it belongs */
    runtab = malloc(ntotal * sizeof(int)); //input_set
    for (i = 0, j = 0; i < ntotal; i++) {
        if (i == cumsize[j])
            j++;
        runtab[i] = j;
    }

    /* Setup tables to keep attainment statistics
     * save_attained is needed to cope with repeated values on the same axis */
    attained = malloc(nruns * sizeof(int));
    save_attained = malloc(nruns * sizeof(int));
    
    for (t = 0; t < nlevels; t++) {
        tee = attlevel[t];
        gx = 0;
        gy = -1;
        level = 0;
        for (i = 0; i < nruns; attained[i++] = 0);
        
        while (gx < ntotal && gy < ntotal-1) {
            do {
                gy++;
                if (iy[gy][0] < ix[gx][0]) {
                    run = runtab[(iy[gy]-data)/NOBJ];
                    if (attained[run]++ == 0)
                        level++;
                }
            } while (gy < ntotal-1 && (level < tee || iy[gy][1] == iy[gy+1][1]));

            if (level >= tee) {
                do {
                    gx++;
                    if (indicators && ix[gx][0] != ix[gx-1][0])
                        memcpy(save_attained, attained, nruns * (sizeof *attained));
                    if (ix[gx][1] <= iy[gy][1]) {
                        run = runtab[(ix[gx]-data)/NOBJ];
                        if(--attained[run] == 0)
                            level--;
                    }
                } while (level >= tee || (gx < ntotal && ix[gx][0] == ix[gx+1][0]));
                
                llen = 2*lvdata->len[t];
                lvdata->p[t] = realloc(lvdata->p[t], sizeof(double)*(llen+2));
                lvdata->p[t][llen] = ix[gx][0];
                lvdata->p[t][llen+1] = iy[gy][1];
                // Save attainment indicators values 
                if (indicators) {
                    ilen = nruns*lvdata->len[t];
                    lvdata->ind[t] = realloc(lvdata->ind[t], ilen+nruns);
                    for (i = 0; i < nruns; i++)
                        lvdata->ind[t][ilen+i] = save_attained[i]!=0;
                }
                lvdata->len[t]++;
                totalp++;
            }
        }
    }
    free(save_attained);
    free(attained);
    free(runtab);
    free(iy);
    free(ix);
    return lvdata;
}

void free_lvdata(leveldata *ld)
{
    int i;
    // Free indicators
    if (ld->ind) {
        for (i = 0; i < ld->nlevels; i++)
            free(ld->ind[i]);
        free(ld->ind);
    }
    if (ld->p) {
        for (i = 0; i < ld->nlevels; i++)
            free(ld->p[i]);
        free(ld->p);
    }
    free(ld->len);
    free(ld);
}

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "eafbb.h"

int main(int argc, char * argv[]) {
    int i, from = 0, to = -1;
    char * points_file, * masks_file;
    int * results, * tail;    
    int nvars, nmasks, npoints;

    set_debug_level(2);

    if (argc < 3) {
        puts("Usage: ./eafbb <points_file> <masks_file> [start_mask] [stop_mask]");
        return 1;
    }
    
    points_file = argv[1];
    masks_file = argv[2];
    if (argc == 4)
        to = atoi(argv[3]);
    if (argc >= 5) {
        from = atoi(argv[3]);
        to = atoi(argv[4]);
    }
    
    puts("Loading data...");
    init_from_files(points_file, masks_file, &nvars, &nmasks, &npoints);

    /* Structures for results */
    results = calloc(nmasks, sizeof(int));
    tail = calloc(nvars/2+1, sizeof(int));

    /* Correct 'to' */
    if (to == -1 || to > nmasks)
        to = nmasks;
    
    printf("Will test the masks: %d..%d\n\n", from, to);

    /* test masks */
    for (i = from; i < nmasks && i < to; i++) {
        results[i] = run_test_mask(i);
        tail[results[i]]++;
    }
    
    printf("\n=== Results ===\n");
    for (i = from; i < to; i++)
        printf("%d ", results[i]);
    
    printf("\n\n=== Tail ===\n");
    for (i = 0; i < nvars/2+1; i++)
        printf("%d ", tail[i]);
    puts("");
    
    return 0;
}

int main_old() {
    int points[] = {1, 0, 1, 0, 1, 1,
                    1, 0, 1, 0, 0, 1,
                    0, 1, 0, 1, 1, 0,
                    1, 1, 1, 1, 1, 1};
    int masks[] = {1, 0, 1, 1, 0, 0,
                   0, 0, 0, 1, 1, 1,
                   1, 1, 1, 0, 0, 0};

    set_debug_level(2);
    init_from_arrays(points, masks, 6, 3, 4);
    return 0;
}
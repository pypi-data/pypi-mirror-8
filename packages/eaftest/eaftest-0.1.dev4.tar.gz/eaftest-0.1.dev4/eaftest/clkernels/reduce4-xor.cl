
kernel void eaf_test2(
    global const uint *data,
    global const uint *mask,
    global int *dist,
    const uint pstart)
{
    local int m[PBLOCK];
    const int ii = get_global_id(0) % TDIVS;
    const int jj = get_global_id(0) / TDIVS;

    int D[PBLOCK] = {0};
    
    mask = mask + 2 * pstart;
    //dist = dist + pstart;
    
    for (int i = ii; i < NPOINTS; i += TDIVS) {
        for (int j = jj*TBLOCK; j < (jj+1)*(TBLOCK) && j <= i; j++) {
            uint x1 = data[i*2 + 0] & data[j*2 + 0];
            uint x2 = data[i*2 + 1] & data[j*2 + 1];
            for (int z = 0; z < PBLOCK; z++) {
                int d = abs_diff(popcount(mask[2*z] ^ x1) + 
                                 popcount(mask[2*z+1] ^ x2), (uint) MASKLEN);
                D[z] = max(D[z], d);
            }
        }
    }
    
    if (get_local_id(0) == 0)
        for (int i = 0; i < PBLOCK; i++)
            m[i] = 0;
    barrier(CLK_LOCAL_MEM_FENCE);
    
    for (int i = 0; i < PBLOCK; i++) {
        atomic_max(m + i, D[i]);
    }
    
    barrier(CLK_LOCAL_MEM_FENCE);
    if (get_local_id(0) == 0)
        for (int i = 0; i < PBLOCK; i++)
            atomic_max(dist + i, m[i]);
}

kernel void zerodist(global int* dist) {
      dist[get_global_id(0)] = 0;
}

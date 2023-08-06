
kernel void eaf_test2(
    global const uint *data,
    global const uint *mask,
    global int *dist,
    const int pstart,
    const int istart)
{
    local uint xx[TBLOCK*2];
 
    int gid = get_global_id(0);
    int j = get_global_id(1);
    int maskpos = pstart + gid;
    
    if (j > istart*TBLOCK)
        return;
    
    int D[PBLOCK] = {0};
    int d;
    const global uint *p = mask + (maskpos*PBLOCK*2);
    const int lid = get_local_id(0);
    const int i = istart*TBLOCK + lid;
    
    xx[lid*2] = i < NPOINTS ? data[i*2] & data[j*2]: 0;
    xx[lid*2+1] = i < NPOINTS ? data[i*2+1] & data[j*2+1]: 0;
    
    barrier(CLK_LOCAL_MEM_FENCE);
    
    for (int i = 0; i < TBLOCK; i++) {
        for (int z = 0; z < PBLOCK; z++) {
            d = abs_diff(popcount(p[2*z] ^ xx[i*2]) + 
                         popcount(p[2*z+1] ^ xx[i*2+1]), (uint) MASKLEN);
            D[z] = max(D[z], d);
        }
    }
    
    for (int i = 0; i < PBLOCK; i++) {
        atomic_max(dist + (gid*PBLOCK + i), D[i]);
    }
}


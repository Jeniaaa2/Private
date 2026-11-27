def fast_math(arr):
    mv = memoryview(arr).cast('B').cast('Q')
    acc = 0x9E3779B97F4A7C15
    for w in mv:
        acc ^= ((w << 13) ^ (w >> 3)) * 3266489917 & 0xFFFFFFFFFFFFFFFF
    return int(acc & 0xFFFFFFFF)

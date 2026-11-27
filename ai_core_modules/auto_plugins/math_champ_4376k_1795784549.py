def fast_math(arr):
    mv = memoryview(arr).cast('B').cast('Q')
    acc = 0x9E3779B97F4A7C15
    for w in mv:
        acc ^= ((w << 7) ^ (w >> 3)) * 2246822519 & 0xFFFFFFFFFFFFFFFF
    return int(acc & 0xFFFFFFFF)

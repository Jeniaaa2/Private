import os, time, ctypes, random, subprocess, tempfile

def forge_and_bench(gen_num=56):
    s1, s2 = random.choice((13, 17, 21)), random.choice((7, 11, 15))
    m1 = random.choice(["0x9e3779b97f4a7c15ULL", "0xbf58476d1ce4e5b9ULL", "0x94d049bb133111ebULL"])
    iters = 50000000
    c_src = f"""#include <stdint.h>
uint64_t fast_kernel(uint64_t seed, uint64_t n) {{
    uint64_t x = seed;
    for (uint64_t i = 0; i < n; i++) {{ x ^= (x << {s1}) + i; x *= {m1}; x ^= (x >> {s2}); }}
    return x;
}}"""
    so_path = os.path.join(tempfile.gettempdir(), f"c_kernel_g{gen_num}.so")
    c_path = so_path + ".c"
    try:
        open(c_path, "w").write(c_src)
        comp = subprocess.run(["gcc", "-O3", "-shared", "-fPIC", c_path, "-o", so_path], capture_output=True, text=True)
        if comp.returncode != 0:
            return " | ⚙️ C-Forge: gcc нет, активен Python-SIMD"
        lib = ctypes.CDLL(so_path)
        lib.fast_kernel.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
        lib.fast_kernel.restype = ctypes.c_uint64
        t0 = time.perf_counter()
        res = lib.fast_kernel(0x123456789ABCDEF0, iters)
        dt = max(time.perf_counter() - t0, 1e-6)
        ops = int((iters * 4) / dt)
        return f" | ⚙️ C-Forge (-O3): {ops:,} ops/s (h={hex(res)[:10]})"
    except Exception as e:
        return f" | ⚙️ C-Forge резерв: {str(e)[:35]}"
    finally:
        for p in (c_path, so_path):
            if os.path.exists(p):
                try: os.remove(p)
                except Exception: pass

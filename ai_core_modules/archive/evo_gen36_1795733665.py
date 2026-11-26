# Evolved Gen #36 (Attempt #1): Оптимизированная шахматная графовая компрессия
import time, random
random.seed(47301)
t0 = time.perf_counter()
board = random.getrandbits(64)
not_a, not_h = 0xfefefefefefefefe, 0x7f7f7f7f7f7f7f7f
attacks = ((board & not_h) << 1) | ((board & not_a) >> 1) | (board << 8) | (board >> 8)
attacks &= 0xffffffffffffffff
dt = round((time.perf_counter() - t0) * 1e6, 2)
print(f'Bitboard 64-bit [Оптимизированная шахматная графовая компрессия]: фигур={board.bit_count()}, битых_полей={attacks.bit_count()}, время={dt} мкс')

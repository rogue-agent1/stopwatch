import time
from stopwatch import Stopwatch, Timer, RateLimiter
sw = Stopwatch()
assert not sw.is_running
sw.start()
assert sw.is_running
time.sleep(0.05)
e = sw.elapsed()
assert e > 0.01
sw.stop()
e2 = sw.elapsed()
assert not sw.is_running
assert abs(e2 - sw.elapsed()) < 0.001  # stopped, so stable
sw.start(); time.sleep(0.01)
lap = sw.lap()
assert lap > 0
sw.reset()
assert sw.elapsed() == 0
t = Timer(0.05).start()
assert not t.is_expired()
assert t.remaining() > 0
time.sleep(0.06)
assert t.is_expired()
rl = RateLimiter(3, 1.0)
assert rl.allow() and rl.allow() and rl.allow()
assert not rl.allow()
print("stopwatch tests passed")

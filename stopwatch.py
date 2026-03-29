#!/usr/bin/env python3
"""Stopwatch and timer utilities. Zero dependencies."""
import time

class Stopwatch:
    def __init__(self):
        self._start = None; self._elapsed = 0; self._running = False; self._laps = []

    def start(self):
        if not self._running:
            self._start = time.monotonic(); self._running = True
        return self

    def stop(self):
        if self._running:
            self._elapsed += time.monotonic() - self._start
            self._running = False
        return self

    def reset(self):
        self._start = None; self._elapsed = 0; self._running = False; self._laps = []
        return self

    def lap(self):
        elapsed = self.elapsed()
        prev = self._laps[-1] if self._laps else 0
        self._laps.append(elapsed)
        return elapsed - prev

    def elapsed(self):
        if self._running: return self._elapsed + (time.monotonic() - self._start)
        return self._elapsed

    @property
    def laps(self): return self._laps[:]
    @property
    def is_running(self): return self._running

class Timer:
    def __init__(self, duration):
        self.duration = duration; self._start = None; self._running = False

    def start(self):
        self._start = time.monotonic(); self._running = True; return self

    def remaining(self):
        if not self._start: return self.duration
        elapsed = time.monotonic() - self._start
        return max(0, self.duration - elapsed)

    def is_expired(self):
        return self._start is not None and self.remaining() <= 0

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls; self.period = period; self._calls = []

    def allow(self):
        now = time.monotonic()
        self._calls = [t for t in self._calls if now - t < self.period]
        if len(self._calls) < self.max_calls:
            self._calls.append(now); return True
        return False

if __name__ == "__main__":
    sw = Stopwatch().start()
    time.sleep(0.1)
    print(f"Elapsed: {sw.elapsed():.3f}s")

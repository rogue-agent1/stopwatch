#!/usr/bin/env python3
"""stopwatch - Stopwatch with laps, splits, and statistics."""
import sys, time

class Stopwatch:
    def __init__(self):
        self._start = None
        self._elapsed = 0
        self._running = False
        self.laps = []
    def start(self):
        if not self._running:
            self._start = time.monotonic()
            self._running = True
    def stop(self):
        if self._running:
            self._elapsed += time.monotonic() - self._start
            self._running = False
    def lap(self):
        current = self.elapsed
        prev = sum(self.laps)
        self.laps.append(current - prev)
        return self.laps[-1]
    @property
    def elapsed(self):
        if self._running:
            return self._elapsed + (time.monotonic() - self._start)
        return self._elapsed
    def reset(self):
        self._start = None
        self._elapsed = 0
        self._running = False
        self.laps.clear()
    def stats(self):
        if not self.laps: return {}
        return {
            "count": len(self.laps),
            "total": sum(self.laps),
            "avg": sum(self.laps) / len(self.laps),
            "min": min(self.laps),
            "max": max(self.laps),
        }

def test():
    sw = Stopwatch()
    sw.start()
    time.sleep(0.02)
    l1 = sw.lap()
    time.sleep(0.02)
    l2 = sw.lap()
    sw.stop()
    assert sw.elapsed >= 0.03
    assert len(sw.laps) == 2
    assert l1 > 0 and l2 > 0
    s = sw.stats()
    assert s["count"] == 2
    assert abs(s["total"] - (l1 + l2)) < 1e-9
    sw.reset()
    assert sw.elapsed == 0
    assert len(sw.laps) == 0
    # Start/stop
    sw.start()
    time.sleep(0.01)
    sw.stop()
    e1 = sw.elapsed
    time.sleep(0.01)
    assert abs(sw.elapsed - e1) < 1e-6  # not running
    print("stopwatch: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: stopwatch.py --test")

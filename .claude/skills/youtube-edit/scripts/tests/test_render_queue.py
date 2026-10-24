"""render-queue.py: the second command waits for the first (they never overlap), the exit code passes through, a stale lock is cleared."""
import os, shutil, subprocess, sys, time, unittest
from .helpers import SCRIPTS, run, scratch

PY = sys.executable
# a command that records "start" and "end" with timestamps into a log file, holding for 1.2 s between them
STEP = "import sys,time; f=open(sys.argv[1],'a'); f.write('s%s %f\\n'%(sys.argv[2],time.time())); f.flush(); time.sleep(1.2); f.write('e%s %f\\n'%(sys.argv[2],time.time())); f.close()"


class RenderQueue(unittest.TestCase):
    def test_two_commands_never_overlap(self):
        d = scratch(self)
        lock, log = os.path.join(d, "q.lock"), os.path.join(d, "log.txt")
        q = [PY, os.path.join(SCRIPTS, "render-queue.py"), "--lock", lock, "--poll", "0.1", "--"]
        p1 = subprocess.Popen(q + [PY, "-c", STEP, log, "1"])
        time.sleep(0.4)
        p2 = subprocess.Popen(q + [PY, "-c", STEP, log, "2"])
        self.assertEqual((p1.wait(), p2.wait()), (0, 0))
        marks = {l.split()[0]: float(l.split()[1]) for l in open(log).read().splitlines()}
        self.assertGreaterEqual(marks["s2"], marks["e1"])             # the second started only after the first ended
        self.assertFalse(os.path.exists(lock))                         # the lock is released

    def test_exit_code_passes_through(self):
        d = scratch(self)
        r = run("render-queue.py", "--lock", os.path.join(d, "q.lock"), "--", PY, "-c", "import sys; sys.exit(7)")
        self.assertEqual(r.returncode, 7)

    def test_stale_lock_is_removed_and_waiting_gives_up(self):
        d = scratch(self)
        lock = os.path.join(d, "q.lock")
        open(lock, "w").write("999 crashed\n"); old = time.time() - 3600; os.utime(lock, (old, old))
        r = run("render-queue.py", "--lock", lock, "--stale-minutes", "30", "--", PY, "-c", "pass")
        self.assertEqual(r.returncode, 0, r.stderr)                    # the 1 h old lock was cleared
        open(lock, "w").write("1 busy\n")                              # a fresh lock, nobody will release it
        r = run("render-queue.py", "--lock", lock, "--wait-minutes", "0.02", "--poll", "0.2", "--", PY, "-c", "pass")
        self.assertEqual(r.returncode, 3)

    def test_finds_a_program_on_the_path_by_name(self):
        d = scratch(self)
        r = run("render-queue.py", "--lock", os.path.join(d, "q.lock"), "--", "ffmpeg" if shutil.which("ffmpeg") else "python", "-version")
        self.assertEqual(r.returncode, 0, r.stderr)                    # a bare name (npx.cmd on Windows) resolves like in a shell


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python

import subprocess
import time

if __name__ == "__main__":
    while True:
        proc = subprocess.Popen(["ping", "-c 1", "-W 0.01", "192.168.1.1"], stdout=subprocess.PIPE, universal_newlines=True)
        out, _ = proc.communicate()

        print out
        time.sleep(0.001)


#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime

def humanize_size(size):
    if size < 1024:
        return "{0:.3f}B".format(size)
    elif size < 1024 * 1024:
        return "{0:.3f}KiB".format(size / 1024)
    elif size < 1024 * 1024 * 1024:
        return "{0:.3f}MiB".format(size / (1024 * 1024))
    else:
        return "{0:.3f}GiB".format(size / (1024 * 1024 * 1024))


if __name__ == "__main__":

    file_path = sys.argv[1]
    ncpus = int(sys.argv[2])

    st = os.stat(file_path)

    size = st.st_size

    print("Input file size: {}".format(humanize_size(size)))

    size_per_cpu = int(size / ncpus)

    procs = []

    start_time = datetime.now()

    for i in range(ncpus):
        start = i * size_per_cpu
        end = start + size_per_cpu

        print("Process {} reading from {} to {}".format(i,start,end))

        cmd = [
            "dd", 
            "if={}".format(file_path), 
            "of=/dev/null",
            "bs=1M",
            "skip={}".format(start),
            "count={}".format(size_per_cpu),
            "iflag=nocache,skip_bytes,count_bytes",
        ]

        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procs.append(proc)

    for (i, proc) in enumerate(procs):
        proc.wait()
        print("Process {} done".format(i))
        print(proc.stderr.read().decode())

    duration = datetime.now() - start_time
    duration_secs = duration.total_seconds()

    size_gib = size / (1024 * 1024 * 1024)
    gbps = size_gib / duration_secs

    print("Total run-time {} seconds".format(duration_secs))
    print("{0:.2f} GiB/s".format(gbps))

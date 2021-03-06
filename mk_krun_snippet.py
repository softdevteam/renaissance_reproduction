#!/usr/bin/env python3
"""
Ideally this script wouldn't exist, and this logic would be right inside the
Krun config file itself. However, krun_ext_common.py is Python3 and Krun config
files are Python2. Mixing the two is asking for trouble, so we just use this
little script to generate a snippet the config file can include.
"""

import tempfile
import sys
import shutil
from krun_ext_common import (RENAISSANCE_BENCHMARKS, DACAPO_BENCHMARKS,
                             SPECJVM_BENCHMARKS, SKIP_RENAISANCE, SKIP_SPECJVM,
                             SKIP_DACAPO, JAVA_HEAP_GB)


def main(output_path):
    with tempfile.NamedTemporaryFile() as tmpf:
        tmpf.write("# This file is auto-generated by mk_krun_snippet.py\n\n"
                   .encode())

        tmpf.write(f"JAVA_HEAP_GB = {JAVA_HEAP_GB}\n\n".encode())

        tmpf.write("BENCHMARKS = {\n".encode())
        for suite in [RENAISSANCE_BENCHMARKS, DACAPO_BENCHMARKS,
                      SPECJVM_BENCHMARKS]:
            for bench in suite:
                # We don't utilise benchmark parameters in this experiment, so
                # they are all set to 0.
                tmpf.write(f"    '{bench}': 0,\n".encode())
        tmpf.write("}\n\n".encode())

        tmpf.write("SKIP = [\n".encode())
        for skip_dict in [SKIP_RENAISANCE, SKIP_DACAPO, SKIP_SPECJVM]:
            for vm, benchs in skip_dict.items():
                for bench in benchs:
                    tmpf.write(f"    '{bench}:{vm}:default-ext',\n".encode())
        tmpf.write("]\n".encode())

        tmpf.flush()
        shutil.copyfile(tmpf.name, output_path)


if __name__ == "__main__":
    try:
        output_path = sys.argv[1]
    except IndexError:
        print("usage: mk_krun_snippet.py <output-path>")
        sys.exit(1)

    main(output_path)

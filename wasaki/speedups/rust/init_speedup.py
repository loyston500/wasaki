# this will do some shit job to speed up wasaki internals

import os
import platform

platf = platform.system().lower()

if __name__ == "__main__":
    os.system("cargo build --release")
    if platf == "linux":
        os.system("cp target/release/libspeedups.so ../speedups.so")
else:
    print("Please run this module directly, ex: `python init_speedups.py`")

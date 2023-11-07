# Author: Luchang Jin 2023

import qlat as q
import sys

if len(sys.argv) < 2:
    q.displayln_info("Usage: fields-properly-truncate [--check-all] [--only-check] path1 path2 ...")
    exit()

q.begin_with_mpi()

args = sys.argv[1:]

is_check_all = False
is_only_check = False

while True:
    if args[0] == "--check-all":
        is_check_all = True
        args = args[1:]
    elif args[0] == "--only-check":
        is_only_check = True
        args = args[1:]
    else:
        break

for path in args:
    tags = q.properly_truncate_fields(
            path, is_check_all = is_check_all, is_only_check = is_only_check)
    for tag in tags:
        q.displayln_info(tag)

q.timer_display()

q.end_with_mpi()

exit()

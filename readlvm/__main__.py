import sys
import yaml
from . import LvmData

encoding = "utf-8"
cols = None
compress_col = None
src_filename = None

for arg in sys.argv[1:]:
    if arg.startswith("-e="):
        encoding = arg[len("-e=") :]
    elif arg.startswith("--encoding="):
        encoding = arg[len("--encoding=") :]

    elif arg.startswith("-c="):
        cols_str = arg[len("-c=") :].split(",")
        cols = list(map(lambda i: int(i) - 1, cols_str))
    elif arg.startswith("--columns="):
        cols_str = arg[len("-c=") :].split(",")
        cols = list(map(lambda i: int(i) - 1, cols_str))

    elif arg.startswith("--compress="):
        compress_col = int(arg[len("--compress=") :]) - 1

    elif src_filename == None:
        src_filename = arg

    else:
        sys.stderr.write(f"Unknown argument: {arg}")
        sys.exit(1)

if src_filename == None:
    sys.stderr.write("LVM file is not given.")
    sys.exit(1)

lvm = LvmData.read(src_filename)
if cols != None:
    lvm.pick_cols(cols)
if compress_col != None:
    lvm.compress_data(compress_col)

yaml.dump(lvm.into_yaml(), sys.stdout, allow_unicode=True)

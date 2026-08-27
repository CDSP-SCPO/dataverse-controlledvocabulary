import argparse
import sys
import os

ENCODING = "iso-8859-1"


def read_prop_file(f):
    d = dict()
    with open(f, mode='r', encoding=ENCODING) as fd:
        for line in fd.readlines():
            if "=" in line:
                prop, val = line.split("=", 1)
                d[prop] = val.rstrip("\n")
    return d


def merge_files(fp_1, fp_2):
    # Read properties of second file
    props = read_prop_file(fp_2)

    # First read the file to check if there is a new line at the end
    new_line = False
    with open(fp_1, mode="r", encoding=ENCODING) as fd:
        # Check if there is a new line
        lines = fd.readlines()
        if len(lines) > 0 and lines[-1] == "\n":
            new_line = True

    # Merge them to first file
    with open(fp_1, mode="a", encoding=ENCODING) as fd:
        # Add a new line first if there is no new line at the end of the file
        for i, (k, v) in enumerate(props.items()):
            if i == 0 and not new_line:
                print(f"\n{k}={v}", file=fd)
            else:
                print(f"{k}={v}", file=fd)
        fd.truncate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file1', type=str, help="Properties file 1")
    parser.add_argument('file2', type=str, help="Properties file 2")
    pargs = parser.parse_args()

    # Get absolute paths
    fp_1 = os.path.abspath(pargs.file1)
    fp_2 = os.path.abspath(pargs.file2)

    # Check if files exist
    for f in [fp_1, fp_2]:
        if not os.path.exists(f):
            print(f"Propeties file {f} does not exist")
            sys.exit(1)

    merge_files(fp_1, fp_2)

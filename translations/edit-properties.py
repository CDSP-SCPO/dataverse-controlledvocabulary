import argparse
import glob
import shutil

ENCODING = "iso-8859-1"

PROP_IGNORE_LIST = [
    # # citation
    # "controlledvocabulary.kindOfData",
    # "controlledvocabulary.topicClassValue",
    # # socialscience
    # "controlledvocabulary.unitOfAnalysis",
    # "controlledvocabulary.collectionMode",
    # "controlledvocabulary.samplingProcedure",
    # "controlledvocabulary.timeMethod",
    # "controlledvocabulary.researchInstrument",
    # geospatial
    "controlledvocabulary.country"
]

FILE_IGNORE_LIST = [

]

FILE_FR_IGNORE_LIST = [

]


def read_prop_file(f):
    d = dict()
    with open(f, mode='r', encoding=ENCODING) as fd:
        for line in fd.readlines():
            if "=" in line:
                prop, val = line.split("=", 1)
                d[prop] = val.rstrip("\n")
    return d


def print_new_prop(filename, mapping, diff, commitdir=None, pval=None):
    print(f"APPEND  {filename}")
    for p in diff:
        print(f"{p}={mapping.get(p) if pval is None else pval}")
        if commitdir:
            with open(f"{commitdir}/{filename}", mode="a", encoding=ENCODING) as fd:
                print(f"{p}={mapping.get(p) if pval is None else pval}", file=fd)


def check_new_prop(args):

    for f in glob.glob("*.properties", root_dir=args.newdir):
        if f in FILE_IGNORE_LIST:
            print(f"SKIP  {f}")
            continue

        try:
            oldlines = read_prop_file(f"{args.olddir}/{f}")
            newlines = read_prop_file(f"{args.newdir}/{f}")

            diff = {elem for elem in newlines.keys() - oldlines.keys() if not elem.startswith(tuple(PROP_IGNORE_LIST))}
            if diff:
                print_new_prop(f, newlines, diff, commitdir=args.olddir if args.commit else None)
            else:
                continue

        except FileNotFoundError as e:
            print(f"{f}  {e}")
            if args.create:
                print(f"COPY  {f}")
                shutil.copy2(f"{args.newdir}/{f}", f"{args.olddir}/{f}")
        except Exception as e:
            print(f"{f}  {e}")
        print("\n\n")


def check_trans(args):
    for f in glob.glob("*[!_fr].properties", root_dir=args.olddir):
        if f in FILE_FR_IGNORE_LIST:
            print(f"SKIP  {f}")
            continue

        filenamefr = "{0}_fr.{1}".format(*f.rsplit('.', 1))
        try:
            lines = read_prop_file(f"{args.olddir}/{f}")
            linesfr = read_prop_file(f"{args.olddir}/{filenamefr}")
            diff = {elem for elem in lines.keys() - linesfr.keys() if not elem.startswith(tuple(PROP_IGNORE_LIST))}

            if diff:
                print_new_prop(filenamefr, dict(), diff, commitdir=args.olddir if args.commit else None, pval="")
            else:
                continue
        except FileNotFoundError as e:
            print(f"{f} / {filenamefr}  {e}")
            if args.create:
                print(f"CREATE  {filenamefr}")
                print_new_prop(filenamefr, dict(), read_prop_file(f"{args.olddir}/{f}"), commitdir=args.olddir, pval="")
        except Exception as e:
            print(f"{f}  {e}")
        print("\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('olddir', type=str, help="Old DV edited property files (https://github.com/CDSP-SCPO/dataverse-controlledvocabulary/tree/main/translations/languageszip)")
    parser.add_argument('newdir', type=str, help="New DV raw property files (https://github.com/IQSS/dataverse/tree/v{DV_VERSION}/src/main/java/propertyFiles)")
    parser.add_argument('-c', '--create', dest='create', action='store_true', help='create new files')
    parser.add_argument('-w', '--write', dest='commit', action='store_true', help='write to files')
    parser.add_argument('-n', '--new', dest='new', action='store_true', help='check new prop')
    parser.add_argument('-t', '--trans', dest='trans', action='store_true', help='check trans')
    pargs = parser.parse_args()

    if pargs.new:
        check_new_prop(pargs)
    if pargs.trans:
        check_trans(pargs)

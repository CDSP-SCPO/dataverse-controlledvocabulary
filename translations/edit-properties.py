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


def print_update_prop(filename, mapping, diff, commitdir=None, pvals=None):
    print(f"UPDATE  {filename}")
    for key in mapping:
        if key in diff:
            print(f"{key}: '{mapping[key]}' -> '{pvals.get(key)}'")
    if commitdir:
        with open(f"{commitdir}/{filename}", mode="r+", encoding=ENCODING) as fd:
            for key in mapping:
                print(f"{key}={pvals.get(key) if key in diff else mapping[key]}", file=fd)
            fd.truncate()


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


def check_missing(args):
    """Check missing translations: check if a key is present without value in _fr files even through the key is present and have a value in the original file"""
    for f in glob.glob("*[!_fr].properties", root_dir=args.olddir):
        if f in FILE_FR_IGNORE_LIST:
            print(f"SKIP  {f}")
            continue

        filenamefr = "{0}_fr.{1}".format(*f.rsplit('.', 1))
        try:
            lines = read_prop_file(f"{args.olddir}/{f}")
            linesfr = read_prop_file(f"{args.olddir}/{filenamefr}")
            diff = {elem for elem in lines.keys() & linesfr.keys() if not elem.startswith(tuple(PROP_IGNORE_LIST)) and lines.get(elem) and not linesfr.get(elem)}

            if diff:
                print(f"MISSING TRANS: {filenamefr}")
                for p in diff:
                    print(f"{p}={lines.get(p)}")
            else:
                continue
        except FileNotFoundError as e:
            print(f"{f} / {filenamefr}  {e}")
        except Exception as e:
            print(f"{f}  {e}")
        print("\n\n")


def check_diff(args):
    for f in glob.glob("*[!_fr].properties", root_dir=args.olddir):
        if f in FILE_IGNORE_LIST:
            print(f"SKIP  {f}")
            continue

        try:
            oldlines = read_prop_file(f"{args.olddir}/{f}")
            newlines = read_prop_file(f"{args.newdir}/{f}")

            diff = {elem for elem in oldlines.keys() & newlines.keys() if not elem.startswith(tuple(PROP_IGNORE_LIST)) and oldlines.get(elem) != newlines.get(elem)}
            if diff:
                print_update_prop(f, oldlines, diff, commitdir=args.olddir if args.commit else None, pvals=newlines)
            else:
                continue

        except FileNotFoundError as e:
            print(f"{f}  {e}")
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
    parser.add_argument('-m', '--missing', dest='missing', action='store_true', help='check missing translations')
    parser.add_argument('-d', '--diff', dest='diff', action='store_true', help='check diff values')
    pargs = parser.parse_args()

    if pargs.new:
        check_new_prop(pargs)
    if pargs.trans:
        check_trans(pargs)
    if pargs.missing:
        check_missing(pargs)
    if pargs.diff:
        check_diff(pargs)

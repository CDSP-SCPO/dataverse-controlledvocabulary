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


def read_prop_files(oldfile, newfile):
    oldlines = dict()
    newlines = dict()
    with open(oldfile, mode='r', encoding=ENCODING) as oldfd:
        for line in oldfd.readlines():
            if "=" in line:
                prop, val = line.split("=", 1)
                oldlines[prop] = val.rstrip("\n")
    with open(newfile, mode='r', encoding=ENCODING) as newfd:
        for line in newfd.readlines():
            if "=" in line:
                prop, val = line.split("=", 1)
                newlines[prop] = val.rstrip("\n")
    return oldlines, newlines


def print_new_prop(filename, mapping, diff, commitdir=None):
    print(f"APPEND  {filename}")
    for p in diff:
        print(f"{p}={mapping.get(p)}")
        if commitdir:
            with open(f"{commitdir}/{filename}", mode="a", encoding=ENCODING) as fd:
                print(f"{p}={mapping.get(p)}", file=fd)


def check_new_prop(args):

    for f in glob.glob("*.properties", root_dir=args.newdir):
        if f in FILE_IGNORE_LIST:
            print(f"SKIP  {f}")
            continue

        try:
            oldlines, newlines = read_prop_files(f"{args.olddir}/{f}", f"{args.newdir}/{f}")

            diff = {elem for elem in newlines.keys() - oldlines.keys() if not elem.startswith(tuple(PROP_IGNORE_LIST))}
            if diff:
                print_new_prop(f, newlines, diff, commitdir=args.olddir if args.commit else None)
            else:
                continue

        except FileNotFoundError as e:
            print(f"COPY  {f}")
            shutil.copy2(f"{args.newdir}/{f}", f"{args.olddir}/{f}")
        except Exception as e:
            print(f"{f}  {e}")
        print("\n\n")


def check_trans(args):  # TODO check between oldfiles & oldfiles_fr (if !exist -> write&print + if val !exist -> print)
    for f in glob.glob("*.properties", root_dir=args.newdir):
        try:
            pass
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"{f}  {e}")
        print("\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('olddir', type=str, help="Old DV edited property files (https://github.com/CDSP-SCPO/dataverse-controlledvocabulary/tree/main/translations/languageszip)")
    parser.add_argument('newdir', type=str, help="New DV raw property files (https://github.com/IQSS/dataverse/tree/v{DV_VERSION}/src/main/java/propertyFiles)")
    parser.add_argument('-w', '--write', dest='commit', action='store_true', help='write to oldfiles')
    args = parser.parse_args()

    check_new_prop(args)
    print(args)
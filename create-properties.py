import argparse
import csv
import os
import shutil
from collections import defaultdict
from operator import itemgetter

OUTPUT_DIR = 'output'
LANGUAGES = ['en_US', 'fr_FR']


# transforms the code to the property format
# http://guides.dataverse.org/en/latest/admin/metadatacustomization.html#id8
def transform_code(code):
    result = code.lower().replace(' ', '_')
    return result


def main(args):
    with open(args.file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        output = defaultdict(str)
        for row in csv_reader:
            fields = ['block', 'field', 'code', 'term_en', 'term_fr']
            block, field, code, term_en, term_fr = itemgetter(*fields)(row)
            block = block.replace('_', '')  # dv properties do not have underscores in their file name
            code = transform_code(code)
            output[f'en_US/{block}.properties'] += f'controlledvocabulary.{field}.{code}={term_en}\n'
            output[f'fr_FR/{block}_fr.properties'] += f'controlledvocabulary.{field}.{code}={term_fr}\n'

    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for language in LANGUAGES:
        os.makedirs(f'{OUTPUT_DIR}/{language}', exist_ok=True)

    for key, value in output.items():
        file_path = f'{OUTPUT_DIR}/{key}'
        with open(file_path, mode='ab') as props_file:
            # strings must be latin_1 for dv
            encoding = 'latin_1' if args.encode else 'utf_8'
            props_file.write(value.encode(encoding))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate dataverse properties for translation.')
    parser.add_argument('file', type=str, help='the CSV file for mapping')
    parser.add_argument('-e', '--encode', dest='encode', action='store_true', help='encode special characters in latin_1')
    args = parser.parse_args()
    main(args)

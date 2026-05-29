#!/usr/bin/env bash

set -uo pipefail

TMPDIR=$(mktemp -d /tmp/dv_langpacks.XXXXXX)

DATAVERSE_REPO="IQSS/dataverse"

if [[ $# -ne 1 ]]; then
  echo "usage: $(basename "$0") <dataverse version>"
  exit 1
fi

version="$1"

# Fetch Dataverse zip file
wget -O "${TMPDIR}/${version}.zip" "https://github.com/${DATAVERSE_REPO}/archive/refs/tags/${version}.zip" 

# Unzip and copy properties to current directory
unzip "${TMPDIR}/${version}.zip" -d "${TMPDIR}"
mkdir -p "${TMPDIR}/language_pack"
find ${TMPDIR}/dataverse*/src/main/java -name '*.properties' -exec cp -prv '{}' "${TMPDIR}/language_pack" ';'

# Add French translation to language_pack folder
cp -r translations/fr_FR/* "${TMPDIR}/language_pack/"

# Merge citation and socialsciences properties
for file in "citation" "geospatial" "socialscience"; do
  python3 translations/merge-properties.py "${TMPDIR}/language_pack/${file}.properties" "translations/custom/en_US/${file}.properties"
  python3 translations/merge-properties.py "${TMPDIR}/language_pack/${file}_fr.properties" "translations/custom/fr_FR/${file}_fr.properties"
done 

# Zip folder
zip -j "language_${version}.zip" ${TMPDIR}/language_pack/*.properties

#!/usr/bin/env bash

set -uo pipefail

TMPDIR=$(mktemp -d /tmp/dv_metadatablock.XXXXXX)

DATAVERSE_REPO="IQSS/dataverse"

if [[ $# -ne 1 ]]; then
  echo "usage: $(basename "$0") <dataverse version>"
  exit 1
fi

version="$1"

# Fetch citation.tsv and social_science.tsv from Dataverse repo
for file in "citation" "social_science"; do
  wget -O "${TMPDIR}/${file}.tsv" "https://raw.githubusercontent.com/${DATAVERSE_REPO}/refs/tags/${version}/scripts/api/data/metadatablocks/${file}.tsv"
done 

# Merge partial files with fetched ones
cat ${TMPDIR}/citation.tsv metadatablocks/custom/citation.tsv > citation.tsv
cat ${TMPDIR}/social_science.tsv metadatablocks/custom/social_science.tsv > social_science.tsv

# Copy geospatial ones to root of repository
cp metadatablocks/geospatial_0.tsv geospatial_0.tsv
cp metadatablocks/geospatial.tsv geospatial.tsv

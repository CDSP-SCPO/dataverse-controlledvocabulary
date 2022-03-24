# dataverse-controlledvocabulary

Controlled vocabulary used by the CDSP.


## Dataverse metadata blocks

We created custom TSV files following the 
[CESSDA Metadata Model](https://doi.org/10.5281/zenodo.3236171).

Borschewski, Kerrin, Hermann, Julia, Zenk-Möltgen, Wolfgang, Bockaj, Brigita, Bolko, Irena, Vipavc Brvar, Irena, … Bell, Darren. (2019). CMM CESSDA Metadata Model (Version 0.1). Zenodo.

We consulted also this Metadata Crosswalk: The Dataverse Project. (2020, February). Dataverse 4.0+ Metadata Crosswalk. https://docs.google.com/spreadsheets/d/10Luzti7svVTVKTA-px27oq3RxCUM-QbiTkm8iMd5C54


### Fields added or modified (`<cessda_field>` → `<dataverse_field>`)

`citation.tsv`:
- [x] `KindOfData` → `kindOfDataType`
- [X] `TopicClassification` → `topicClassValue`

`social_science.tsv`:
- [x] `AnalysisUnit` → `unitOfAnalysis`
- [x] `ModeOfCollection` → `collectionMode`
- [x] `SamplingProcedure` → `samplingProcedure`
- [x] `TimeMethod` → `timeMethod`
- [x] `TypeOfInstrument` → `researchInstrument`

We also changed the `geospacial.tsv` file to update country values using ISO 3166. We needed to update the values in two steps:
1. `geospatial_0.tsv` adds the IDs to each value
1. `geospatial.tsv` updates the values


### Translation

The script `create-properties.py` is used to generate dataverse properties from a CSV containing controlled vocabulary with their translation (see `controlled_vocabulary.csv`). These properties need to be added to the corresponding property files in the languages.zip (https://guides.dataverse.org/en/latest/installation/config.html#creating-a-languages-zip-file).

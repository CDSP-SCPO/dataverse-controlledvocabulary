Controlled vocabulary used by the CDSP.

We used the 
[CESSDA Metadata Model](https://doi.org/10.5281/zenodo.3236171)

Borschewski, Kerrin, Hermann, Julia, Zenk-Möltgen, Wolfgang, Bockaj, Brigita, Bolko, Irena, Vipavc Brvar, Irena, … Bell, Darren. (2019). CMM CESSDA Metadata Model (Version 0.1). Zenodo.

We consulted also this Metadata Crosswalk: The Dataverse Project. (2020, February). Dataverse 4.0+ Metadata Crosswalk. https://docs.google.com/spreadsheets/d/10Luzti7svVTVKTA-px27oq3RxCUM-QbiTkm8iMd5C54
citation.tsv:
- [x] KindOfData -> kindOfDataType
- [X] TopicClassification -> topicClassValue

social_science.tsv:
- [x] AnalysisUnit -> unitOfAnalysis
- [x] ModeOfCollection -> collectionMode
- [x] SamplingProcedure -> samplingProcedure
- [x] TimeMethod -> timeMethod
- [x] TypeOfInstrument -> researchInstrument

(Meaning: <cessda_field> -> <dataverse_field>)


`create-properties.py`: script to generate dataverse properties from a CSV containing controlled vocabulary (see `controlled_vocabulary.csv`). These properties are used to configure the displayed names of the CV and the translations.

To update the country values with ISO 3166, we have to upload two TSV files:
- `geospatial_1.tsv` adds the IDs to each value
- `geospatial_2.tsv` updates the values

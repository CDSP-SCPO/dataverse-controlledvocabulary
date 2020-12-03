Controlled vocabulary used by the CDSP.

We used the 
[CESSDA Metadata Model] (https://doi.org/10.5281/zenodo.3236171)


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


`create-properties.py`: script to generate dataverse properties for the controlled vocabulary. These properties are used to configure the displayed names of the CV and the translations.

To update the country values with ISO 3166, we have to upload two TSV files:
- `geospatial_1.tsv` adds the IDs to each value
- `geospatial_2.tsv` updates the values

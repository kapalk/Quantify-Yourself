# Quantify-yourself-project
The aim of the project was to investigate different factors which affect sleep quality. In addition, the aim was to create a novel measurement for sleep quality. Results showed that the measured variables had highly individual effects on sleep quality. Despite this our classifier model was quite successful in classifying sleep quality. This shows that our measure for sleep quality (peak count) correlates with subjective evaluations.

Unfortunately the original data used in this study cannot be shared due to privacy reasons.

# Directories

Under `bed_sensor/`:

- `preprocessing.py`: separates nights according to survey answers and 
                      separates subjects. final results is python dictionary 
                      where subjects are keys and values are lists of nights.
                      Nights contain timestamps, median-filtered respiration rate
                      and its rolling sd. This dictionary is saved as pickle dump.
- `rrPreprocess.py`: preprocess respiration rate
- `sleepQuality.py`: determines a value to describe sleep quality from rolling standard deviation of respiration rate

Under `figs/`:

- Results of the FAMD for each individual and visualization of peak_counts

Under `classifying/`:

- `alldata.csv`: learning data
- `featureSelection.py`: feature selection for classifying
- `LogisticRegression`: logistic regression
- `temp.py:` visualization of peak count


# Scripts
- `outside_light_intensity_reader.py`: reads outside light intensity from outside.aalto.fi .
- `outside-light-intensity-preprocess.py`: preprocessing of the light intensity data.
- `surveyHandling.py`: reorganizes survey data. The output is dictionary where subjects are keys and values are pandas dataframes which columns are answers from user-defined questions and index is datetime.
- `combineData.py`: combiness sensor, survey and light intensity data.
- `FAMD.r`: FAMD for each each subject.

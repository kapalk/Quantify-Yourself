# Quantify-yourself-project
The goal of the project was to investigate different factors which affect sleep quality. In addition, a goal was to create a novel measurement for sleep quality. Unfortunately the data used in this study cannot be shared because of privacy reasons

# Directories

Under `bed_sensor/`:

- `preprocessing.py`: separates nights according to survey answers and 
                      separates subjects. final results is python dictionary 
                      where subjects are keys and values are lists of nights.
                      Nights contain timestamps, median-filtered respiration rate
                      and its rolling sd. This dictionary is saved as pickle dump.
- `rrPreprocess.py`: preprocess respiration rate
- `sleepQuality.py`: determines a value to describe sleep quality from rolling standard deviation of respiration rate

# Scripts
- `outside_light_intensity_reader.py`: reads outside light intensity from outside.aalto.fi
- `outside-light-intensity-preprocess.py`: preprocessing of the light intensity data
- `surveyHandling.py`: reorganizes survey data. The output is dictionary where subjects are keys and values are pandas dataframes which columns are answers from user-defined questions and index is datetime.

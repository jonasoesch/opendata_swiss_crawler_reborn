import datetime
# In order to analyze them, the datasets are downloaded.
# If you want to keep them ('keep_data'), this takes a lot of space
# Here you have the option to change the output dir
data_dir = "./temp"

# Stores all the data, which takes 100+ GB for the whole platform
keep_data = False

# The results are saved to a JSON-File. Define how it should be called here
output_file = "./output/"+str(datetime.date.today().strftime("%Y%m%d"))+"_opendata.swiss.datasets.json"

logfile = "./output/"+str(datetime.date.today().strftime("%Y%m%d"))+"_log"


# A specific range of datasets can be downloaded. This is especially useful when
# the crawler has crashed at a certain point.
start_from = 0
finish_at  = 9000

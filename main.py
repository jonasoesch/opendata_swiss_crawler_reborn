import requests
import ssl
import json
import time
from dataset import Dataset
import os
import config as cfg
import logging
import datetime

# Data-Structure:
#
# name
# id
# description
# organization
#   name
#   political level
# tags[]
# downloads[]
#   format
#   url
#   created
#   issued
#   modified
#   rights
#   size



logging.basicConfig(filename=cfg.logfile,level=logging.INFO)

def dump(datasets):
    tempfile = cfg.output_file + '.tmp'
    with open(tempfile, 'w') as fp:
        fp.write(
            json.dumps(
                [dataset.serialize() for dataset in datasets],
                indent=4, separators=(',', ': ')
            )
        )
        fp.flush(); # Paranoid writing to disk as in https://stackoverflow.com/questions/2333872/atomic-writing-to-file-with-python
        os.fsync(fp.fileno());
    os.rename(tempfile, cfg.output_file)



def resume():
    try:
        with open(cfg.output_file, 'r') as file:
            datasets = []
            for dataset in json.load(file):
                dataset_object = Dataset(dataset, True)
                datasets.append(dataset_object)

            return datasets
    except Exception:
        return []



try:
    # Get the list of Datasets
    r = requests.get("https://opendata.swiss/api/3/action/package_list")
    packages = r.json()

    # packages = {
    #     'result': [
    #         'abfallgefasse',
    #         'bazl-geocat-harvester',
    #         'bodenubersichtskarte-wms-dienst',
    #     ]
    # }

    datasets = resume()

    logging.info("=========== Starting a new run =============")
    logging.info("It's: "+str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")) )
    logging.info("The total number of packages is: " + str(len(packages['result'])))

    for i, package in enumerate(packages['result']):

        dataset_name = package #packages['result'][i]
        dataset = None

        if (i > cfg.finish_at): break
        if (i < cfg.start_from): continue

        exists = False
        for ds in datasets:
            if (ds.id == dataset_name):
                logging.info("Reading from cache: " + str(i) + ". "+ ds.id)
                print "Reading from cache: " + str(i) + ". "+ ds.id
                dataset = ds
                break


        if not(dataset):
            time.sleep(0.2)


            try:
                logging.info("https://opendata.swiss/api/3/action/package_show?id=" + dataset_name)
                ds = requests.get("https://opendata.swiss/api/3/action/package_show?id=" + dataset_name)
            except (ssl.SSLError):
                continue


            if ds.status_code == 200:
                logging.info("Adding: " + str(i) + ". " + dataset_name)
                print "Adding: " + str(i) + ". " + dataset_name
                result = ds.json()['result']
                dataset = Dataset(result, False)
                datasets.append(dataset)

            else:
                logging.info("Status code " + ds.status_code)

        for dl in dataset.downloads:
            if not(dl.status == 'Downloaded' or dl.status == "Analyzed"):
                print "Downloading..."
                dl.download()
            if not(dl.status == 'Analyzed'):
                print "Analyzing..."
                dl.analyze()

            if(not(cfg.keep_data)):
                dl.delete_file()

        dump(datasets)
except Exception as e:
    logging.exception("Crawler crashed. Error: %s", e)

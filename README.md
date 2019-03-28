# opendata.swiss Crawler

This is a crawler for the Open Data-Plattform of the Swiss Confederation. [opendata.swiss](http://opendata.swiss) collects open datasets from the national, cantonal and communal administration which is published for free use. The crawler attempts to download each dataset and analyze it.

## Usage

First of all you should set all the options in `config.py` to your preference.
Then you can build the docker image on your computer (you're free to choose your own tag):

```
docker build --tag=opendata .
```

Run the image by mounting the host directory in docker (see the [Docker documentation](https://docs.docker.com/storage/bind-mounts/) for details):
```
docker run -v /Users/jonas/Desktop/opendata_swiss_crawler:/app opendata
```

There is also a `cron`-file that can be used to run the script every Thursday. Modify the command to match your setup (path and docker image tag) and [add it to your crontab](https://www.adminschoice.com/crontab-quick-reference).

One run takes about 16 hours in order to download and analyze over 3000 datasets.

## Results

The result of the analysis is stored at the `output_file` path that is defined in the `config.py` file. By default its a timestamped JSON-file in the `output`-directory.

For every timestamp there is also a logfile.

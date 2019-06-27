---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.0'
      jupytext_version: 1.0.5
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import pandas as pd
from pdvega import Axes
import pdvega
```

```python
from pandas.io.json import json_normalize
import json
```

## Setup
```python
def reader(path):
    date = path.split("_")[0]
    with open("../output/"+path) as f:
        a = json.load(f)
        a = json_normalize(a, ['downloads'], ['description', 'id', 'name', ['organization', 'name'], 'tags'])
    b = pd.DataFrame(a)
    print(len(b))
    b["date"] = pd.to_datetime(date)
    return b
```

## Importing the data
```python
li = list(map(reader, ["20171031_opendata.swiss.datasets.json",
                  "20180322_opendata.swiss.datasets.json",
                  "20180818_opendata.swiss.datasets.json",
                  "20180704_opendata.swiss.datasets.json",
                  "20180906_opendata.swiss.datasets.json",
                  "20181031_opendata.swiss.datasets.json",
                  "20181107_opendata.swiss.datasets.json",
                  "20181128_opendata.swiss.datasets.json",
                  "20190109_opendata.swiss.datasets.json",
                  "20190504_opendata.swiss.datasets.json",
                  "20190508_opendata.swiss.datasets.json",
                  "20190529_opendata.swiss.datasets.json",
                  "20190605_opendata.swiss.datasets.json",
                  "20190619_opendata.swiss.datasets.json"
                 ]))
```

```python
ods = pd.concat(li)
ods.rename({"organization.name": "organization"}, axis=1, inplace=True)
```

```python
top = ods.groupby(["date", "id"]).first().reset_index()
top.head()
```

```python
len(top[top.date == "2019-05-08"])
```

```python
len(top[top.date == "2019-05-04"])
```

## 1. Datasets

We start by inspecting how the number of datasets on the platform has evolved. Expect for a jump in 2018, the growth has been relatively steady.

```python
datasets1 = top.groupby(["date"]).id.count().to_frame().reset_index()
Axes({
   "mark": "line",
    "encoding": {
        "x": {
            "field": "date",
            "type": "temporal"
        },
        "y": {
            "field": "id",
            "type": "quantitative",
            "axis": {"title": "datasets"}
        }
    },
    "width": 800,
    "height": 300
}, datasets1)
```

## 2. Datasets by Organization

Different organizations publish datasets. Yet it is the FSO who is responsible for most of the growth of the platform in the last year. When zooming in, other organizations who have contributed to the growth become visible such as Geoinformation Kanton Zürich and Kanton Basel-Stadt.


```python
orgas = top.groupby(["organization", "date"]).id.count().to_frame().reset_index()
```

```python
Axes({
    "mark": "line",
    "selection": {
        "a": {
            "type": "interval",
            "bind": "scales",
            "encodings": ["y"]
        }
    },
    "encoding": {
        "x": {
            "field": "date",
            "type": "temporal"
        },
        "y": {
            "field": "id",
            "type": "quantitative",
            "axis": {"title": "datasets"}
        },
        "color": {
            "field": "organization",
            "type": "nominal"
        },
        "tooltip": {
            "field": "organization",
            "type": "nominal" 
        }
    },
         "width": 700,
        "height": 1000
}, orgas)
```

## 3 File size over time

Interestingly the jump in newly provided FSO datasets in 2018 didn't affect the total file size so much. This is mostly because the FSO doesn't provide a large quantitiy of data compared to the City of Zürich or the SBB for example. For some organizations there are some strange spikes to the bottom at the end of November 2018. This might be due to data collection issues and no represent the reality.

```python
ods.loc[ods.file_size == "undefined", "file_size"] = 0
```

```python
filesize3 = ods.groupby("date").file_size.sum().reset_index()
filesize3.file_size = filesize3.file_size / 1000 / 1000 / 1000
Axes({
    "mark": "line",
    "encoding": {
        "x": {
            "field": "date",
            "type": "temporal"
        },
        "y": {
            "field": "file_size",
            "type": "quantitative",
            "axis": {"title": "Total downloadable file size in GB"}
        }
    },
    "height": 600,
    "width": 700
}, filesize3)
```

```python
fs_orga = ods.groupby(["date", "organization"]).file_size.sum().to_frame().reset_index()
fs_orga.file_size = fs_orga.file_size / 1000 / 1000 / 1000
fs_orga.groupby("organization")["file_size"].max().sort_values(ascending=False).head()
```

```python
Axes({
    "mark": "line",
    "selection": {
        "a": {
            "type": "interval",
            "bind": "scales",
            "encodings": ["y"]
        }
    },
    "encoding": {
        "x": {
            "field": "date",
            "type": "temporal"
        },
        "y": {
            "field": "file_size",
            "type": "quantitative",
            "axis": {"title": "Downloadable file size in GB"}
        },
        "color": {
            "field": "organization",
            "type": "nominal",
            "sort": {"field": "file_size", "op": "sum"}
        },
        "tooltip": {
            "field": "organization",
            "type": "nominal" 
        }
    },
         "width": 700,
        "height": 1000
}, fs_orga)
```

## 4. Status Codes

```python
status4 = ods.groupby(["date", "status_code"]).id.count().reset_index()
status4.head()
```

```python
Axes({
  "mark": "area",
        "selection": {
        "a": {
            "type": "interval",
            "bind": "scales",
            "encodings": ["y"]
        }
    },
  "encoding": {
    "x": {
        "field": "date", 
        "type": "temporal"
    },
    "color": {
        "field": "status_code", 
        "type": "nominal"
    },
    "y": {
        "field": "id", 
        "type": "quantitative",
        "stack": "normalize",
        "axis": {"title": "Share of status code", "format": ".0%"}
    },
     "tooltip": {
        "field": "status_code", 
        "type": "nominal"
    }   
  },
   "width": 600,
    "height": 700
}, status4)
```

Open question: Are the non-200 status codes mainly coming from certain organizations or are they equally distributed?


## Formats

A look at the evolution of dataset formats prominently shows a rise in `HTML`. This typically means that an organization has its own platform and doesn't provide a direct download link. These datasets also don't correctly appear in the statistics on the total size.

The disapearance of the PC-AXIS format, formerly provided by the FSO is also clearly visible.

In contrast to the [recommendations](https://5stardata.info/en/), more and more PDFs are being published and less CSVs. This may also be due to actors sharing data on the platform.

```python
formats = ods.groupby(["date", "format"]).id.count().to_frame().reset_index()
```

```python
Axes({
  "mark": "area",
        "selection": {
        "a": {
            "type": "interval",
            "bind": "scales",
            "encodings": ["y"]
        }
    },
  "encoding": {
    "x": {
        "field": "date", 
        "type": "temporal"
    },
    "color": {
        "field": "format", 
        "type": "nominal"
    },
    "y": {
        "field": "id", 
        "type": "quantitative",
        "stack": "normalize",
        "axis": {"title": "Share of data format code", "format": ".0%"}
    },
     "tooltip": {
        "field": "format", 
        "type": "nominal"
    }   
  },
   "width": 600,
    "height": 700
}, formats)
```

## Descriptions

```python
len(top[top.description.str.len() == 0]) / len(top)
```

```python
desc = top.groupby("date").apply(lambda d: d.description.str.len() == 0).to_frame().reset_index().rename({"level_1": "ct"}, axis=1)
descs = desc.groupby(["date", "description"]).count().reset_index()
descs.head()
```

```python
Axes({
  "mark": "area",
  "encoding": {
    "x": {
        "field": "date", 
        "type": "temporal"
    },
    "color": {
        "field": "description", 
        "type": "nominal"
    },
    "y": {
        "field": "ct", 
        "type": "quantitative",
        "stack": "normalize"
    },
     "tooltip": {
        "field": "description", 
        "type": "nominal"
    }   
  },
   "width": 600,
    "height": 300
}, descs)
```

```python
lic = ods.groupby(["date", "rights"]).id.count().to_frame().reset_index()
lic.head()
```

```python
Axes({
  "mark": "area",
  "encoding": {
    "x": {
        "field": "date", 
        "type": "temporal"
    },
    "color": {
        "field": "rights", 
        "type": "nominal"
    },
    "y": {
        "field": "id", 
        "type": "quantitative",
        "stack": "normalize"
    },
     "tooltip": {
        "field": "rights", 
        "type": "nominal"
    }   
  },
   "width": 600,
    "height": 300
}, lic)
```

```python
ds = ods[(ods.date > "2018-01-12") & (ods.file_size > 5000000)].copy()
ds["fs"] = ds.file_size / 1000000
```

```python
Axes({
  "mark": "circle",
  "encoding": {
    "y": {
        "field": "organization", 
        "type": "nominal"
    },
    "x": {
        "field": "fs", 
        "type": "quantitative",
        "scale": {"type": "pow", "exponent": "0.4"}
    },
     "tooltip": {
        "field": "name", 
        "type": "nominal"
    },
    "href": {
        "field": "url",
        "type": "nominal"
    }
  },
   "width": 800,
    "height": 1200
}, ds)
```

```python
ods[(ods.date > "2018-01-12") & (ods.file_size > 10000000)].head()
```

```python

```

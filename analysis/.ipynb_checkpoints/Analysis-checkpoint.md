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

## Datensätze

```python
top.groupby(["date"]).id.count().to_frame().reset_index().vgplot.line(x="date", y="id")
```

## Datensätze pro Organisation

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
            "type": "quantitative"
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
         "width": 1000,
        "height": 1000
}, orgas)
```

## File size over time

```python
ods.loc[ods.file_size == "undefined", "file_size"] = 0
```

```python
ods.groupby("date").file_size.sum().vgplot.line()
```

```python
fs_orga = ods.groupby(["date", "organization"]).file_size.sum().to_frame().reset_index()
fs_orga.head()
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
            "type": "quantitative"
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

## Status Codes

```python
ods[(ods.status_code != 200) & (ods.date > '2019-03-20')].groupby("status_code").id.count().vgplot.bar()
```

```python
ods[ods.status_code != 200].groupby(["date"]).id.count().vgplot.line()
```

## Formats

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
        "stack": "normalize"
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

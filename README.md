Datahub service for running dataflows

## Factory

The service is responsible for running the flows for datasets that are frequently updated and maintained by [Datahub](https://datahub.io/). Service is using [Datapackage Pipelines](https://github.com/frictionlessdata/datapackage-pipelines) is a framework for declarative stream-processing of tabular data, and [DataFlows](https://github.com/datahq/dataflows) to run the flows through pipelines to process the datasets.

## Install

You will need python 3.x.

```
pip install -r requirements.txt
```

## Developers

Each dataset is `datasets` directory is a standalone repository on GitHub and should be submoduled in and then built:

```
git submodule init && git submodule update
```

Each dataset should have it's flows written as python script and `pipeline-spec.yaml` pointing to flow to run:

* `annual-prices.py`

```

from dataflows import Flow, dump_to_path, load, add_metadata

def flow(parameters, datapackage, resources, stats):
    return Flow(load(load_source='http://www.exampel.com/my-data.csv'))
```

* `pipeline-spec.yaml`

```
example-flow:
  pipeline:
  - flow: annual-prices
  - run: datahub.dump.to_datahub
```

Factory server will read `pipeline-spec.yaml` for each dataset and run the flows and processors stated there. In the example above

1. Run the flows (`annual-prices.py`) and load the data from `http://www.exampel.com/my-data.csv`
2. Run the custom [`datahub.dump.to_datahub`](https://github.com/datahq/datapackage-pipelines-datahub) processors and push files to [datahub.io](https://datahub.io/)

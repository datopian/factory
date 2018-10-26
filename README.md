Datahub service for running dataflows

## Factory

The service is responsible for running the flows for datasets that are frequently updated and maintained by [Datahub](https://datahub.io/). Service is using [Datapackage Pipelines](https://github.com/frictionlessdata/datapackage-pipelines) is a framework for declarative stream-processing of tabular data, and [DataFlows](https://github.com/datahq/dataflows) to run the flows through pipelines to process the datasets.

## Install

You will need python 3.x.

```
pip install -r requirements.txt
```

## Add dataset to factory

Each "folder" in `datasets` directory is named after publisher's username and each dataset in it is a standalone repository on GitHub and should be submoduled. To add a new datasets you will need to submodule your dataset repo into related directory (or create if not exists).

```
mkdir datasts/example
cd datasets/example
git submodule add https://github.com/example/my-awesome-dataset
```

Each dataset should have it's flows written as python script and `pipeline-spec.yaml` pointing to flow to run:

* `annual-prices.py` - script responsible for getting the data, tidy and normalisation

```

from dataflows import Flow, dump_to_path, load, add_metadata

def flow(parameters, datapackage, resources, stats):
    return Flow(load(load_source='http://www.exampel.com/my-data.csv'))
```

* `pipeline-spec.yaml` - metadata about pipelines. Here you should define which flows exactly to run and where the config file is saved

```
example-flow:
  pipeline:
  - flow: annual-prices
  - run: datahub.dump.to_datahub
    parameters:
      config: ~/.config/datahub/config.json.example
```

Factory server will read `pipeline-spec.yaml` for each dataset and run the flows and processors stated there. In the example above

1. Run the flows (`annual-prices.py`) and load the data from `http://www.exampel.com/my-data.csv`
2. Run the custom [`datahub.dump.to_datahub`](https://github.com/datahq/datapackage-pipelines-datahub) processors and push files to [datahub.io](https://datahub.io/)

### Config files

To publish dataset on Datahub, each user has it's own config file. We need this config file for each user who is subscribed to factory in order to push datasets under appropriate username.

Config files for Datahub are usually saved in `~/.config/datahub/config.json`. You will probably need to login with your datahub account if you can't find one. Login in and copy your config file in secrets directory.

```
data login
cp ~/.config/datahub/config.json secrets/config.json.example
```

In order to add new config file to the list, you will have to add `cinfig.json.example` to the `secrets/secrets.tar` Which is encrypted. Please contact if you are not the member of datahub developers team, else:

* Download and decrypt `secrets.tar.enc` from private GitLab repository
* extract `secrets.tar`
* add `cinfig.json.example` to the directory
* archive `secrets.tar`
* encrypt with `travis enctypr-file` and push back to github
  * In parallel encrypt with password (used when decrypting) and push back file to GitLab private repo

```
# Extract
tar xvf secrets.tar
# Add new Config
cp ~/.config/datahub/config.json secrets/config.json.example
# Archive again
tar cvf secrets.tar secrets/
# Encrypt
travis encrypt-file secrets.tar
# Commit and push
git add secrets.tar.enc
git commit -m"example user's config"
git push
```

## Developers

When working locally you will need to update all submodules

```
git submodule init && git submodule update
```

# CYtoSJ - Compose YAML to Swarm JSON

Translate [`docker-compose`](https://docs.docker.com/compose/)'s [YAML files](https://docs.docker.com/compose/yml/) into [Giant Swarm](https://giantswarm.io/)'s [JSON configuration](http://docs.giantswarm.io/reference/swarm-json/).

Read: "Cytos-Jay"

## Install

Requires the `yaml` package, which can be installed using

```
pip install yaml
```

Please use sudo to install globally.

Proper installation via Pypi and `pip` may follow.

## Usage:

```
python cytosj.py -n myapp path/to/docker-compose.yml
```

This will generate a JSON file in the same directory holding the source file, named accordingly.

Use `-h` for details.

## Features

* Translates most compose YAML files to ready-to-use application configuration JSON files
* Shows hints and warnings if details from the source can't be translated

## Known limitations

* Currently tested only on Python 2.7
* `expose` is ignored (currently)
* `env_file` is ignored (currently)
* `extends` is ignored (currently)
* `external_links` is ignored (and probably will be forever)
* Doesn't translate `volumes_from`, since Giant Swarm doesn't support this
* For `volumes`, so far only the `HOST:CONTAINER` format is supported
* If a dependency points to a component with multiple `ports` entries, the first port is used for that dependency automatically.

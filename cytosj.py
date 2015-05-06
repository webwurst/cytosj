# coding: utf8

import sys
import json
import yaml
import argparse
import os


def load_docker_compose_file(path):
    with open(path, "r") as stream:
        data = yaml.load(stream.read())
        return data

def transform(source, app_name):
    """
    Return swarm.json-style dict from docker-compose-style dict
    """
    warnings = set()

    if app_name == "":
        warnings.add("Don't forget to set the app_name in the generated JSON file.")

    sj = {
        "app_name": app_name,
        "services": []
    }

    # helper structure for all exposed ports
    # (used to map depedencies)
    portmap = {}

    # create services and components
    for unit in source.keys():
        service = {
            "service_name": unit,
            "components": [
                {
                    "component_name": unit
                }
            ]
        }

        # component properties
        for attribute in source[unit].keys():

            if attribute == "build":
                warnings.add("Component '%s/%s' has no image definition yet ('build' from YAML can't be converted)." % (unit, unit))
                service["components"][0]["image"] = ""

            elif attribute == "image":
                service["components"][0]["image"] = source[unit]["image"]
                # image validation
                if "/" in source[unit]["image"]:
                    parts = source[unit]["image"].split("/")
                    if len(parts) == 2 or len(parts) > 3:
                        warnings.add("The image '%s' is invalid. Please change to format 'registry.giantswarm.io/<organization>/<imagename>[:<tag>]'." % source[unit]["image"])
                    if len(parts) > 1:
                        if parts[0] != 'registry.giantswarm.io':
                            warnings.add("The image '%s' uses an invalid registry name '%s'. Please change to 'registry.giantswarm.io'." % (source[unit]["image"], parts[0]))
            
            elif attribute == "ports":
                portmap_key = "%s/%s" % (unit, unit)
                portmap[portmap_key] = []
                service["components"][0]["ports"] = []
                for port in source[unit]["ports"]:
                    if ":" in str(port):
                        host, container = port.split(":")
                    else:
                        container = port
                    service["components"][0]["ports"].append(int(container))
                    portmap[portmap_key].append(int(container))              
            
            elif attribute == "environment":
                service["components"][0]["env"] = source[unit]["environment"]
            
            elif attribute == "command":
                command_parts = source[unit]["command"].split()
                service["components"][0]["args"] = command_parts
            
            elif attribute == "volumes":
                service["components"][0]["volumes"] = []
                for volume in source[unit]["volumes"]:
                    # TODO:
                    # - allow for '<path>' only format
                    # - allow for '<path>:<path>:ro' format
                    host_path, container_path = volume.split(":")
                    service["components"][0]["volumes"].append({
                        "path": container_path,
                        "size": "2 GB"  # default (smallest possible)
                    })

            elif attribute == "links":
                service["components"][0]["dependencies"] = []
                for link in source[unit]["links"]:
                    if ":" in link:
                        link, alias = link.split(":")
                    else:
                        alias = link
                    dependency = {
                        "name": "%s/%s" % (link, link),
                        "alias": alias,
                        "port": None  # leave that for later
                    }
                    service["components"][0]["dependencies"].append(dependency)
            
            else:
                warnings.add("The key '%s' has been ignored" % attribute)

        sj["services"].append(service)

    # set ports in dependencies
    for s in range(len(sj["services"])):
        for c in range(len(sj["services"][s]["components"])):
            portmap_key = sj["services"][s]["service_name"] + "/" + sj["services"][s]["components"][c]["component_name"]
            if "dependencies" in sj["services"][s]["components"][c]:
                for dep in range(len(sj["services"][s]["components"][c]["dependencies"])):
                    # Gotcha: We assume that the dependency always points
                    # to the first port exposed!
                    link = sj["services"][s]["components"][c]["dependencies"][dep]["name"]
                    sj["services"][s]["components"][c]["dependencies"][dep]["port"] = portmap[link][0]

    # Print warnings
    if len(warnings):
        sys.stderr.write("\nBe warned:\n")
        for warning in sorted(warnings):
            sys.stderr.write("- %s\n" % warning)
        sys.stderr.write("\n")

    return sj

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert docker-compose YAML into swarm.json')
    parser.add_argument('path', help='YAML file path')
    parser.add_argument('-o', '--overwrite', action="store_true",
        default=False,
        help='Overwrite an existing output file')
    parser.add_argument('-n', '--name', default="", dest="app_name",
        help='Application name (app_name)')
    args = parser.parse_args()
    name_parts = args.path.split(".")
    name_parts[-1] = "json"
    output_name = ".".join(name_parts)

    if args.overwrite == False and os.path.exists(output_name):
        sys.stderr.write("File '%s' already exists, aborting.\n" % output_name)
        sys.exit(1)

    d = load_docker_compose_file(args.path)
    sj = transform(d, args.app_name)

    with open(output_name, "wb") as jsonfile:
        print("Writing result to %s" % output_name)
        jsonfile.write(json.dumps(sj, indent=2, sort_keys=True))

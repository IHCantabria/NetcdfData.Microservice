import toml
import argparse

parser = argparse.ArgumentParser()

# Add a new argument to the parser for major version

parser.add_argument("--major", action="store_true")

# Add a new argument to the parser for minor version

parser.add_argument("--minor", action="store_true")

# Add a new argument to the parser for patch version

parser.add_argument("--patch", action="store_true")

args = parser.parse_args()

# Read version from pyproject.toml

with open("pyproject.toml") as f:
    config = toml.load(f)

version = config["project"]["version"]

# Update major version

if args.major:
    version = version.split(".")

    version[0] = str(int(version[0]) + 1)
    version[1] = "0"
    version[2] = "0"

    version = ".".join(version)

# Update minor version

if args.minor:
    version = version.split(".")

    version[1] = str(int(version[1]) + 1)
    version[2] = "0"

    version = ".".join(version)

# Update patch version

if args.patch:
    version = version.split(".")

    version[2] = str(int(version[2]) + 1)

    version = ".".join(version)

# Write new version to pyproject.toml

config["project"]["version"] = version

with open("pyproject.toml", "w") as f:
    toml.dump(config, f)

# Create a new tag with the new version

import os

os.system("git add pyproject.toml")

os.system("git commit -m 'Bump version to {0}'".format(version))

os.system("git tag -a {0} -m 'Version {0}'".format(version))

os.system("git push --tags")

os.system("git push")



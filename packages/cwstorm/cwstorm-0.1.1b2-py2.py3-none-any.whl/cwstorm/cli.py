import os
import click
import importlib
import json
import yaml
from cwstorm.version import VERSION
from cwstorm.serializers import default, fargo, storm

EXAMPLES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "examples")
EXAMPLE_MODULES_PREFIX = "cwstorm.examples."
GET_JOB_FUNCTION_NAME = "get_job"


EXAMPLE_FILES = os.listdir(EXAMPLES_FOLDER)
MODULE_FILES = [
    file for file in EXAMPLE_FILES if file.endswith(".py") and not file.startswith("__")
]
MODULE_NAMES = [file[:-3] for file in MODULE_FILES]  # Remove the .py extension


########################### MAIN #################################
@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="Print the version and exit.")
def main(ctx, version):
    """Storm Command-line interface."""
    if not ctx.invoked_subcommand:
        if version:
            click.echo(VERSION)
            ctx.exit()
        click.echo(ctx.get_help())
        ctx.exit()


SERIALIZE_HELP = """The structure of serialized DAG. 

default: is a list of nodes and a list of edges. The edges contain source and target pointers to node labels. This is the simplest and easiest to understand. It is also understood by the UI.

storm: The default, is a hierarchical structure where a child node's second and successive parents indicate the child node connection by an object in their tasks array with only the fields 'name' and 'reference', which is set to True. 

fargo (Fucked-around-with Argo) is a list of nodes where each node contains a list of dependencies. The dependencies are the names of the nodes that the node depends on. This is similar to the way that relationships are defined in an ARGO workflow. 
"""

FORMAT_HELP = """The output format. JSON and YAML are implemented. XML is not yet implemented.
"""

EXAMPLE_HELP = """The example job to serialize. The examples are in the storm/examples folder. The examples are python modules that contain a function called get_job that returns a job object.
"""


########################### SERIALIZE #############################
@main.command()
@click.option(
    "-s",
    "--serializer",
    default="default",
    help=SERIALIZE_HELP,
    type=click.Choice(choices=["default", "storm", "fargo"], case_sensitive=False),
)
@click.option(
    "-f",
    "--fmt",
    "--format",
    help=FORMAT_HELP,
    default="json",
    type=click.Choice(choices=["json", "pretty", "yaml", "xml"], case_sensitive=False),
)
@click.option(
    "-x",
    "--example",
    help=EXAMPLE_HELP,
    default="simple",
    type=click.Choice(choices=MODULE_NAMES, case_sensitive=True),
)
@click.argument("output", nargs=1, type=click.Path(exists=False, resolve_path=True))
def serialize(serializer, fmt, example, output):
    """
    Serialize a job to json or yaml.

    Examples:

    # Output json to a file for visualization.

    storm serialize -f json -x frames ~/Desktop/frames.json

    storm serialize -f json -x ass_comp_light -s fargo ~/Desktop/ass_comp_light.json

    # Output yaml to a file for using the the assex job example.

    storm serialize -f yaml -s storm  -x assex  ~/Desktop/assex.yaml

    # ARGO is not yet implemented

    """

    module_name = EXAMPLE_MODULES_PREFIX + example
    module = importlib.import_module(module_name)
    storm_script = getattr(module, GET_JOB_FUNCTION_NAME)
    job = storm_script()

    if serializer == "default":
        serialized = default.serialize(job)
    elif serializer == "storm":
        serialized = storm.serialize(job)
    elif serializer == "fargo":
        serialized = fargo.serialize(job)
    else:
        raise ValueError(f"Unknown serializer: {serializer}")

    if fmt == "json":
        with open(output, "w", encoding="utf-8") as fh:
            json.dump(serialized, fh)
    elif fmt == "pretty":
        with open(output, "w", encoding="utf-8") as fh:
            json.dump(serialized, fh, indent=3)
    elif fmt == "yaml":
        with open(output, "w", encoding="utf-8") as fh:
            yaml.dump(serialized, fh)
    elif fmt == "xml":
        raise NotImplementedError("XML serialization not implemented yet.")
    else:
        raise ValueError(f"Unknown format: {fmt}")

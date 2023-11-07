import csv
from os import path, environ
from argparse import ArgumentParser
from . import get_tags
from .models import Exposure
from dterm.dbt.impact import impact_report

DBT_ROOT = environ.get('DBT_ROOT', '.')
parser = ArgumentParser('dterm', description="""Tools using or creating DBT files and data

""")
parser.add_argument("-b", "--build", default=DBT_ROOT,
                    help="dbt's `target` build directory. "
                         "Used to infer build files")
parser.add_argument("-g", "--graph", required=False,
                    help="gpickle file")
parser.add_argument("-m", "--models",
                    help="models directory of dbt resources")
parser.add_argument("-e", "--exposures",
                    help="exposures directory")
parser.add_argument("--csv",
                    help="CSV to parse into an [exposure]")
parser.add_argument("action",
                    help="""Action to be taken: [impact|tags]
impact: Impact Report, provide a dbt object: model.dave.revenue
""")
parser.add_argument("subject", nargs='?', default=None,
                    help="subject for action "
                         "e.g. model.dave.revenue_daily")
args = parser.parse_args()

graph_file = args.graph or path.join(args.build, "target/graph.gpickle")
modelsdir = args.models or path.join(args.build, "models")
exposure_dir = args.exposures or path.join(args.build, "models")

if args.action == 'impact':
    if args.subject is None:
        raise AssertionError("Provide a subject materialization.")
    impact_report(graph_file, modelsdir, args.subject)

if args.action == 'tags':
    if args.subject is None:
        raise AssertionError("Provide a subject materialization.")
    resource_type, package, name = subject.split('.')
    resource_name = 'dave_saves'
    args = (resource_name, resource_type, package, name)

    get_tags(*args)

if args.csv:
    with open(args.csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        exposures = []
        for line in reader:
            # TODO REMAP HERE
            args = {
                "name": line['Title'],
                "description": line['Description'] + "\n\n" + line['Notes'],
                "sources": [line['Snowflake Data Sources']]
            }
            exposure = Exposure(**args)
            exposures.append(exposure.format())

            # TODO pyyaml
            print(exposure.render())

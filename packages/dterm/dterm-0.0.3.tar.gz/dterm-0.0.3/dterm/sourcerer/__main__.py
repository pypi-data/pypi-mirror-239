from os import path
from argparse import ArgumentParser
from . import sqlmodel, sqlmodels, replace
from dterm.models import SourceYAMLLoader

parser = ArgumentParser(prog='sourcerer', description="forcing dbt sources on SQL")
parser.add_argument('models', default="models",
                    help="path to models dir")
parser.add_argument('--sources', default=None,
                    help="Path to Sources dir")
parser.add_argument("--model",default=None,
                    help="only run one SQL file")
# parser.add_argument('--dest', default=None,
#                     help="SQL destination dir")
parser.add_argument('--dryrun', default=False,
                    help="SQL destination dir")

args = parser.parse_args()

source_dir = args.sources
if source_dir is None:
    source_dir = path.join(args.models, "sources")

# if True:
#     model = sqlmodel(args.models, args.model)
#     # print(dir(model.ctes()))
#     for cte in model.ctes():
#         # print(cte.name)
#         for select in cte.selects:
#             if select == Star:
#                 print('>', cte.name, select.selects()) # str(select).split("AS")[0])
#         # print(dir(cte))
#
#     exit()
SourceYAMLLoader(source_dir)
source_lookup = SourceYAMLLoader(source_dir).sources()

if args.model:
    model = sqlmodel(args.models, args.model)
    for table in model.tables():
        print(table)
    exit()

models = sqlmodels(args.models)
for model in models:
    result = replace(model.filename, model.tables(ignore_errors=True), source_lookup)
    if not args.dryrun:
        print(f"Writing {model.filename}")
        with open(model.filename, 'w') as sqlfile:
            sqlfile.write(result)
    else:
        print(f"Dryrun: {model.filename}")
        print(result)

# implement source and ref functions
# run jinja2 on temp dir
# parse with sqlglot
# slurp source yamls
# replace in orgin dir
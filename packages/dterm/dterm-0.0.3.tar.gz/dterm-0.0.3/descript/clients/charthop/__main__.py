from argparse import ArgumentParser
from . import EmployeeExport


parser = ArgumentParser(description="query employee heirachy using Charthop ")
parser.add_argument("--filename", required=False,
                    default="data/charthop-dave.csv")
parser.add_argument("name")

args = parser.parse_args()

export = EmployeeExport(args.filename)

export.pecking_order()
subs = export.subordinants(args.name)
print(len(subs))
for sub in subs:
    print(sub)

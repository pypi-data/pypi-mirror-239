from argparse import ArgumentParser
from . import charthop


parser = ArgumentParser(description="aggregated data about your coworkers")
parser.add_argument("name",
                    help="name or partial name")

args = parser.parse_args()

for name in charthop(args.name):
    print(name)
    print()

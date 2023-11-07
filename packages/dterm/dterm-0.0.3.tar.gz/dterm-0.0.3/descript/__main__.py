from argparse import ArgumentParser
from importlib import import_module

PACKAGE_FMT = "descript.schema.{}"

ap = ArgumentParser(description="parse data schemas")
ap.add_argument("in_file")
ap.add_argument("--render", default="markdown",
                help="output format to render")
ap.add_argument("--parse", default="ddl")
args = ap.parse_args()

parse = import_module(PACKAGE_FMT.format(args.parse)).parse
render = import_module(PACKAGE_FMT.format(args.render)).render

with open(args.in_file) as fp:
    dbs = parse(fp.read())
    out = render(dbs)
    print(out)

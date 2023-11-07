import networkx as nx
from dataclasses import dataclass

from dterm.models import ExposureLookup


@dataclass
class ImpactReport:
    exposures: list
    other: list


def impact(graph_file, subject):
    g = nx.read_gpickle(graph_file)
    desc = nx.descendants(g, subject)
    other = []
    exposures = []

    for d in desc:
        if d.startswith('exposure'):
            exposures.append(d)
        else:
            other.append(d)
    return ImpactReport(exposures=exposures, other=other)


def impact_report(graph, dir, subject):
    report = impact(graph, subject)
    exp_lookup = ExposureLookup(dir)
    print("=== Impact Report ===")
    print("Exposures: ")
    for exposure in report.exposures:
        print(exposure, end='')
        lookup = exp_lookup.lookup(exposure)
        if lookup and lookup.owner:
            print(f"\t\t{lookup.owner}", end='')
        print()

    print()

    print("Models: ")
    for m in report.other:
        print(m)

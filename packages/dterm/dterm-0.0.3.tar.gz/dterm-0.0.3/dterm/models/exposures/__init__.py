from glob import glob
from yaml import safe_load, scanner
from dataclasses import dataclass
from typing import Optional


@dataclass
class Owner:
    name: str
    email: str

    def __str__(self):
        return f"{self.name} <{self.email}>"


@dataclass(init=False)
class Exposure:
    name: str
    type: Optional[str]
    maturity: Optional[str]
    url: Optional[str]
    description: Optional[str]
    depends_on: Optional[list]
    owner: Optional

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.owner = kwargs.get('owner')
        if self.owner:
            self.owner = Owner(**self.owner)

    def __repr__(self):
        return self.name


class ExposureLookup:
    def __init__(self, dir):
        self.loader = DBTYAMLLoader(dir)
        exposures = self.loader.exposures()
        self.registry = {}

        for exp in exposures:
            key = exp.name.replace(" ", "_").lower()
            self.registry[key] = exp

    def lookup(self, name):
        name = name.split(".")[-1].lower()
        return self.registry.get(name)


class DBTYAMLLoader:
    def __init__(self, dir):
        self.dir = dir

    def exposures(self, recursive=True):
        out = []

        for file in self.yamls(recursive=recursive):
            try:
                data = safe_load(open(file, 'r').read())
                for exposure in data.get('exposures', []):
                    out.append(Exposure(
                        **exposure
                    ))
                    # print(out[-1])
            except scanner.ScannerError as ex:
                raise Exception(f"{file}")
        return out

    def yamls(self, recursive=True):
        """
        returns a lame hash map of tuples
        FQTN -> (source_name, table_name)
        """
        lookup = {}
        for file in glob(self.dir + "/**/*.yml", recursive=recursive):
            yield file
        for file in glob(self.dir + "/**/*.yaml", recursive=recursive):
            yield file

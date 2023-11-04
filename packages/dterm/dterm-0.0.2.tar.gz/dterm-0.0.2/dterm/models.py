from dataclasses import dataclass
from typing import Optional

EXPOSURE_HEADER = """
version: 2

exposures:
"""


@dataclass
class Exposure:
    name: str
    description: str
    sources: list[str]
    type: Optional[str] = "application"

    def format(self):
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "depends_on": self.sources
        }

    def render(self):
        return f"""
- name: {self.name}
  type: {self.type}
  depends_on: 
    - {self.sources}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Cell:
    id: str
    kind: str
    locator: str


@dataclass(frozen=True)
class Stalk:
    cell_id: str
    fields: Mapping[str, Any]
    g_v: bool
    evidence: tuple[str, ...] = ()
    sheaf_role: str = "capability"  # capability | knowledge | conservation


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    shared_fields: tuple[str, ...]
    observed: bool = True


@dataclass
class Sheaf:
    cells: dict[str, Cell]
    stalks: dict[str, Stalk]
    edges: list[Edge]
    package_id: str = ""
    morse_core: frozenset[str] | None = None
    cover_generation: int = 0
    schema: tuple[str, ...] = ()

    def copy(self) -> "Sheaf":
        return Sheaf(
            cells=dict(self.cells),
            stalks=dict(self.stalks),
            edges=list(self.edges),
            package_id=self.package_id,
            morse_core=self.morse_core,
            cover_generation=self.cover_generation,
            schema=self.schema,
        )


@dataclass
class DomainPackage:
    id: str
    cells_from: str
    cover_from: str
    stalk_schema: tuple[str, ...]
    shared_fields: tuple[str, ...]
    mediators: tuple[str, ...]
    critical_lenses: tuple[str, ...]
    soft_lenses: tuple[str, ...]
    oracle: str
    grain_min: int = 2
    grain_max: int = 10_000
    min_observed_edges: int = 1
    grain: str = ""
    three_sheaves: dict[str, str] = field(default_factory=dict)
    forbidden: tuple[str, ...] = ()


@dataclass
class GlueReport:
    phi: bool
    g_v_ok: bool
    restrictions_ok: bool
    mismatches: list[dict[str, Any]]
    h1_vanishes_linear: bool
    oracle_ran: bool
    oracle_ok: bool
    morse_core: tuple[str, ...]
    notes: list[str] = field(default_factory=list)
    critical_ok: bool = True
    soft_score: float | None = None

    @property
    def write_allowed(self) -> bool:
        return bool(self.phi and self.oracle_ran and self.oracle_ok and self.critical_ok)

"""sheaf-port: domain-agnostic capability/knowledge sheaf runtime for agent harnesses."""

from .types import Cell, Edge, Stalk, Sheaf, DomainPackage, GlueReport
from .package import load_package, validate_package, PackageError
from .bind import bind, BindError
from .kernel import instantiate, KernelError
from .glue import evaluate_phi, may_commit
from .repair import repair, RepairError
from .morse import reduce as morse_reduce, MorseError
from .harness import run_loop
from .validate_skills import validate_plugin

__version__ = "0.1.0"

__all__ = [
    "Cell",
    "Edge",
    "Stalk",
    "Sheaf",
    "DomainPackage",
    "GlueReport",
    "load_package",
    "validate_package",
    "PackageError",
    "bind",
    "BindError",
    "instantiate",
    "KernelError",
    "evaluate_phi",
    "may_commit",
    "repair",
    "RepairError",
    "morse_reduce",
    "MorseError",
    "run_loop",
    "validate_plugin",
]

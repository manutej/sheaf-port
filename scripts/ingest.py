#!/usr/bin/env python3
"""Walk a folder. Emit a typed index, a lattice JSON, and a reusable package.

Stdlib only. This is the out-of-box path:

    python scripts/ingest.py path/to/folder --out ./out

Reads .py (ast), .md (links), .ts/.js/.tsx/.jsx (import regex).
Keeps a link only when the source shows an import or a markdown link.
Teal = the target was found in the folder.
Terracotta = the import or link does not resolve (dangling).
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "node_modules",
    "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".turbo",
}
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]]+)\]\]")
JS_FROM = re.compile(r"(?:import|from)\s+['\"]([^'\"]+)['\"]")
JS_EXPORT = re.compile(
    r"export\s+(?:async\s+)?(?:default\s+)?(?:class|function|const|type|interface|enum)\s+([A-Za-z_$][\w$]*)"
)
CAP = 120


def iter_files(root: Path, suffixes: set[str]) -> list[Path]:
    out = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else path.stem


def ingest(root: Path, cap: int = CAP) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a folder: {root}")

    py = iter_files(root, {".py"})
    md = iter_files(root, {".md"})
    js = iter_files(root, {".ts", ".tsx", ".js", ".jsx"})

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    skipped: list[str] = []
    aliases: dict[str, str] = {}

    def add_node(nid: str, **kw):
        if nid in nodes:
            return
        if len(nodes) >= cap:
            skipped.append(f"cap {cap}: dropped {nid}")
            return
        nodes[nid] = kw

    def add_edge(src: str, dst: str, evidence: str, dangling: bool):
        if src == dst:
            return
        edges.append(
            {
                "source": src,
                "target": dst,
                "relation": "dangling-import" if dangling else "import",
                "restrictKind": "projection",
                "residual": 1.0 if dangling else 0.0,
                "note": "target not in this folder" if dangling else "resolved import or link",
                "evidence": evidence,
            }
        )

    for path in py:
        rel = path.relative_to(root).as_posix()
        mod = module_name(path, root)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
        except SyntaxError as exc:
            skipped.append(f"{rel}: {exc}")
            continue
        mid = f"mod:{mod}"
        add_node(
            mid,
            id=mid,
            title=rel,
            kind="module",
            level=2 if "test" in rel else 0,
            dim=3,
            known=True,
            section=[1.0, 1.0, 1.0],
            summary=f"Python module {mod}",
            locator=f"{rel}:0",
            path=rel,
            symbol=mod,
            module=mod,
        )
        aliases[mod] = mid
        aliases[path.stem] = mid
        aliases[mod.split(".")[-1]] = mid
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                cid = f"{mod}.{node.name}"
                add_node(
                    cid,
                    id=cid,
                    title=node.name,
                    kind="symbol",
                    level=2 if "test" in rel else 1,
                    dim=3,
                    known=False,
                    section=[1.0, 1.0, 1.0],
                    summary=f"{type(node).__name__} in {rel}:{node.lineno}",
                    locator=f"{rel}:{node.lineno}",
                    path=rel,
                    symbol=node.name,
                    module=mod,
                )
                aliases[node.name] = aliases.get(node.name, cid)
                aliases[cid] = cid
                aliases[f"{path.stem}.{node.name}"] = cid

    for path in py:
        rel = path.relative_to(root).as_posix()
        mod = module_name(path, root)
        src = aliases.get(mod)
        if not src:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            specs: list[tuple[str, str | None]] = []
            if isinstance(node, ast.Import):
                for alias in node.names:
                    specs.append((alias.name, None))
            elif isinstance(node, ast.ImportFrom) and node.module:
                specs.append((node.module, None))
                for alias in node.names:
                    specs.append((node.module, alias.name))
            for module, name in specs:
                if name:
                    dst = (
                        aliases.get(f"{module}.{name}")
                        or aliases.get(f"{module.split('.')[-1]}.{name}")
                        or aliases.get(name)
                    )
                    evidence = f"{rel}: from {module} import {name}"
                    target_label = f"{module}.{name}"
                else:
                    dst = aliases.get(module) or aliases.get(module.split(".")[-1])
                    evidence = f"{rel}: import {module}"
                    target_label = module
                if dst == src:
                    continue
                if dst:
                    add_edge(src, dst, evidence, dangling=False)
                else:
                    miss = f"missing:{target_label}"
                    add_node(
                        miss,
                        id=miss,
                        title=target_label,
                        kind="missing",
                        level=3,
                        dim=3,
                        known=False,
                        section=[0.0, 0.0, 0.0],
                        summary=f"import not found in {root.name}",
                        locator=f"{rel}:import",
                        path="",
                        symbol=name or module,
                        module=module,
                    )
                    add_edge(src, miss, evidence + " (dangling)", dangling=True)

    for path in md:
        rel = path.relative_to(root).as_posix()
        title = path.stem
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        nid = f"page:{rel}"
        add_node(
            nid,
            id=nid,
            title=title,
            kind="page",
            level=0,
            dim=2,
            known=True,
            section=[1.0, 1.0],
            summary=rel,
            locator=rel,
            path=rel,
            symbol=title,
            module="",
        )
        aliases[rel] = nid
        aliases[path.name] = nid
        aliases[path.stem] = nid
        aliases[title.lower()] = nid

    page_ids = {n["id"]: n for n in nodes.values() if n.get("kind") == "page"}
    for path in md:
        rel = path.relative_to(root).as_posix()
        src = aliases.get(rel)
        text = path.read_text(encoding="utf-8", errors="replace")
        targets = [m.group(2) for m in MD_LINK.finditer(text)] + [
            m.group(1).split("|")[0].strip() for m in WIKI_LINK.finditer(text)
        ]
        for raw in targets:
            target = raw.split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            dst = aliases.get(target) or aliases.get(Path(target).name) or aliases.get(Path(target).stem)
            evidence = f"{rel}: link {raw}"
            if dst:
                add_edge(src, dst, evidence, dangling=False)
            else:
                miss = f"missing:{target}"
                add_node(
                    miss,
                    id=miss,
                    title=target,
                    kind="missing",
                    level=3,
                    dim=2,
                    known=False,
                    section=[0.0, 0.0],
                    summary="markdown link with no file in this folder",
                    locator=f"{rel}:link",
                    path="",
                    symbol=target,
                    module="",
                )
                add_edge(src, miss, evidence + " (dangling)", dangling=True)

    for path in js:
        rel = path.relative_to(root).as_posix()
        mid = f"js:{rel}"
        add_node(
            mid,
            id=mid,
            title=rel,
            kind="module",
            level=0,
            dim=3,
            known=True,
            section=[1.0, 1.0, 1.0],
            summary=f"JS/TS file {rel}",
            locator=f"{rel}:0",
            path=rel,
            symbol=path.stem,
            module=rel,
        )
        aliases[rel] = mid
        aliases["./" + rel] = mid
        aliases[path.stem] = mid
        text = path.read_text(encoding="utf-8", errors="replace")
        for name in JS_EXPORT.findall(text):
            cid = f"{rel}:{name}"
            add_node(
                cid,
                id=cid,
                title=name,
                kind="symbol",
                level=1,
                dim=3,
                known=False,
                section=[1.0, 1.0, 1.0],
                summary=f"export {name} in {rel}",
                locator=rel,
                path=rel,
                symbol=name,
                module=rel,
            )
        for spec in JS_FROM.findall(text):
            if spec.startswith("."):
                dest_path = (path.parent / spec).resolve()
                # try with extensions
                dest = None
                for ext in ("", ".ts", ".tsx", ".js", ".jsx", "/index.ts", "/index.js"):
                    cand = Path(str(dest_path) + ext) if ext and not dest_path.suffix else dest_path
                    try:
                        rel_c = cand.relative_to(root.resolve()).as_posix()
                    except ValueError:
                        continue
                    dest = aliases.get(rel_c)
                    if dest:
                        break
                evidence = f"{rel}: import {spec}"
                if dest:
                    add_edge(mid, dest, evidence, dangling=False)
                else:
                    miss = f"missing:{spec}"
                    add_node(
                        miss,
                        id=miss,
                        title=spec,
                        kind="missing",
                        level=3,
                        dim=3,
                        known=False,
                        section=[0.0, 0.0, 0.0],
                        summary="relative import not found",
                        locator=f"{rel}:import",
                        path="",
                        symbol=spec,
                        module=spec,
                    )
                    add_edge(mid, miss, evidence + " (dangling)", dangling=True)
            # package imports stay off the lattice — they are not in this folder

    kind = "mixed"
    if py and not md and not js:
        kind = "codebase"
    elif md and not py and not js:
        kind = "wiki"
    elif js and not py and not md:
        kind = "codebase"

    # Dedup edges
    seen = set()
    dedup = []
    for e in edges:
        k = (e["source"], e["target"], e["relation"])
        if k in seen:
            continue
        if e["source"] not in nodes or e["target"] not in nodes:
            continue
        seen.add(k)
        dedup.append(e)

    teal = sum(1 for e in dedup if e["residual"] == 0)
    terra = sum(1 for e in dedup if e["residual"] > 0)
    lattice = {
        "id": re.sub(r"[^a-z0-9._-]+", "-", root.name.lower()) or "folder",
        "title": f"{root.name} index",
        "kicker": f"{len(nodes)} parts · {len(dedup)} observed links · {teal} teal · {terra} terracotta",
        "blurb": (
            f"Typed index of {root}. A node is a module, symbol, or page you can open. "
            "Teal = the import or link resolves inside this folder. "
            "Terracotta = it does not."
        ),
        "residualMeaning": (
            "The import or markdown link on the left does not resolve to a file or symbol in this folder."
        ),
        "levels": [
            {"id": 0, "label": "Modules / pages"},
            {"id": 1, "label": "Symbols"},
            {"id": 2, "label": "Tests"},
            {"id": 3, "label": "Missing targets"},
        ],
        "nodes": [
            {
                "id": n["id"],
                "title": n["title"],
                "kind": n["kind"],
                "level": n["level"],
                "dim": n["dim"],
                "known": n["known"],
                "section": n["section"],
                "summary": n["summary"],
            }
            for n in nodes.values()
        ],
        "edges": [
            {
                "source": e["source"],
                "target": e["target"],
                "relation": e["relation"],
                "restrictKind": e["restrictKind"],
                "residual": e["residual"],
                "note": e["note"],
                "evidence": e["evidence"],
            }
            for e in dedup
        ],
        "rebuild": {
            "command": f"python scripts/ingest.py {root} --out ./out",
            "kind": kind,
            "shared_fields": ["path", "symbol", "module"],
        },
    }
    package = {
        "id": kind,
        "source": {"locator": str(root)},
        "site": {
            "cells_from": "python symbols, markdown pages, js/ts files",
            "cover_from": "observed imports and markdown links",
            "grain": "symbol-or-page",
        },
        "restriction": {"shared_fields": ["path", "symbol", "module"]},
        "rebuild": f"python scripts/ingest.py {root} --out ./out",
        "parts": len(nodes),
        "links": len(dedup),
        "teal": teal,
        "terracotta": terra,
    }
    return {
        "kind": kind,
        "root": str(root),
        "nodes": len(nodes),
        "edges": len(dedup),
        "teal": teal,
        "terracotta": terra,
        "skipped": skipped,
        "lattice": lattice,
        "package": package,
    }


def write_bundle(result: dict, out: Path) -> dict[str, str]:
    out.mkdir(parents=True, exist_ok=True)
    lattice_path = out / "lattice.json"
    package_path = out / "domain.package.yaml"
    structure_path = out / "STRUCTURE.md"
    index_path = out / "index.json"
    lattice_path.write_text(json.dumps(result["lattice"], indent=2) + "\n")
    index_path.write_text(json.dumps({
        "kind": result["kind"],
        "root": result["root"],
        "parts": result["nodes"],
        "links": result["edges"],
        "teal": result["teal"],
        "terracotta": result["terracotta"],
        "skipped": result["skipped"],
    }, indent=2) + "\n")
    pkg = result["package"]
    package_path.write_text(
        "\n".join(
            [
                f"id: {pkg['id']}",
                "source:",
                f"  locator: {pkg['source']['locator']}",
                "site:",
                f"  cells_from: {pkg['site']['cells_from']}",
                f"  cover_from: {pkg['site']['cover_from']}",
                f"  grain: {pkg['site']['grain']}",
                "restriction:",
                "  shared_fields: [path, symbol, module]",
                f"rebuild: {pkg['rebuild']}",
                f"parts: {pkg['parts']}",
                f"links: {pkg['links']}",
                f"teal: {pkg['teal']}",
                f"terracotta: {pkg['terracotta']}",
                "",
            ]
        )
    )
    skipped = result["skipped"] or ["none"]
    structure_path.write_text(
        f"""# Structure — {Path(result['root']).name}

Reusable index of `{result['root']}`.

- Kind: `{result['kind']}`
- Parts: {result['nodes']}
- Observed links: {result['edges']}
- Teal (resolves): {result['teal']}
- Terracotta (dangling): {result['terracotta']}
- Rebuild: `python scripts/ingest.py {result['root']} --out ./out`

A part is a module, function, class, or page with a locator you can open.
A link exists only if an import or markdown link was in the source.
Teal means that target was found in this folder.
Terracotta means it was not — open the `evidence` field on the edge.

Dropped this run:
"""
        + "\n".join(f"- {s}" for s in skipped)
        + "\n"
    )
    return {
        "lattice": str(lattice_path),
        "package": str(package_path),
        "structure": str(structure_path),
        "index": str(index_path),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Take a folder and build a sheaf / lattice / reusable package.")
    p.add_argument("folder")
    p.add_argument("--out", default="out")
    p.add_argument("--cap", type=int, default=CAP)
    args = p.parse_args(argv)
    result = ingest(Path(args.folder), cap=args.cap)
    paths = write_bundle(result, Path(args.out))
    print(json.dumps({
        "kind": result["kind"],
        "parts": result["nodes"],
        "links": result["edges"],
        "teal": result["teal"],
        "terracotta": result["terracotta"],
        "skipped": result["skipped"],
        "files": paths,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

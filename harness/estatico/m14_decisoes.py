"""M14 (parte D) — selecao das decisoes (harness/regras.md §1) e checks estaticos.

Selecao: cada item de lista/frase das secoes de decisao tecnica que cumpra TODAS as condicoes:
 1. verbo de prescricao ou de fato (use, must, should, will, never, always, implements,
    implemented with, lives in, goes through, add, keep, placed in ...);
 2. >= 1 identificador concreto: pacote (`nome` com a palavra 'package' na frase, ou listado
    no pubspec), classe com sufixo Bloc/Cubit/Repository/UseCase/Service/DataSource/Failure/
    Client/Store (ou `Impl`), ou caminho `lib/...`;
 3. refere-se a codigo de lib/ (caminho `lib/` ou classe/pacote de lib/), nao a processo/docs/testes;
 4. nao repete restricao do pacote de entrada P8 (flutter_bloc, Clean Architecture, fpdart/Either,
    mocktail, whisper_ggml, design_tokens, convencao de pastas, iOS).
Ordem: constitution, depois plan.md da F000 (Ciclo A); deduplicadas (candidata cujo conjunto de identificadores e igual a,
ou subconjunto de, o de outra ja aceita conta uma vez); ficam as 10 primeiras. < 8 candidatas: entram todas e o
numero e registrado.

Verificacao estatica (parte D) so quando a decisao vira check:
 - 'X must never import Y' -> o arquivo que declara X nao importa o que declara Y;
 - caminho/classe/pacote ('use', 'lives in', 'implements', 'goes through', 'add', 'keep' + identificador)
   -> existencia em lib/ (arquivo/pasta), declaracao da classe e, para pacote, entrada no pubspec;
 - demais (comportamento) -> `juiz` (parte J, fora deste modulo).
Cada decisao sai com `esperado`: ok | falha | juiz.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from .common import app_name, dart_files, dump, imports_of, mask_dart, read, rel, resolve_import, tag_copy

# D-109: "ou equivalentes" (regras.md §1) = verbos de escolha, posse e fato tecnico que os documentos reais usam
# (chosen, fixed, owns, exposes, returns, persists, imports, binds, is/are, via ...); mesma lista nos dois ciclos.
VERBOS = re.compile(r"\b(use[sd]?|using|must|should|will|shall|never|always|implements?|implemented\s+with|lives?\s+in|goes\s+through|"
                    r"placed\s+in|add|keep|is\s+implemented|chosen|fixed|selected|adopted|owns?|exposes?|returns?|persists?|"
                    r"imports?|binds?|prevents?|covered|is|are|via|only)\b", re.I)
# D-109: o nome de classe com sufixo conta com ou sem crases (regras.md §1 nao exige crases)
CLASSE_RE = re.compile(r"`?\b([A-Z][A-Za-z0-9]*(?:Bloc|Cubit|Repository|UseCase|Service|DataSource|Failure|Client|Store|Impl))\b`?")
CLASSE_FREE_RE = re.compile(r"`([A-Z][A-Za-z0-9]+)`")
PATH_RE = re.compile(r"`?(lib/[A-Za-z0-9_/\.]*)`?")
PKG_RE = re.compile(r"`([a-z][a-z0-9_]+)`")
P8_RE = re.compile(r"flutter_bloc|clean architecture|fpdart|\bEither\b|mocktail|whisper_ggml|design_tokens|convention|convencao|\bios\b", re.I)


def _itens(md):
    """Itens de lista e frases de paragrafos, cada um com o texto original."""
    out = []
    for linha in md.splitlines():
        t = linha.strip()
        if not t or t.startswith("#") or t.startswith("|"):
            continue
        t = re.sub(r"^([-*]|\d+\.)\s+", "", t)
        for frase in re.split(r"(?<=[.;])\s+(?=[A-Z`])", t):
            if frase.strip():
                out.append(frase.strip())
    return out


def _ids(frase, pkgs_pubspec):
    ids = set(CLASSE_RE.findall(frase))
    paths = {p.rstrip("/.") for p in PATH_RE.findall(frase) if len(p) > 4}
    ids |= paths
    if re.search(r"package|dependency|pub", frase, re.I):
        ids |= set(PKG_RE.findall(frase))
    ids |= {p for p in PKG_RE.findall(frase) if p in pkgs_pubspec}
    return ids


def selecionar(constitution_md, plan_md, pubspec_text="", maximo=10):
    pkgs = set(re.findall(r"^\s{2}([a-z0-9_]+):", pubspec_text, re.M))
    cands, excl = [], []
    for fonte, md in (("constitution", constitution_md), ("plan", plan_md)):
        for frase in _itens(md):
            ids = _ids(frase, pkgs)
            if not VERBOS.search(frase) or not ids:
                excl.append((frase, "sem verbo de prescricao ou sem identificador"))
                continue
            if not (any(i.startswith("lib/") for i in ids) or CLASSE_RE.search(frase) or any(i in pkgs or re.search("package|dependency|pub", frase, re.I) for i in ids if not i.startswith("lib/"))):
                excl.append((frase, "nao e codigo de lib/"))
                continue
            if P8_RE.search(frase):
                excl.append((frase, "repete restricao do P8"))
                continue
            if any(ids <= c["ids"] or c["ids"] <= ids for c in cands):
                excl.append((frase, "duplicada"))
                continue
            cands.append({"fonte": fonte, "texto": frase, "ids": ids})
    sel = cands[:maximo]
    return sel, {"total_candidatas": len(cands), "excluidas": excl, "menos_de_8": len(cands) < 8}


def _declaracoes(root):
    decl = {}
    for f in dart_files(root):
        for m in re.finditer(r"\b(?:abstract\s+|sealed\s+|base\s+|final\s+)*class\s+(\w+)", mask_dart(read(f))):
            decl[m.group(1)] = rel(root, f)
    return decl


def verificar(decisao, root):
    frase, ids = decisao["texto"], decisao["ids"]
    app, decl = app_name(root), _declaracoes(root)
    pubspec = read(Path(root) / "pubspec.yaml")
    m = re.search(r"`(\w+)`\s+(?:must\s+)?never\s+import[s]?\s+`(\w+)`", frase, re.I)
    if m:
        a, b = m.groups()
        if a not in decl or b not in decl:
            return "falha", f"{a if a not in decl else b} nao declarada"
        fa = decl[a]
        for linha, uri in imports_of(read(Path(root) / fa)):
            k, t = resolve_import(root, fa, uri, app)
            if k == "int" and t == decl[b]:
                return "falha", f"{fa}:{linha} importa {t}"
        return "ok", "sem import"
    if re.search(r"\b(sorted|rounded|ordered|returns?|retries|calculat)\w*", frase, re.I) and not re.search(r"\b(use[sd]?|implements?|lives?\s+in|goes\s+through|add|keep)\b", frase, re.I):
        return "juiz", "comportamento"
    faltam = []
    for i in sorted(ids):
        if i.startswith("lib/"):
            if not (Path(root) / i).exists():
                faltam.append(i)
        elif i[0].isupper():
            if i not in decl:
                faltam.append(i)
        elif not re.search(rf"^\s{{2}}{re.escape(i)}:", pubspec, re.M):
            faltam.append(i)
    if re.search(r"\b(use[sd]?|using|implements?|lives?\s+in|goes\s+through|add|keep|placed\s+in|chosen|selected|adopted|owns?|exposes?)\b", frase, re.I):
        return ("falha", "ausentes: " + ", ".join(faltam)) if faltam else ("ok", "identificadores presentes")
    return "juiz", "sem check estatico aplicavel"


def analisar(root, constitution_path, plan_path, maximo=10):
    sel, meta = selecionar(read(constitution_path), read(plan_path), read(Path(root) / "pubspec.yaml"), maximo)
    itens = []
    for n, d in enumerate(sel, 1):
        v, ev = verificar(d, root)
        itens.append({"ordem": n, "fonte": d["fonte"], "texto": d["texto"], "identificadores": sorted(d["ids"]),
                      "estatica": v != "juiz", "esperado": v, "evidencia": ev})
    estaticas = [i for i in itens if i["estatica"]]
    return {"decisoes": itens, "total_selecionadas": len(itens), "total_candidatas": meta["total_candidatas"],
            "menos_de_8": meta["menos_de_8"], "estaticas_ok": sum(1 for i in estaticas if i["esperado"] == "ok"),
            "estaticas_total": len(estaticas), "para_o_juiz": sum(1 for i in itens if not i["estatica"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--constitution", required=True, help="caminho relativo a raiz da tag")
    ap.add_argument("--plan", required=True)
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(analisar(root, Path(root) / a.constitution, Path(root) / a.plan))


if __name__ == "__main__":
    main()

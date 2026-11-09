"""M15 — consistencia de padroes entre features (regras C1..C4 de harness/regras.md §2).

Referencia: a feature que implementa o RF01 (`--ref-feature`, ou detectada por
`detectar_ref` = feature de `lib/features/<x>/` que mais recebeu arquivos entre a tag
anterior ao RF01 e `rf01-done`). O padrao e extraido da referencia NA TAG DE REFERENCIA;
as demais features sao comparadas NA TAG `final`.

Contagem (interpretacao registrada nas notas — o texto diz 'divergencia' sem fixar a unidade):
- C1: por camada (data/domain/presentation), |subpastas_ref (simetrica) subpastas_feature|
      (cada subpasta presente so de um lado = 1);
- C2: cada implementacao `X implements YRepository` cuja relacao de nomes (sufixo de X sobre
      Y) difere da relacao da referencia = 1;
- C3: cada classe `extends *Failure` cujo (ultima palavra do nome, classe-base) difere do
      padrao da referencia = 1;
- C4: |papeis_ref (simetrica) papeis_feature| com papeis = {bloc, cubit, event, state} dos
      arquivos de presentation, + 1 por arquivo `x_<papel>.dart` que nao declara a classe
      `Camel(x)+Papel`.
Convencao 'respeitada' = zero divergencias nela. Feature sem camada: so conta nas convencoes
afetadas (as subpastas da camada ausente contam em C1).
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from .common import dart_files, dump, git, mask_dart, read, tag_copy

LAYERS = ("data", "domain", "presentation")
ROLES = ("bloc", "cubit", "event", "state")
IMPL_RE = re.compile(r"class\s+(\w+)\s+implements\s+(\w+Repository)\b")
FAIL_RE = re.compile(r"class\s+(\w+)\s+extends\s+(\w*Failure)\b")


def _camel(snake):
    return "".join(p.capitalize() for p in snake.split("_"))


def _ult_palavra(name):
    return re.findall(r"[A-Z][a-z0-9]*", name)[-1] if re.findall(r"[A-Z][a-z0-9]*", name) else name


def features(root):
    base = Path(root) / "lib" / "features"
    return sorted(p.name for p in base.iterdir() if p.is_dir()) if base.exists() else []


def extrair(root, feat):
    fdir = Path(root) / "lib" / "features" / feat
    subs = {l: set() for l in LAYERS}
    impls, fails, papeis, nomes_ruins = [], [], set(), 0
    for f in sorted(fdir.rglob("*.dart")):
        rel = f.relative_to(fdir).parts
        if len(rel) >= 3 and rel[0] in LAYERS:
            subs[rel[0]].add(rel[1])
        code = mask_dart(read(f))
        for m in IMPL_RE.finditer(code):
            impl, abstract = m.group(1), m.group(2)
            relacao = impl[len(abstract):] if impl.startswith(abstract) else f"<{impl}>"
            impls.append((impl, relacao))
        for m in FAIL_RE.finditer(code):
            fails.append((m.group(1), (_ult_palavra(m.group(1)), m.group(2))))
        if rel and rel[0] == "presentation":
            mm = re.match(r"(.+)_(bloc|cubit|event|state)\.dart$", f.name)
            if mm:
                papeis.add(mm.group(2))
                esperado = _camel(mm.group(1)) + mm.group(2).capitalize()
                if not re.search(r"\bclass\s+" + esperado + r"\b", code):
                    nomes_ruins += 1
    return {"subpastas": subs, "impls": impls, "falhas": fails, "papeis": papeis, "nomes_ruins": nomes_ruins}


def _padrao(lista):
    c = Counter(r for _, r in lista)
    return c.most_common(1)[0][0] if c else None


def comparar(ref, feat):
    c1 = sum(len(ref["subpastas"][l] ^ feat["subpastas"][l]) for l in LAYERS)
    pref = _padrao(ref["impls"])
    c2 = sum(1 for _, r in feat["impls"] if pref is not None and r != pref)
    ffref = _padrao(ref["falhas"])
    c3 = sum(1 for _, r in feat["falhas"] if ffref is not None and r != ffref)
    c4 = len(ref["papeis"] ^ feat["papeis"]) + feat["nomes_ruins"]
    d = {"C1": c1, "C2": c2, "C3": c3, "C4": c4}
    d["total"] = sum(d.values())
    d["respeitadas"] = sum(1 for k in ("C1", "C2", "C3", "C4") if d[k] == 0)
    return d


def detectar_ref(repo, tag_anterior, tag_rf01):
    c = Counter()
    for l in git(repo, "diff", "--name-only", "--diff-filter=A", tag_anterior, tag_rf01).splitlines():
        m = re.match(r"lib/features/([^/]+)/", l)
        if m:
            c[m.group(1)] += 1
    return c.most_common(1)[0][0] if c else None


def analisar(root_ref, root_final, ref_feature):
    ref = extrair(root_ref, ref_feature)
    por_feature = {f: comparar(ref, extrair(root_final, f)) for f in features(root_final) if f != ref_feature}
    return {"referencia": ref_feature, "por_feature": por_feature,
            "M15_divergencias": sum(v["total"] for v in por_feature.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref-tag", required=True, help="tag rf01-done")
    ap.add_argument("--tag", required=True, help="tag final")
    ap.add_argument("--ref-feature")
    ap.add_argument("--tag-anterior-rf01", help="para detectar a feature de referencia")
    a = ap.parse_args()
    ref = a.ref_feature or detectar_ref(a.repo, a.tag_anterior_rf01, a.ref_tag)
    with tag_copy(a.repo, a.ref_tag) as r1, tag_copy(a.repo, a.tag) as r2:
        dump(analisar(r1, r2, ref))


if __name__ == "__main__":
    main()

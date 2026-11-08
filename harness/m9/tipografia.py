"""H-003 — introspeccao tipografica (M9, parte D).

Injeta em UMA COPIA temporaria da tag um teste de widget que monta o widget indicado,
percorre a arvore (todos os RichText) e extrai `fontFamily` e `fontSize` efetivos de cada
texto; compara com os tokens (familias e tamanhos permitidos, da §4 do doc-prototipo.md).
O resultado vai para um arquivo temporario fora do repositorio.

Uso (calibracao): python3 -m harness.m9.tipografia --repo <repo> --tag v1 \\
    --import "package:cal_app/features/entries/presentation/pages/entries_page.dart" \\
    --widget "const EntriesPage()" --tokens calibracao/tokens.json

Nos ciclos (Parte IV) o `--widget` e o ponto de entrada de cada estado da M9; o tema do app
(real) e que deveria definir a familia padrao: `--familia-padrao` so e usada na calibracao.
Tokens reais: ainda nao extraidos (doc-prototipo.md fica em `entrada/`, ausente neste checkout);
as familias visiveis no HTML do prototipo sao Karla, IBM Plex Mono e Fraunces.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from harness.estatico.common import dump, flutter_bin, flutter_env, tag_copy

TMPL = Path(__file__).with_name("tipografia_test.dart.tmpl")


def extrair(root, imports, widget, familia_padrao, timeout=600):
    imps = "\n".join(f"import '{i}';" for i in imports)
    corpo = TMPL.read_text().replace("{{IMPORTS}}", imps).replace("{{WIDGET}}", widget).replace("{{FAMILIA_PADRAO}}", familia_padrao)
    (Path(root) / "test").mkdir(exist_ok=True)
    alvo = Path(root) / "test" / "_harness_tipografia_test.dart"
    alvo.write_text(corpo)
    with tempfile.TemporaryDirectory(prefix="harness-out-") as out_dir:
        saida = Path(out_dir) / "tipografia.json"
        env = flutter_env()
        env["HARNESS_OUT"] = str(saida)
        subprocess.run([flutter_bin(), "pub", "get"], cwd=root, capture_output=True, text=True, env=env, timeout=timeout)
        p = subprocess.run([flutter_bin(), "test", "--no-pub", "test/_harness_tipografia_test.dart"], cwd=root,
                           capture_output=True, text=True, env=env, timeout=timeout)
        if not saida.exists():
            raise RuntimeError("introspeccao falhou: " + (p.stdout[-600:] + p.stderr[-300:]))
        return json.loads(saida.read_text())


def comparar(textos, tokens):
    fams, tams = set(tokens["fontFamilies"]), {float(x) for x in tokens["fontSizes"]}
    viol = []
    for t in textos:
        motivos = []
        if t["fontFamily"] not in fams:
            motivos.append("familia")
        if t["fontSize"] is None or float(t["fontSize"]) not in tams:
            motivos.append("tamanho")
        if motivos:
            viol.append({**t, "motivos": motivos})
    return {"M9_tipografia_textos": len(textos), "M9_tipografia_fora_do_token": len(viol), "violacoes": viol}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--import", dest="imports", action="append", required=True)
    ap.add_argument("--widget", required=True)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--familia-padrao", default="Inter")
    a = ap.parse_args()
    tokens = json.loads(Path(a.tokens).read_text())
    with tag_copy(a.repo, a.tag) as root:
        dump(comparar(extrair(root, a.imports, a.widget, a.familia_padrao), tokens))


if __name__ == "__main__":
    main()

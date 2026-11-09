from pathlib import Path

from harness.estatico import m14_decisoes as m14
from harness.estatico.common import tag_copy


def test_m14_calibracao(repo, gab):
    g = gab["m14"]
    with tag_copy(repo, "v2") as root:
        r = m14.analisar(root, Path(root) / ".specify/memory/constitution.md", Path(root) / "specs/001-entries/plan.md")
    assert r["total_candidatas"] == g["total_candidatas"] and r["menos_de_8"] is True
    assert len(r["decisoes"]) == len(g["decisoes"])
    for d, e in zip(r["decisoes"], g["decisoes"]):
        assert d["ordem"] == e["ordem"] and e["id_principal"] in d["texto"], (d["texto"], e)
        assert (d["estatica"], d["esperado"]) == (e["estatica"], e["esperado"]), d


def test_m14_regras_de_selecao():
    const = ("- Use `flutter_bloc` for state management.\n- Tests should be written first.\n"
             "- `FooBloc` must never import `BarBloc` (see `lib/features/a/bloc.dart`).\n- Document in `docs/x.md`.\n")
    sel, meta = m14.selecionar(const, "")
    assert [s["texto"][:12] for s in sel] == ["`FooBloc` mu"] and meta["total_candidatas"] == 1


def test_m14_maximo_dez():
    linhas = "\n".join(f"- Use `Foo{i}Service` in `lib/f{i}.dart`." for i in range(15))
    sel, meta = m14.selecionar(linhas, "")
    assert len(sel) == 10 and meta["total_candidatas"] == 15 and meta["menos_de_8"] is False

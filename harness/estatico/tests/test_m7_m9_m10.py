from harness.estatico import m7_camadas, m9_hardcodes, m10_either
from harness.estatico.common import tag_copy


def _pares(lst, *chaves):
    return sorted(tuple(x[k] for k in chaves) for x in lst)


def test_m7_v1(repo, gab):
    with tag_copy(repo, "v1") as root:
        r = m7_camadas.analisar(root)
    esp = gab["m7"]["v1"]
    assert _pares(r["M7"], "arquivo", "linha", "regra") == _pares(esp, "arquivo", "linha", "regra")
    assert _pares(r["rf07_bloc_importa_bloc"], "arquivo", "linha") == _pares(gab["estruturais"]["rf07_bloc_importa_bloc"], "arquivo", "linha")
    assert _pares(r["rf10_chat_importa_entradas"], "arquivo", "linha") == _pares(gab["estruturais"]["rf10_chat_importa_entradas"], "arquivo", "linha")


def test_m7_v2_novas(repo, gab):
    with tag_copy(repo, "v1") as a, tag_copy(repo, "v2") as b:
        r1, r2 = m7_camadas.analisar(a), m7_camadas.analisar(b)
    assert _pares(r2["M7"], "arquivo", "linha", "regra") == _pares(gab["m7"]["v2"], "arquivo", "linha", "regra")
    novas = {(v["arquivo"], v["linha"]) for v in r2["M7"]} - {(v["arquivo"], v["linha"]) for v in r1["M7"]}
    assert len(novas) == gab["m7"]["m7_novas_v2"]


def test_m9_hardcodes(repo, gab):
    for tag in ("v1", "v2"):
        with tag_copy(repo, tag) as root:
            r = m9_hardcodes.analisar(root)
        assert _pares(r["ocorrencias"], "arquivo", "linha", "tipo") == _pares(gab["m9_hardcodes"]["v1"], "arquivo", "linha", "tipo")
        assert r["M9_hardcodes"] == 4


def test_m9_ignora_comentarios_strings_e_tokens():
    src = ("// Color(0xFF000000) fontSize: 99\n"
           "final a = 'fontSize: 12 Color(0xFF111111)';\n"
           "final b = \"\"\"EdgeInsets.all(9)\n\"\"\";\n"
           "x(padding: EdgeInsets.all(AppSpacing.md), s: SizedBox(height: AppSpacing.sm), z: EdgeInsets.zero, w: EdgeInsets.all(0));\n"
           "y(c: Colors.transparent);\n"
           "z(c: Colors.red, p: SizedBox(width: 12), q: EdgeInsets.symmetric(horizontal: 4.5));\n")
    r = m9_hardcodes.analisar_arquivo(src)
    assert r == [(7, "cor"), (7, "espacamento"), (7, "espacamento")]


def test_m10(repo, gab):
    for tag in ("v1", "v2"):
        with tag_copy(repo, tag) as root:
            r = m10_either.analisar(root)
        assert _pares(r["violacoes"], "arquivo", "linha", "metodo") == sorted(
            (x["arquivo"], x["linha"], x["metodo"].split(".")[1]) for x in gab["m10_assinaturas"]["v1"])
        assert r["M10_assinaturas"] == gab["m10_assinaturas"]["total"]


def test_m10_casos():
    src = ("abstract class XRepository {\n  Future<Either<Failure, int>> a();\n  Future<int> b();\n  void c();\n"
           "  Stream<Either<F, int>> d();\n  int get e;\n  final int f = 1;\n  Future<void> _p();\n  XRepository();\n}\n"
           "class Z { Future<int> nope() async => 1; }\n")
    r = m10_either.analisar_arquivo(src)
    assert [(v["metodo"], v["linha"]) for v in r] == [("b", 3), ("c", 4)]

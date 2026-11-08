import subprocess

from harness.estatico import m15_consistencia as m15
from harness.estatico.common import tag_copy


def test_m15_calibracao(repo, gab):
    g = gab["m15"]
    with tag_copy(repo, "v1") as a, tag_copy(repo, "v2") as b:
        r = m15.analisar(a, b, gab["referencia_m15"]["feature"])
    assert r["referencia"] == g["referencia"]
    assert r["por_feature"]["chat"] == g["chat"]
    assert r["por_feature"]["timeline"] == g["timeline"]
    assert r["M15_divergencias"] == g["M15_divergencias"]


def test_m15_detectar_ref(tmp_path):
    def sh(*a):
        subprocess.run(a, cwd=tmp_path, check=True, capture_output=True)
    sh("git", "init", "-q", "-b", "main")
    sh("git", "config", "user.email", "x@y.z"); sh("git", "config", "user.name", "x")
    (tmp_path / "README.md").write_text("x"); sh("git", "add", "-A"); sh("git", "commit", "-qm", "a"); sh("git", "tag", "f000")
    for f in ("lib/features/capture/domain/a.dart", "lib/features/capture/data/b.dart", "lib/features/other/x.dart"):
        p = tmp_path / f; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("//")
    sh("git", "add", "-A"); sh("git", "commit", "-qm", "b"); sh("git", "tag", "rf01")
    assert m15.detectar_ref(tmp_path, "f000", "rf01") == "capture"

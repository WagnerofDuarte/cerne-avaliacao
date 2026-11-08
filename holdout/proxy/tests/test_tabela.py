"""Cada um dos 15 cenarios de rnf09.md (C-019) existe na tabela do addon com a funcao e a falha certas."""
import re
from pathlib import Path

from holdout.proxy.cenarios import CENARIOS

RNF09 = Path(__file__).resolve().parents[2] / "rnf09.md"


def test_quinze_cenarios_do_rnf09():
    linhas = re.findall(r"^\| (F\d\d) \| `([a-z-]+)` \|.*?\| (timeout|malformed|offline) \|", RNF09.read_text(), re.M)
    assert [l[0] for l in linhas] == [f"F{i:02d}" for i in range(1, 16)]
    for fid, fn, falha in linhas:
        r = CENARIOS[fid]
        assert len(r) == 1 and r[0]["fn"] == fn and r[0]["acao"] == "fault" and r[0]["valor"] == falha and r[0]["limite"] == 1, fid

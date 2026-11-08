"""Testes do H-007 com dados SINTÉTICOS (regra 8: nenhum dado real aqui)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rederivar as rd  # noqa: E402

col = rd.col


def human(ts, text, uuid):
    return {"type": "user", "timestamp": ts, "uuid": uuid, "origin": {"kind": "human"},
            "message": {"role": "user", "content": text}}


def assistant(ts, uuid, stop="end_turn", mid="m1", out=5):
    return {"type": "assistant", "timestamp": ts, "uuid": uuid,
            "message": {"id": mid, "model": "claude-sonnet-5", "stop_reason": stop,
                        "usage": {"input_tokens": 1, "output_tokens": out}, "content": [{"type": "text", "text": "ok"}]}}


class TestUnwrap(unittest.TestCase):
    def setUp(self):
        rd.install_unwrap()

    def run_extract(self, text):
        recs = [human("2026-01-01T00:00:00Z", text, "u1")]
        seg = col.segment_by_phase(recs)
        return col.extract_intervencoes_e_processo(seg)

    def test_intervencao_digitada(self):
        i, p, a = self.run_extract("INTERVENÇÃO [correção|S2|prd]: texto")
        self.assertEqual((len(i), len(p)), (1, 0))

    def test_intervencao_colada_reconhecida(self):
        wrapped = '<pasted_content id="x">\nINTERVENÇÃO [correção|S2|prd]: texto\n</pasted_content id="x">'
        i, p, a = self.run_extract(wrapped)
        self.assertEqual(len(i), 1)
        self.assertEqual(i[0].tipo, "correção")

    def test_processo_colado_reconhecido(self):
        i, p, a = self.run_extract('<pasted_content id="y">\nPROCESSO: Yes.\n</pasted_content id="y">')
        self.assertEqual((len(i), len(p)), (0, 1))

    def test_texto_comum_nao_vira_intervencao(self):
        i, p, a = self.run_extract("continue")
        self.assertEqual((len(i), len(p), len(a)), (0, 0, 0))


class TestFases(unittest.TestCase):
    def test_correcao_vira_impl(self):
        recs = [human("2026-01-01T00:00:00Z", "INTERVENÇÃO [correção|S2|prd]: x", "u1"), assistant("2026-01-01T00:00:05Z", "a1")]
        seg = rd.segment_with_correction_phase(recs, "RF04")
        self.assertTrue(all(f == "IMPL" and m == "(correcao)" for _, f, m in seg))

    def test_setup_e_plan_ficam_como_estao(self):
        recs = [human("2026-01-01T00:00:00Z", "oi", "u1")]
        for unidade in ("SETUP", "PLAN"):
            seg = rd.segment_with_correction_phase(recs, unidade)
            self.assertTrue(all(f == "SETUP" for _, f, _ in seg))

    def test_sessao_com_comando_mantem_fase_do_comando(self):
        cmd = "<command-message>speckit-plan</command-message>\n<command-name>/speckit-plan</command-name>"
        recs = [human("2026-01-01T00:00:00Z", cmd, "u1"), assistant("2026-01-01T00:00:05Z", "a1")]
        seg = rd.segment_with_correction_phase(recs, "RF01")
        self.assertEqual({(f, m) for _, f, m in seg} - {("SETUP", "(nenhum)")}, {("ESPEC", "speckit-plan")})

    def test_skill_tool_do_agente_vale_como_marcador(self):
        """D-014: comando dentro de <pasted_content>; o agente chama a ferramenta Skill."""
        colado = '<pasted_content id="1">\n/speckit-constitution # P-SETUP\n</pasted_content id="1">'
        ag = {"type": "assistant", "timestamp": "2026-01-01T00:00:03Z", "uuid": "a0",
              "message": {"id": "m0", "model": "claude-sonnet-5", "stop_reason": "tool_use",
                          "usage": {"input_tokens": 1, "output_tokens": 1},
                          "content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "speckit-constitution"}}]}}
        recs = [human("2026-01-01T00:00:00Z", colado, "u1"), ag, assistant("2026-01-01T00:00:09Z", "a1")]
        seg = rd.segment_with_correction_phase(recs, "SETUP")
        self.assertEqual(seg[-1][1:], ("ESPEC", "speckit-constitution"))
        self.assertEqual(seg[0][1:], ("SETUP", "(nenhum)"))

    def test_skill_tool_nao_sobrescreve_comando_digitado(self):
        cmd = "<command-name>/bmad-build</command-name>"
        ag = {"type": "assistant", "timestamp": "2026-01-01T00:00:03Z", "uuid": "a0",
              "message": {"id": "m0", "model": "claude-sonnet-5", "stop_reason": "tool_use",
                          "usage": {"input_tokens": 1, "output_tokens": 1},
                          "content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "bmad-code-review"}}]}}
        recs = [human("2026-01-01T00:00:00Z", cmd, "u1"), ag]
        seg = rd.segment_with_correction_phase(recs, "RF01")
        self.assertEqual(seg[-1][1:], ("IMPL", "bmad-build"))


class TestLivres(unittest.TestCase):
    def test_categorias(self):
        self.assertEqual(rd.categorize_free("[Request interrupted by user]"), "interrupcao")
        self.assertEqual(rd.categorize_free("Yes"), "neutra")
        self.assertEqual(rd.categorize_free("Yeds"), "neutra")
        self.assertEqual(rd.categorize_free("continue the developing"), "retomada")
        self.assertEqual(rd.categorize_free("Try again"), "retomada")
        self.assertEqual(rd.categorize_free("ill run the tests by myself"), "outra")

    def test_nao_lista_reconhecidas_nem_invocacoes(self):
        recs = [
            human("2026-01-01T00:00:00Z", "<command-name>/bmad-build</command-name>", "u1"),
            human("2026-01-01T00:00:01Z", "PROCESSO: Yes.", "u2"),
            human("2026-01-01T00:00:02Z", "continue", "u3"),
            human("2026-01-01T00:00:03Z", "<command-name>/coletar-sessao</command-name>", "u4"),
        ]
        seg = col.segment_by_phase(recs)
        out = rd.free_messages(seg, "b", "RF01", "s1")
        self.assertEqual([o["categoria"] for o in out], ["retomada"])

    def test_interrupcao_e_listada_mesmo_sem_origem_humana(self):
        recs = [{"type": "user", "timestamp": "2026-01-01T00:00:00Z", "uuid": "u9",
                 "message": {"role": "user", "content": [{"type": "text", "text": "[Request interrupted by user for tool use]"}]}}]
        seg = col.segment_by_phase(recs)
        out = rd.free_messages(seg, "b", "RF01", "s1")
        self.assertEqual([o["categoria"] for o in out], ["interrupcao"])


class TestCiclo(unittest.TestCase):
    """Fim a fim com um ciclo sintético: duplicata de coleta, sessão sem coleta, uma linha por sessão."""

    def make(self, tmp: Path):
        dados = tmp / "dados"
        (dados / "brutos").mkdir(parents=True)
        recs = [human("2026-01-01T00:00:00Z", "INTERVENÇÃO [correção|S2|prd]: x", "u1"), assistant("2026-01-01T00:00:10Z", "a1")]
        for sid in ("s1111111-0000-0000-0000-000000000001", "5256ebbb-0000-0000-0000-000000000002"):
            with (dados / "brutos" / f"{sid}.jsonl").open("w") as f:
                for r in recs:
                    f.write(json.dumps(r) + "\n")
        header = col.CSV_FIELDS["sessoes.csv"]
        rows = []
        for _ in range(2):  # duplicata (D-031)
            r = {k: "" for k in header}
            r.update({"ciclo": "a", "id_rf": "RF04", "sessao_id": "s1111111-0000-0000-0000-000000000001",
                      "tipo_sessao": "desenvolvimento", "modo_coleta": "manual", "motivo_fim": "normal"})
            rows.append(r)
        rd.write_csv(dados / "sessoes.csv", header, rows)
        return dados

    def test_ciclo(self):
        with tempfile.TemporaryDirectory() as t:
            dados = self.make(Path(t))
            res = rd.rederive_cycle("a", dados, dados / "rederivado")
            self.assertEqual(res["sessoes"], 2)  # 1 linha por sessão + a sem coleta (D-037)
            self.assertEqual(res["problemas"], [])
            ids = [r["sessao_id"] for r in rd.read_csv(dados / "rederivado" / "sessoes.csv")]
            self.assertEqual(len(ids), len(set(ids)))
            sem = [r for r in rd.read_csv(dados / "rederivado" / "sessoes.csv") if r["sessao_id"].startswith("5256ebbb")]
            self.assertEqual(sem[0]["id_rf"], "RF04")
            self.assertEqual(sem[0]["modo_coleta"], "sem_coleta")
            interv = rd.read_csv(dados / "rederivado" / "intervencoes.csv")
            self.assertEqual(len(interv), 2)


if __name__ == "__main__":
    unittest.main()

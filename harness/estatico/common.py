"""Utilitarios comuns do harness estatico (Python, so biblioteca padrao + PyYAML).

Regra: nada aqui grava dentro de repositorio de app. Toda leitura de tag e feita por
`git archive` numa pasta temporaria (copia), nunca por checkout no repositorio medido.
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

# --------------------------------------------------------------------------- git

def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


@contextlib.contextmanager
def tag_copy(repo, tag, prefix="harness-"):
    """Extrai a tag para uma pasta temporaria (copia) e a remove no fim."""
    tmp = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        p = subprocess.run(f"git -C '{repo}' archive '{tag}' | tar -x -C '{tmp}'", shell=True, capture_output=True, text=True)
        if p.returncode != 0:
            raise RuntimeError(f"git archive {tag}: {p.stderr.strip()}")
        # D-107: `.env` e ignorado pelo git (guarda segredos), mas o pubspec o declara como asset; sem o arquivo o
        # `flutter test` nao monta o pacote de assets. A copia recebe o `.env.example` do proprio repositorio
        # (valores de exemplo) ou, sem ele, um `.env` vazio; nenhum segredo e usado.
        pub = tmp / "pubspec.yaml"
        if pub.exists() and any(l.strip() == "- .env" for l in pub.read_text(encoding="utf-8", errors="ignore").splitlines()):
            exemplo = tmp / ".env.example"
            if exemplo.exists():
                shutil.copy(exemplo, tmp / ".env")
            else:
                (tmp / ".env").touch(exist_ok=True)
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def tree_files(repo, tag):
    return [l for l in git(repo, "ls-tree", "-r", "--name-only", tag).splitlines() if l]


def show(repo, tag, path):
    return git(repo, "show", f"{tag}:{path}", check=False)


def diff_name_status(repo, prev, tag):
    """[(status, path)] entre duas tags; renomeacao vira D + A (sem -M)."""
    out = git(repo, "diff", "--no-renames", "--name-status", prev, tag)
    return [tuple(l.split("\t", 1)) for l in out.splitlines() if l]


def diff_added_lines(repo, prev, tag):
    """{path: [(linha_no_arquivo_novo, texto)]} das linhas adicionadas."""
    out = git(repo, "diff", "--no-renames", "-U0", prev, tag)
    res, cur, ln = {}, None, 0
    for l in out.splitlines():
        if l.startswith("+++ "):
            cur = l[6:] if l.startswith("+++ b/") else None
            if cur is not None:
                res.setdefault(cur, [])
        elif l.startswith("@@"):
            m = re.search(r"\+(\d+)", l)
            ln = int(m.group(1)) if m else 0
        elif cur is not None and l.startswith("+") and not l.startswith("+++"):
            res[cur].append((ln, l[1:]))
            ln += 1
    return res

# --------------------------------------------------------------------------- dart

def mask_dart(src: str, strings: bool = True) -> str:
    """Troca comentarios (e, se `strings`, o conteudo de literais de string) por espacos,
    preservando quebras de linha e posicoes (os numeros de linha continuam validos)."""
    res = list(src)
    n = len(src)

    def blank(a, b):
        for k in range(a, b):
            if res[k] != "\n":
                res[k] = " "

    def skip_interp(j):
        """j aponta para o '{' de ${...}; devolve o indice depois do '}' correspondente."""
        depth = 0
        while j < n:
            c = src[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return j + 1
            elif c in "'\"":
                j = scan_string(j, False)
                continue
            j += 1
        return j

    def scan_string(i, do_mask):
        q = src[i]
        triple = src.startswith(q * 3, i)
        raw = i > 0 and src[i - 1] == "r" and (i < 2 or not (src[i - 2].isalnum() or src[i - 2] == "_"))
        j = i + (3 if triple else 1)
        start = j
        while j < n:
            c = src[j]
            if c == "\\" and not raw:
                j += 2
                continue
            if c == "$" and not raw and j + 1 < n and src[j + 1] == "{":
                j = skip_interp(j + 1)
                continue
            if triple and src.startswith(q * 3, j):
                if do_mask and strings:
                    blank(start, j)
                return j + 3
            if not triple and c == q:
                if do_mask and strings:
                    blank(start, j)
                return j + 1
            if not triple and c == "\n":
                break
            j += 1
        if do_mask and strings:
            blank(start, min(j, n))
        return j

    i = 0
    while i < n:
        if src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
        elif src.startswith("/*", i):
            depth, j = 1, i + 2
            while j < n and depth:
                if src.startswith("/*", j):
                    depth += 1
                    j += 2
                elif src.startswith("*/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            blank(i, j)
            i = j
        elif src[i] in "'\"":
            i = scan_string(i, True)
        else:
            i += 1
    return "".join(res)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


GERADO = re.compile(r"\.(freezed|g)\.dart$")  # D-108: codigo gerado por build_runner nao e codigo do produto


def dart_files(root, sub="lib"):
    base = Path(root) / sub
    return sorted(p for p in base.rglob("*.dart") if not GERADO.search(p.name)) if base.exists() else []


def rel(root, p):
    return PurePosixPath(Path(p).relative_to(root)).as_posix()


def app_name(root) -> str:
    m = re.search(r"^name:\s*([A-Za-z0-9_]+)", read(Path(root) / "pubspec.yaml"), re.M)
    return m.group(1) if m else ""


IMPORT_RE = re.compile(r"""^[ \t]*(?:import|export)\s+(['"])(.+?)\1""", re.M)


def imports_of(src: str):
    """[(linha, uri)] de import/export, lendo o texto sem comentarios."""
    code = mask_dart(src, strings=False)
    return [(line_of(code, m.start()), m.group(2)) for m in IMPORT_RE.finditer(code)]


def resolve_import(root, file_rel: str, uri: str, app: str):
    """Caminho relativo a raiz (posix) do arquivo importado, ou None se for externo.
    Devolve ('ext', nome) para pacotes externos / dart:."""
    if uri.startswith("dart:"):
        return ("ext", uri)
    if uri.startswith("package:"):
        pkg, _, path = uri[len("package:"):].partition("/")
        if pkg == app:
            return ("int", f"lib/{path}")
        return ("ext", uri)
    base = PurePosixPath(file_rel).parent
    parts = []
    for seg in (base / uri).parts:
        if seg == "..":
            if parts:
                parts.pop()
        elif seg != ".":
            parts.append(seg)
    return ("int", "/".join(parts))


def layer_of(path: str):
    """lib/features/<f>/<layer>/... -> (feature, layer); lib/core/... -> ('core', 'core')."""
    p = PurePosixPath(path).parts
    if len(p) >= 4 and p[0] == "lib" and p[1] == "features":
        return p[2], (p[3] if p[3] in ("data", "domain", "presentation") else "other")
    if len(p) >= 2 and p[0] == "lib" and p[1] == "core":
        return "core", "core"
    return None, None


def dump(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=False))

# ------------------------------------------------------------------------ flutter

def flutter_env():
    env = dict(os.environ)
    env.setdefault("FLUTTER_ALLOW_ROOT", "true")
    return env


def flutter_bin():
    return shutil.which("flutter") or "flutter"


def preparar_dependencias(root, env=None, timeout=600):
    """D-108: `flutter pub get` e, se o pubspec depende de `build_runner`, a geracao de codigo no procedimento
    documentado pelo proprio repositorio (`pub run build_runner build --delete-conflicting-outputs`). Os arquivos
    `*.freezed.dart` e `*.g.dart` sao ignorados pelo git nas tags; sem a geracao, os testes nao compilam."""
    env = env or flutter_env()
    subprocess.run([flutter_bin(), "pub", "get"], cwd=root, capture_output=True, text=True, env=env, timeout=timeout)
    pub = Path(root) / "pubspec.yaml"
    if pub.exists() and re.search(r"^\s*build_runner\s*:", pub.read_text(encoding="utf-8", errors="ignore"), re.M):
        subprocess.run([flutter_bin(), "pub", "run", "build_runner", "build", "--delete-conflicting-outputs"], cwd=root,
                       capture_output=True, text=True, env=env, timeout=timeout)


def run_flutter_tests_json(root, extra=(), timeout=600, pub_get=True):
    """Roda `flutter test --reporter json` em `root` (uma copia temporaria!) e devolve
    (codigo_saida, {id_teste: 'success'|'failure'|'error'|'skipped'})."""
    if pub_get:
        preparar_dependencias(root, flutter_env(), timeout)
    p = subprocess.run([flutter_bin(), "test", "--reporter", "json", "--no-pub", *extra], cwd=root,
                       capture_output=True, text=True, env=flutter_env(), timeout=timeout)
    return p.returncode, parse_test_json(p.stdout, root)


def parse_test_json(text, root=None):
    """Interpreta o reporter json do `flutter test`. ID = '<arquivo relativo>::<nome completo>'."""
    suites, tests, result = {}, {}, {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        t = ev.get("type")
        if t == "suite":
            suites[ev["suite"]["id"]] = ev["suite"]["path"]
        elif t == "testStart":
            tt = ev["test"]
            tests[tt["id"]] = (tt["suiteID"], tt["name"], tt.get("metadata", {}).get("skip", False))
        elif t == "testDone":
            tid = ev["testID"]
            if tid not in tests or ev.get("hidden"):
                continue
            sid, name, skip = tests[tid]
            if name.startswith("loading "):
                continue
            path = suites.get(sid, "")
            if root:
                with contextlib.suppress(ValueError):
                    path = PurePosixPath(Path(path).resolve().relative_to(Path(root).resolve())).as_posix()
            res = "skipped" if (ev.get("skipped") or skip) else ev["result"]
            result[f"{path}::{name}"] = res
    return result

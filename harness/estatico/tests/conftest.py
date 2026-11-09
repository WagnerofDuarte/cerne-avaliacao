import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[3]
CAL = RAIZ / "calibracao"


@pytest.fixture(scope="session")
def repo(tmp_path_factory):
    """Repositorio git de calibracao montado em pasta temporaria (tags v1 e v2)."""
    dest = tmp_path_factory.mktemp("calibracao") / "repo"
    subprocess.run([str(CAL / "montar-repo.sh"), str(dest)], check=True, capture_output=True)
    return dest


@pytest.fixture(scope="session")
def gab():
    return json.loads((CAL / "gabarito.json").read_text())


@pytest.fixture(scope="session")
def sintetico():
    return CAL / "backend-sintetico"

import os
import subprocess
import sys
from pathlib import Path


def test_eval_runs_outside_repository_directory(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        filter(None, [str(repo_root), env.get("PYTHONPATH", "")])
    )

    result = subprocess.run(
        [sys.executable, "-m", "eval.run_eval"],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "| heuristics | All | 30 | 28 |" in result.stdout

"""Day 4: the eval files must at least parse as ADK expects.

This checks the shape only. Running the evaluation needs a live model:
    adk eval vinyl_crate_agents evals/vinyl_basics.evalset.json --config_file_path evals/test_config.json
"""

import json
from pathlib import Path

from google.adk.evaluation.eval_config import EvalConfig
from google.adk.evaluation.eval_set import EvalSet

EVALS = Path(__file__).resolve().parents[1] / "evals"


def test_evalset_parses():
    eval_set = EvalSet.model_validate_json((EVALS / "vinyl_basics.evalset.json").read_text())
    assert [c.eval_id for c in eval_set.eval_cases] == [
        "records_owned_album",
        "lists_collection",
        "recommends_by_genre",
    ]


def test_eval_config_parses():
    config = EvalConfig.model_validate(json.loads((EVALS / "test_config.json").read_text()))
    assert "tool_trajectory_avg_score" in config.criteria

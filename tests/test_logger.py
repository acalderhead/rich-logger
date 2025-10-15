# ─────────────────────────────────────────────────────────────────────────────
# Minimal test for the RichLogger module
# ─────────────────────────────────────────────────────────────────────────────

import pytest
from time        import sleep
from rich_logger import RichLogger


def test_logger_execution(capsys):
    """
    Smoke test to ensure all RichLogger methods execute without error.
    Output is captured but not visually validated.
    """
    logger = RichLogger("demo")

    # Initialization
    logger.config("Mode: test | Threshold=10")
    logger.meta("Dataset: sample_data.csv | Records=5")
    logger.read("Loading dataset")
    sleep(1)

    # Iterative Processing
    logger.stage("Validating data")
    sample_data = [4, 12, 15]
    accepted = []
    sleep(1)

    for i, value in enumerate(sample_data, start=1):
        logger.step(f"Record {i}: {value}")
        logger.check(f"Type={type(value).__name__}")

        if value > 10:
            logger.substep("Above threshold")
            accepted.append(value)
            logger.result(f"{value} accepted")
        else:
            logger.substep("Below threshold")
            logger.warning(f"{value} ignored")

        sleep(1)

    # Metrics and Outputs
    ratio = len(accepted) / len(sample_data)
    ignored = len(sample_data) - len(accepted)
    logger.metric(f"accepted={len(accepted)} ignored={ignored} ratio={ratio:.2f}")
    logger.info("Validation done")
    sleep(1)

    # Final Computation
    try:
        logger.stage("Computing summary")
        avg = sum(accepted) / len(accepted)
        logger.result(f"Mean={avg:.2f}")
        logger.write("Saved results")
        _ = 1 / 0  # force exception
    except Exception as e:
        logger.error(f"Failure: {e}")
        logger.debug("ZeroDivisionError test")

    sleep(1)

    logger.alert("Run completed with handled exception")

    # Capture output for sanity check
    out, err = capsys.readouterr()
    assert "Loading dataset" in out
    assert "Failure" in out

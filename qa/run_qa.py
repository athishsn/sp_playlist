from qa.raw_checks import RAW_LISTENING_CHECKS
from qa.qa_engine import run_checks
from qa.gatekeeper import evaluate_run_status


def main():
    results = run_checks(
        RAW_LISTENING_CHECKS,
        table_name="raw_listening_events"
    )

    run_id =results[0][0]
    
    run_status, qa_failures = evaluate_run_status(run_id)
    print(f"Pipeline QA Status: {run_status}")

    if run_status == "FAILED":
        raise RuntimeError("Pipeline failed due to QA errors")

if __name__ == "__main__":
    main()

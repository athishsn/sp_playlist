from qa.raw_checks import RAW_LISTENING_CHECKS
from qa.qa_engine import run_checks

def main():
    results = run_checks(
        RAW_LISTENING_CHECKS,
        table_name="raw_listening_events"
    )

    for r in results:
        print(r)

if __name__ == "__main__":
    main()

from qa.checks_raw import RAW_LISTENING_CHECKS
from qa.engine import run_checks

results = run_checks(RAW_LISTENING_CHECKS, "raw_listening_events")

for r in results:
    print(r)

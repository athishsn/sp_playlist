from utils.db import run_sql_file


def main():
    print("Refreshing analytics_user_metrics.")
    
    run_sql_file('analytics/sql/analytics_user_metrics.sql')
    
    print('user metrics refreshed.')
    
if __name__ == "__main__":
    main()
    
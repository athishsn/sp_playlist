from utils.db import run_sql_file

def main():
    print("Building analytics tables.")
    
    run_sql_file('analytics/sql/create_analytics_tables.sql')
    run_sql_file('analytics/sql/analytics_listening_events.sql')
    run_sql_file('analytics/sql/analytics_user_metrics.sql')
    
    
    print('anlytics table built successfully.')
    
if __name__ == "__main__":
    main()
from analytics.pipelines.refresh_user_metrics import main as refresh

from analytics.pipelines.build_analytics_tables import main as build


def main():
    print("executing run all pipeline.")
    build()
    refresh()
    
    print("pipeline run successful.")
    
if __name__ == "__main__":
    main()
    
    
    
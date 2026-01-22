import pandas as pd 

def label_persona(row):
    if row["session_length"] > 20 and row["unique_artists"] <= 2:
        return "Comfort Binge"
    if row["unique_artists"] > 5:
        return "Exploration Mode"
    
    if row["session_start_hour"] > 22 :
        return "Night Owl"
    
    if row["session_length"] <= 5:
        return "Quick Hit"
    
    return "Balanced session"


def main():
    df = pd.read_csv('session_clusters.csv')
    
    cluster_profiles = (
        df.groupby("cluster_id")
            .mean(numeric_only=True)
            .reset_index()
    )
    
    cluster_profiles['persona'] = cluster_profiles.apply(
        label_persona, axis=1
    )
    
    
    #join labels 
    df = df.merge(
        cluster_profiles[['cluster_id','persona']],
        on='cluster_id',
        how='left'
    )
    
    print(cluster_profiles[["cluster_id","persona"]])
    
    df.to_csv('session_clusters_labeled.csv', index=False)
    print("Saved session_clusters_labeled.csv")
    
if __name__ == "__main__":
    main()
    
    
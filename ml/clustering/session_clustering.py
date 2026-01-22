import pandas as pd 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def main(desired_k=4):
    
    df = pd.read_csv('ml_session_features.csv')
    
    if df.empty:
        print("No sessions available.")
        return 
    
    feature_cols = [
        'session_length',
        'unique_artists',
        'session_start_hour'
    ]
    
    X = df[feature_cols]
    
    n_samples = len(X)
    if n_samples <2 :
        print("not enough sessions to cluster.")
        return 
    
    #Dynamic cluster count 
    k = min(desired_k, n_samples)
    
    
    #scaler features 
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    #Kmeans clustering 
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    
    df.to_csv('session_clusters.csv', index=False)
    print("Saved session_cluster.csv")
    
    print(df.groupby('cluster_id')[feature_cols].mean())
    
if __name__ =="__main__":
    main()
    
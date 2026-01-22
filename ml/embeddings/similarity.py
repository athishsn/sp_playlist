import pandas as pd 
import numpy as np 


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10
    )
    
    
def most_similar_users(user_id, top_K = 5):
    
    user_vectors = pd.read_csv('user_embeddings.csv', index_col=0)
    
    target = user_vectors.loc[user_id].values
    
    sims=[]
    
    for uid, row in user_vectors.iterrows():
        if uid == user_id:
            continue
        
        sim = cosine_similarity(target, row.values)
        sims.append((uid, sim))
        
    sims.sort(key=lambda x: x[1], reverse=True)
    
    return sims[:top_K]


if __name__ == "__main__":
    print(most_similar_users("current_user"))
    
    
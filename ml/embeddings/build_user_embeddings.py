import pandas as pd 

def main():
    
    artist_vectors= pd.read_csv('artist_embeddings.csv', index_col=0)
    
    #normalize artist vector 
    artist_vectors_norm = artist_vectors.div(
        (artist_vectors.pow(2).sum(axis=1)** 0.5), axis=0
    ).fillna(0)
    
    # User embedding = sum of artist embeddings listened to
    user_vectors = artist_vectors_norm.T
    
    user_vectors.to_csv("user_embeddings.csv")
    print("Saved user_embeddings.csv")
    
if __name__ == "__main__":
    main()
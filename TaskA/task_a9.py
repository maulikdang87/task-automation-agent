import dotenv
import os
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

import requests
import numpy as np

def A9():
    """
    Reads comments from './data/comments.txt', obtains embeddings for all comments via the LLM embeddings API,
    computes cosine similarities between each pair, and writes the most similar pair to './data/comments-similar.txt'.
    """
    
    load_dotenv()
    api_token = os.environ.get("OPENAI_API_KEY")
    
    comments_file = os.path.join(os.getcwd(), "data", "comments.txt")
    output_file = os.path.join(os.getcwd(), "data", "comments-similar.txt")
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
 
    
    # Check prerequisites
    if not os.path.isfile(comments_file):
        raise FileNotFoundError("Comments file not found")
    if not api_token:
        raise RuntimeError("API token not found in environment variables")
    
    try:
        # Read non-empty comments
        with open(comments_file, "r", encoding="utf-8") as f:
            comments = [line.strip() for line in f if line.strip()]
        
        if len(comments) < 2:
            raise RuntimeError("Not enough comments to compare")
        
        # Prepare the payload for the embeddings API
        payload = {
            "model": "text-embedding-3-small",
            "input": comments
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        
        # Request embeddings from the LLM embeddings endpoint
        response = requests.post(api_url, headers=headers, json=payload)

        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()
        # Extract embeddings as numpy arrays
        embeddings = [np.array(item["embedding"]) for item in response_data["data"]]
        n = len(embeddings)
        max_score = -1.0
        max_pair = (None, None)
        
        # Compute cosine similarity between each pair of embeddings
        for i in range(n):
            for j in range(i + 1, n):
                norm_i = np.linalg.norm(embeddings[i])
                norm_j = np.linalg.norm(embeddings[j])
                if norm_i == 0 or norm_j == 0:
                    continue
                sim = np.dot(embeddings[i], embeddings[j]) / (norm_i * norm_j)
                if sim > max_score:
                    max_score = sim
                    max_pair = (i, j)
                    
        
        if max_pair[0] is None or max_pair[1] is None:
            raise RuntimeError("Failed to find similar comments")
        
        # Write the two most similar comments to the output file (one per line)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(comments[max_pair[0]] + "\n" + comments[max_pair[1]] + "\n")
        
        return response_data
    except Exception as e:
        raise RuntimeError(f"Error finding similar comments: {e}")

# memory.py
import chromadb

# ✅ Use the new persistent client method
client = chromadb.PersistentClient(path="./chroma_store")

# ✅ Create or load the memory collection
collection = client.get_or_create_collection("rain_tasks")

def store_prompt(prompt: str, task_id: str):
    collection.add(
        documents=[prompt],
        metadatas=[{"task_id": task_id}],
        ids=[task_id]
    )

def search_similar_prompts(query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
if __name__ == "__main__":
    store_prompt("Generate a Python script to fetch weather data", "test-001")
    result = search_similar_prompts("Fetch weather from an API")
    print(result)
if __name__ == "__main__":
    store_prompt("Generate a Python script to fetch weather data", "test-001")
    result = search_similar_prompts("Fetch weather from an API")
    print(result)

import chromadb

client = chromadb.PersistentClient(path="./database/")
print(client)
client.heartbeat() # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
#client.reset() # Empties and completely resets the database. ⚠️ This is destructive and not reversible.

collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
collection = client.get_collection(name="my_collection", embedding_function=emb_fn)

collection = client.get_collection(name="test") # Get a collection object from an existing collection, by name. Will raise an exception if it's not found.
collection = client.get_or_create_collection(name="test") # Get a collection object from an existing collection, by name. If it doesn't exist, create it.
client.delete_collection(name="my_collection") # Delete a collection and all associated embeddings, documents, and metadata. ⚠️ This is destructive and not reversible
print("RAG PIPELINE STARTED")

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGPipeline:

    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.chunks = []

    def load_documents(self):

        documents = []

        if not os.path.exists(self.data_folder):
            print(f"Folder '{self.data_folder}' not found!")
            return documents
        print("Files Found:", os.listdir(self.data_folder))

        for file in os.listdir(self.data_folder):

            file_path = os.path.join(self.data_folder, file)

            if file.endswith(".md") or file.endswith(".txt"):

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    documents.append({
                        "source": file,
                        "content": text
                    })

                except Exception as e:
                    print(f"Error reading {file}: {e}")

        return documents

    def create_chunks(self):

        documents = self.load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )

        for doc in documents:

            split_chunks = splitter.split_text(doc["content"])

            for i, chunk in enumerate(split_chunks):

                self.chunks.append({
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_id": i
                })

        return self.chunks

    def retrieve(self, query):

        results = []

        query_words = query.lower().split()

        for chunk in self.chunks:

            chunk_text = chunk["text"].lower()

            score = 0

            for word in query_words:
                if word in chunk_text:
                    score += 1

            if score > 0:
                results.append((score, chunk))

        results.sort(reverse=True, key=lambda x: x[0])

        return [item[1] for item in results[:3]]

if __name__ == "__main__":

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    data_path = os.path.join(base_dir, "data")

    print("Using data folder:", data_path)

    rag = RAGPipeline(data_path)

    rag.create_chunks()

    print(rag.chunks)

    print("Chunks Loaded:", len(rag.chunks))

    question = input("\nEnter Query: ")

    retrieved = rag.retrieve(question)

    print("\nRetrieved Chunks:\n")

    if not retrieved:
        print("No relevant chunks found.")

    for item in retrieved:
        print("Source:", item["source"])
        print("Chunk ID:", item["chunk_id"])
        print(item["text"])
        print("-" * 50)
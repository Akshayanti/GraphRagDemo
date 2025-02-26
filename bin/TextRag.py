import ollama


class TextRag:
    def __init__(self, model, embedding="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"):
        self.embedding = embedding
        self.dataset = []
        self.model = model
        with open("data/text/cat_facts.txt", "r") as file:
            self.dataset = file.readlines()
        self.vector_db = []
        for i, chunk in enumerate(self.dataset):
            embedding = ollama.embed(model=self.embedding, input=chunk)["embeddings"][0]
            self.vector_db.append((chunk, embedding))

    def query(self, query):
        self.retrieve(query)
        prompt = f"""You are a helpful chatbot. Use only the following pieces of context 
            to answer the question if possible. If it's not possible, use your own knowledge 
            but DO NOT make up any new information:
            {' '.join([f' - {chunk}' for chunk, similarity in self.retrieved_knowledge])}"""
        print(f"Query: {query}")
        print("**************** BEFORE RAG: ****************")
        print(
            ollama.chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": query},
                ],
                stream=False,
            )["message"]["content"]
        )
        print("**************** AFTER RAG: *****************")
        print(
            ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                ],
                stream=False,
            )["message"]["content"]
        )
        print("***********************************************************************")

    def retrieve(self, query, top_n=10):
        qe = ollama.embed(model=self.embedding, input=query)["embeddings"][0]
        similarities = []

        def cosine_similarity(a, b):
            dot_product = sum([x * y for x, y in zip(a, b)])
            norm_a = sum([x**2 for x in a]) ** 0.5
            norm_b = sum([x**2 for x in b]) ** 0.5
            return dot_product / (norm_a * norm_b)

        for chunk, embedding in self.vector_db:
            similarity = cosine_similarity(qe, embedding)
            similarities.append((chunk, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        self.retrieved_knowledge = similarities[:top_n]

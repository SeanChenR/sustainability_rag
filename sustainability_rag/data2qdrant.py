from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from uuid import uuid4

from parse_pdf import parse_pdf

class data2qdrant:
    def __init__(self):
        self.nodes = parse_pdf('issb').main_parse()
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = "sustainability_data"

    def check_collection(self):
        if self.client.collection_exists(collection_name=self.collection_name):
            print("Collection already exists")
        else:
            print("Creating collection")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
    
    def node2doc(self):
        documents = []
        for node in self.nodes:
            docs = Document(page_content=node)
            documents.append(docs)
        uuids = [str(uuid4()) for _ in range(len(documents))]
        return documents, uuids
    
    def main(self):
        self.check_collection()
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )
        documents, uuids = self.node2doc()
        vector_store.add_documents(documents=documents, ids=uuids)

if __name__ in "__main__":
    data2qdrant().main()
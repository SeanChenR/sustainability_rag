import os
import nest_asyncio
nest_asyncio.apply()

from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()

class parse_pdf():
    def __init__(self, prefix):
        self.folder_path = "/Users/seanchen/Sean/sustainability_rag/docs"
        self.model = "gpt-4o"
        self.llm = OpenAI(model=self.model)
        self.prefix = prefix

    def get_file(self):
        sustainability_data = []
        folder = os.listdir(self.folder_path)
        for file in folder:
            if file.startswith(self.prefix):
                sustainability_data.append(file)
        return sustainability_data
    
    def do_llama_parse(self, file_name):
        parser = LlamaParse(result_type="markdown")
        markdown_docs = parser.load_data(file_path=file_name)
        return markdown_docs
    
    def parse_node(self, markdown_docs):
        Settings.llm = self.llm
        node_parser = MarkdownElementNodeParser(llm=OpenAI(model=self.model), num_workers=8)
        nodes = node_parser.get_nodes_from_documents(markdown_docs)
        return nodes
    
    def do_pypdf(self):
        file_name = self.get_file()[0]
        print(file_name)
        file_path = os.path.join(self.folder_path, file_name)
        pdf_loader = PyPDFLoader(file_path)
        pdf_docs = pdf_loader.load()
        pdf_text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=2000)
        pdf_split = pdf_text_splitter.split_documents(pdf_docs)
        pdf_text = [node.page_content for node in pdf_split]
        return pdf_text
    
    def main_parse(self):
        file_names = self.get_file()
        if file_names[0].startswith("issb"):
            all_node = []
            for file_name in file_names:
                print(file_name)
                file_path = os.path.join(self.folder_path, file_name)
                markdown_docs = self.do_llama_parse(file_path)
                nodes = self.parse_node(markdown_docs)
                nodes_text = [node.text for node in nodes]
                all_node.extend(nodes_text)
        else:
            all_node = self.do_pypdf()
        return all_node
        
if __name__ == "__main__":
    nodes = parse_pdf('2024').main_parse()


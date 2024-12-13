import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class parse_conclusion:
    def __init__(self, lang):
        self.folder_path = "/Users/seanchen/Sean/sustainability_rag/result"
        self.lang = lang

    def text_split(self):
        file_names = os.listdir(self.folder_path)
        for file_name in file_names:
            if file_name.startswith(self.lang):
                print(file_name)
                file_path = os.path.join(self.folder_path, file_name)
                with open(file_path, 'rb') as f:
                    file = f.read()
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=2000)
                docs = [Document(page_content=file)]
                split_txt = text_splitter.split_documents(docs)
        return split_txt
    
if __name__ == "__main__":
    pdf_text = parse_conclusion('en').text_split()
    print(pdf_text[0])
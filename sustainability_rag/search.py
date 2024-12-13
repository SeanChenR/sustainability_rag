from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

class search:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = QdrantVectorStore.from_existing_collection(
            url="http://localhost:6333",
            collection_name="sustainability_data",
            embedding=self.embeddings,
        )
        self.retriever = self.vector_store.as_retriever()
    
    def get_res(self, company_report):
        template = """
        請根據{context}中的永續報告書的框架規範來詳細評價我提供給你的企業報告書內容，可以提及符合哪些IFRS框架的規範。
        請直接告訴我評價的內容即可，不要評價未提及的內容。
        企業報告書內容：{report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = (
            RunnableParallel({"context": self.retriever, "report": RunnablePassthrough()})
            | prompt
            | self.llm
        )
        response = chain.invoke(company_report).content
        return response

    def get_res_en(self, company_report):
        template = """
        Please provide a detailed evaluation of the corporate report content I provide, based on the framework standards outlined in the {context} for sustainability reports. Mention which IFRS framework standards are met.
        Focus only on evaluating the content provided, and avoid commenting on aspects not mentioned.
        Corporate report content: {report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = (
            RunnableParallel({"context": self.retriever, "report": RunnablePassthrough()})
            | prompt
            | self.llm
        )
        response = chain.invoke(company_report).content
        return response
    
    def get_conclusion(self, company_report):
        template = """
        將以下企業永續報告書的評價結果做一個完整的總結，什麼內容符合IFRS的什麼規範一併保留。
        評價結果如下：{report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        response = chain.invoke(company_report).content
        return response
    
    def get_conclusion_en(self, company_report):
        template = """
        Please provide a comprehensive summary of the evaluation results for the corporate sustainability report below, including details of which content complies with specific IFRS standards.  
        Evaluation results are as follows: {report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        response = chain.invoke(company_report).content
        return response
    
    def get_conclusion_en2ch(self, company_report):
        template = """
        Please translate the following corporate sustainability report evaluation into Traditional Chinese.  
        Corporate evaluation content: {report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        response = chain.invoke(company_report).content
        return response
    
    def get_translate(self, company_report):
        template = """
        將以下企業永續報告書的內容翻譯成英文。
        需翻譯的內容如下：{report}
        """
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.llm
        response = chain.invoke(company_report).content
        return response
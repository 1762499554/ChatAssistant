from langchain_community.vectorstores import Chroma
from vector_db.file_process import FileProcessor
from langchain_huggingface import HuggingFaceEmbeddings

class DataVector:
    def __init__(self, model_name="shibing624/text2vec-base-chinese"):
        self.vectors = []
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.fileprocessor = FileProcessor()
    def datavector(self, persist_directory="../data/vector_base"):

        chunks = self.fileprocessor.process()

        vectorstore = Chroma.from_documents(chunks, self.embeddings,
                                            persist_directory=persist_directory)  # 本地存储到向量数据库的地址

        # vectorstore.persist()  //新版本会自动持久化，不再需要这行代码
        return vectorstore

if __name__ == '__main__':
    # 测试是否嵌入成功
    query = "你是谁？"  # 测试问句
    datavecotrv = DataVector()
    doc = datavecotrv.datavector().similarity_search(query)
    print(doc[0].page_content)
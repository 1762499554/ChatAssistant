# 多线程加载大文件夹
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class FileProcessor:
    def __init__(self, directory="../data/source_data/", glob="**/*.docx"):
        # # 获取当前工作目录
        # cwd = os.getcwd()
        # print(f"当前工作目录: {cwd}")
        #
        # # 构建完整路径
        # full_path = os.path.join(cwd, directory)
        # print(f"尝试加载的完整路径: {full_path}")
        #
        # # 验证路径是否存在
        # if not os.path.exists(full_path):
        #     raise FileNotFoundError(f"目录不存在: {full_path}")
        #
        # # 验证路径是否为目录
        # if not os.path.isdir(full_path):
        #     raise NotADirectoryError(f"不是有效的目录: {full_path}")
        #
        # # 检查目录是否为空
        # if not os.listdir(full_path):
        #     print(f"警告: 目录 {full_path} 为空")
        #
        # # 列出目录中的文件（用于调试）
        # print(f"目录内容: {os.listdir(full_path)}")

        self.loader = DirectoryLoader(path=directory,
            glob=glob,
            use_multithreading=True)  # 启用多线程

    def process(self):
        try:
            docs = self.loader.load()
        except Exception as e:
            print(f"加载失败: {str(e)}")
            docs = []

        # ===== 中文长文本分割 =====
        splitter_zh = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "，"]  # 优先按句分割
        )

        chunks = splitter_zh.split_documents(docs)
        return chunks
if __name__ == '__main__':
    fileprocessor = FileProcessor()
    chunks = fileprocessor.process()
    print(chunks)
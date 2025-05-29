这个项目是一个基于OpenAI的智能聊天助手，具备与用户对话、调用工具（如查询天气、显示地图、发送邮件）等功能，以下是详细介绍：

### 项目结构
```
ChatAssistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── weather.py
│   ├── email_sender.py
│   ├── session_manager.py
├── data/
│   ├── city.json
│   ├── source_data/
├── vector_db/
│   └── __init__.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
├── .env
├── data_vector.py
├── file_process.py
├── model_link.py
├── README.md
```

### 功能模块
1. **模型请求 (`model_link.py`)**
    - 该模块负责与模型进行交互，根据用户输入的消息向模型发起请求。
    - 初始化模型时，会加载环境变量中的`OPENAI_API_KEY`，并使用指定的向量数据库进行相似度搜索，获取相关上下文信息。
    - 定义了多个工具函数，包括`send_email`、`get_weather`和`get_map`，可以在模型回复中调用这些工具。

2. **数据向量处理 (`data_vector.py`)**
    - 使用`langchain_community.vectorstores`中的`Chroma`将文档数据嵌入到向量数据库中。
    - 采用`HuggingFaceEmbeddings`进行文本向量化，使用`shibing624/text2vec-base-chinese`模型。

3. **日志配置 (`logger_config.py`)**
    - 配置日志记录，将日志信息保存到`app.log`文件中。
    - 可以在项目中使用`setup_logger`函数获取日志记录器。

4. **Web界面 (`app.py`)**
    - 使用`streamlit`构建Web界面，实现用户与智能聊天助手的交互。
    - 支持保存会话状态，避免多标签页冲突。
    - 根据模型回复调用相应的工具函数，如查询天气、显示地图、发送邮件等。

### 环境安装
项目需要安装以下依赖库：
```
openai==0.28.1
streamlit==1.37.0
```
同时，需要配置`.env`环境变量，将`.env_sample`重命名为`.env`，并设置`OPENAI_API_KEY`和`AUTHORIZATION_CODE`。

### 项目执行
1. **本地知识库处理**：在目录
```data\source_data```下上传作为知识库的docx文件，运行以下python程序，将文件向量化后存入向量库。
```
data_vector.py
```

2. **终端运行**：在终端中执行以下命令启动项目。
```
streamlit run app.py
```
3. **网页访问**：在浏览器中打开相应的URL，即可使用智能聊天助手。

### 参考链接
- [126邮箱授权码获取](https://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e49998b374173cfe9171305fa1ce630d7f67ac2a5feb28b66796d3b)
- [openai官方示例](https://platform.openai.com/docs/guides/function-calling)

### 思考
项目还提出了开发一款AI机器人（2D / 3D）的设想，该机器人可以实现对话、表达情感（喜怒哀乐）和做出对应动作。
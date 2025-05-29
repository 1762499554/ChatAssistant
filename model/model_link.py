from dotenv import load_dotenv
import os
# from langchain_community.vectorstores import Chroma  //已不使用
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import openai
from utils.logger import setup_logger


class ModelRequest:
    def __init__(self):
        load_dotenv()
        self.logger = setup_logger()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.OPENAI_API_KEY,
                                    base_url="https://api.siliconflow.cn/v1")
        self.embedding_function = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
        self.db = Chroma(persist_directory="data/vector_base", embedding_function=self.embedding_function)

    def request(self, messages, tool_choice=None, k=3):
        if not isinstance(messages, str):
            question = messages[-1]["content"]
            history_text = " ".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            doc = self.db.similarity_search(history_text, k=k)
            try:
                context = doc[0].page_content
            except Exception as e:
                context = doc
                self.logger.warning(f"Exception occurred: {e}")

        else:
            question = messages
            doc = self.db.similarity_search(messages, k=k)
            context = doc

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send an email to the specified email with the subject and content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "FromEmail": {
                                "type": "string",
                                "description": "The email address, eg., remember0101@126.com",
                            },
                            "Subject": {
                                "type": "string",
                                "description": "Subject of the email",
                            },
                            "Body": {
                                "type": "string",
                                "description": "The content of the email",
                            },
                            "Recipients": {
                                "type": "string",
                                "description": "The recipients' email addresses",
                            }
                        },
                        "required": ["FromEmail", "Subject", "Body", "Recipients"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the weather forecast for today in the city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name, eg., 北京",
                            }
                        },
                        "required": ["city"],
                    },
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_map",
                    "description": "get the special map of city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The city name, eg., 北京",
                            }
                        },
                        "required": ["city"],
                    },
                }
            }
        ]

        prompt = [
            {"role": "system", "content": f"你是一名问答助手，优先使用以下片段{context}去回答问题."},
            {"role": "user", "content": question}
        ]

        try:
            self.logger.info(f"请求模型的信息:{messages}")
            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V2.5",
                messages=prompt,
                tools=tools,
                tool_choice=tool_choice,
                temperature=0.8
            )
            self.logger.info(f"模型回复信息:{response}")
            return response
        except Exception as e:
            self.logger.error("Unable to generate ChatCompletion response")
            self.logger.error(f"Exception: {e}")
            return e


if __name__ == '__main__':
    model = ModelRequest()
    response = model.request("你是谁")
    print(response)
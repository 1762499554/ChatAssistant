import streamlit as st
from app.weather import WeatherService
from app.email_sender import EmailSender
from app.map import Map
from app.session_manager import SessionManager
from model.model_link import ModelRequest
import os
from utils.logger import setup_logger
import json

# 初始化会话管理器
session_manager = SessionManager()
# 初始化日志
logger = setup_logger()

print("-----------------新运行----------------------")
logger.info("-----------------新运行----------------------")

# 设置页面标题和图标
st.set_page_config(
    page_title="智能聊天助手",
    page_icon="💬",
    layout="wide"
)

# 应用标题
st.title("智能聊天助手")

# 显示聊天历史
for message in session_manager.get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 保存用户消息
    session_manager.add_user_message(prompt)

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用模型请求
    model = ModelRequest()
    response = model.request(session_manager.get_messages())
    try:
        if content := response.choices[0].message.content:
            with st.chat_message("assistant"):
                st.markdown(content)
                session_manager.add_assistant_message(content)
                session_manager.update_show_weather(False)
                session_manager.update_show_map(False)
                session_manager.update_show_email(False)
        else:
            fun_name = response.choices[0].message.tool_calls[0].function.name
            fun_args = response.choices[0].message.tool_calls[0].function.arguments
            fun_args = json.loads(fun_args)

            # 存储对应函数的参数
            if fun_name == "get_weather":
                session_manager.update_weather_args(fun_args)
                session_manager.update_show_weather(True)
                session_manager.update_show_map(False)
                session_manager.update_show_email(False)

            elif fun_name == "get_map":
                session_manager.update_map_args(fun_args)
                session_manager.update_show_weather(False)
                session_manager.update_show_map(True)
                session_manager.update_show_email(False)
            elif fun_name == "send_email":
                session_manager.update_email_args(fun_args)
                session_manager.update_show_weather(False)
                session_manager.update_show_map(False)
                session_manager.update_show_email(True)
    except IndexError:
        with st.chat_message("assistant"):
            st.markdown("模型连接超时，请再试一次")


if session_manager.get_show_weather():
    args = session_manager.get_weather_args()
    weather_service = WeatherService()
    weather_info = weather_service.get_weather(args["city"])
    with st.chat_message("assistant"):
        st.markdown(weather_info)
        session_manager.add_assistant_message(weather_info)
    session_manager.update_show_weather(False)

if session_manager.get_show_map():
    args = session_manager.get_map_args()
    sitemap = Map(args["city"])
    map_info = sitemap.showmap()
    st.markdown(map_info)
    # 保存助手回复
    session_manager.add_assistant_message(map_info)
    session_manager.update_show_map(False)

if session_manager.get_show_email():
    args = session_manager.get_email_args()
    with (st.chat_message("assistant")):
        st.markdown("请确认以下邮件信息：")
        email_from = args["FromEmail"]
        email_to = args["Recipients"]
        email_subject = args["Subject"]
        email_body = args["Body"]

        # 创建邮件表单
        with st.form("email_form"):
            sender_email = st.text_input("发件人", value=email_from)
            recipient_email = st.text_input("收件人", value=email_to)
            subject = st.text_input("主题", value=email_subject)
            body = st.text_area("内容", value=email_body)

            # 提交表单并获取数据
            submitted = st.form_submit_button(label="✅确认发送邮件")
            cancel = st.form_submit_button(label="❌取消发送邮件")

            # print(f"邮件参数：{sender_email}, {recipient_email}, {subject}, {body}")
        # print(f"点击确认后：{submitted}")
        if submitted:
            email_sender = EmailSender()
            try:
                # 使用表单中用户修改后的数据
                email_sender.send_email(
                    sender_email,
                    recipient_email,
                    subject,
                    body
                )
                st.success("邮件已发送")
                session_manager.add_assistant_message("邮件已发送，还需要什么帮助吗？")
                logger.info(f"邮件确认发送: 从 {sender_email} 到 {recipient_email}, 主题: {subject}")
            except Exception as e:
                st.error(f"邮件发送失败: {str(e)}")
                session_manager.add_assistant_message(f"邮件发送失败: {str(e)}")
                logger.error(f"邮件确认发送失败: {str(e)}")
            session_manager.update_show_email(False)
            st.rerun()

        # 取消按钮逻辑
        # print(f"点击取消后：{cancel}")
        if cancel:
            st.warning("邮件发送已取消")
            session_manager.add_assistant_message("邮件已取消，还需要什么帮助吗？")
            logger.info("邮件发送已取消")
            session_manager.update_show_email(False)  # 设置邮件状态为False
            st.rerun()   # 强制刷新页面，隐藏表单


# 侧边栏显示历史对话
with st.sidebar:
    st.header("历史对话")
    if not st.session_state.messages:
        st.write("暂无对话")
    else:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"**用户 {i + 1}:** {msg['content']}")
            else:
                st.markdown(f"**助手 {i + 1}:** {msg['content']}")

# 新增：手动清除会话功能（可选）
if st.sidebar.button("清除会话数据"):
    try:
        os.remove(session_manager.STATE_FILE)
    except FileNotFoundError:
        st.sidebar.success("会话数据已清除")
    st.session_state.clear()
    st.sidebar.success("会话数据已清除")
    st.rerun()


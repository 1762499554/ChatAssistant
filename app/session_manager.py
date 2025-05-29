import os
import json
import uuid
from utils.logger import setup_logger
import streamlit as st


class SessionManager:
    def __init__(self):
        self.logger = setup_logger()
        self.STATE_FILE = "data/session_state.json"
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        self.saved_state = self.load_session_state()
        st.session_state.messages = self.saved_state.get("messages", [])
        st.session_state.show_weather = self.saved_state.get("show_weather", False)
        st.session_state.show_map = self.saved_state.get("show_map", False)
        st.session_state.show_email = self.saved_state.get("show_email", False)
        st.session_state.weather_args = self.saved_state.get("weather_args", {})
        st.session_state.map_args = self.saved_state.get("map_args", {})
        st.session_state.email_args = self.saved_state.get("email_args", {})

    def load_session_state(self):
        if os.path.exists(self.STATE_FILE):
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                try:
                    file = json.load(f)
                    return file
                except json.decoder.JSONDecodeError:
                    return {}
        return {}

    def save_session_state(self):
        state = {
            "session_id": st.session_state.session_id,
            "messages": st.session_state.messages,
            "show_weather": st.session_state.show_weather,
            "show_map": st.session_state.show_map,
            "show_email": st.session_state.show_email,
            "weather_args": st.session_state.weather_args,
            "map_args": st.session_state.map_args,
            "email_args": st.session_state.email_args
        }
        with open(self.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)

    def add_user_message(self, message):
        st.session_state.messages.append({"role": "user", "content": message})
        self.save_session_state()
        self.logger.info(f"用户输入: {message}")

    def add_assistant_message(self, message):
        st.session_state.messages.append({"role": "assistant", "content": message})
        self.save_session_state()
        self.logger.info(f"助手回复: {message}")

    def get_messages(self):
        return st.session_state.messages

    def update_show_weather(self, message):
        st.session_state.show_weather = message
        self.save_session_state()
        self.logger.info(f"是否获取天气：{message}")

    def get_show_weather(self):
        return st.session_state.show_weather

    def update_weather_args(self, message):
        st.session_state.weather_args = message
        self.save_session_state()
        self.logger.info(f"天气参数：{message}")

    def get_weather_args(self):
        return st.session_state.weather_args

    def update_show_map(self, message):
        st.session_state.show_map = message
        self.save_session_state()
        self.logger.info(f"是否获取地图：{message}")

    def get_show_map(self):
        return st.session_state.show_map

    def update_map_args(self, message):
        st.session_state.map_args = message
        self.save_session_state()
        self.logger.info(f"地图参数：{message}")

    def get_map_args(self):
        return st.session_state.map_args

    def update_show_email(self, message):
        st.session_state.show_email = message
        self.save_session_state()
        self.logger.info(f"是否发送邮件: {message}")

    def get_show_email(self):
        return st.session_state.show_email

    def update_email_args(self, message):
        st.session_state.email_args = message
        self.save_session_state()
        self.logger.info(f"邮件参数: {message}")

    def get_email_args(self):
        return st.session_state.email_args

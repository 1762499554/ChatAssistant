import streamlit as st
from app.email_sender import EmailSender

# 初始化会话状态
if 'email_form_data' not in st.session_state:
    st.session_state.email_form_data = {}
if 'email_submitted' not in st.session_state:
    st.session_state.email_submitted = False

if prompt := st.chat_input("请输入您的问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown("请确认以下邮件信息：")
        email_from = "assistant@example.com"
        email_to = "recipient@example.com"
        email_subject = "test"
        email_body = "test"


        # 创建邮件表单
        with st.form("email_form"):
            sender_email = st.text_input("发件人", value=email_from)
            recipient_email = st.text_input("收件人", value=email_to)
            subject = st.text_input("主题", value=email_subject)
            body = st.text_input("内容", value=email_body)

            # 使用回调函数的提交按钮
            on_submit = st.form_submit_button("✅确认发送邮件")
            off_submit = st.form_submit_button("❌取消发送邮件")
            print(sender_email, recipient_email, subject, body)
            print(on_submit)
            print(off_submit)

            # 取消按钮逻辑
            if off_submit:
                st.warning("邮件发送已取消")

            if on_submit:
                email_sender = EmailSender()
                try:
                    email_sender.send_email(sender_email,recipient_email,subject,body)
                    st.success("邮件已发送")
                except Exception as e:
                    st.error(f"邮件发送失败: {str(e)}")

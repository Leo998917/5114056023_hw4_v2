import streamlit as st
from datetime import date
import requests
import json

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🧳"
)

st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption("Generative AI × Gemini (REST API)")

# =====================
# Gemini API Key（作業寫死 OK）
# =====================
GEMINI_API_KEY = "AIzaSyC63w_OUrzcg5EEVpihlj9FGKAIzQa30KA"

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-pro-latest:generateContent"
)


# =====================
# User Input
# =====================
city = st.text_input("旅遊城市", "Tokyo")
start_date = st.date_input("出發日期", date.today())
days = st.slider("旅遊天數", 1, 7, 3)

preference = st.multiselect(
    "旅遊偏好",
    ["美食", "拍照", "文化", "購物"],
    default=["美食", "拍照"]
)

# =====================
# Prompt
# =====================
prompt = f"""
你是一個專業的旅遊規劃 AI Agent。

城市：{city}
日期：{start_date}
天數：{days}
偏好：{', '.join(preference)}

請產生每天「早上 / 下午 / 晚上」的旅遊行程，
並附上旅遊小提醒，使用繁體中文。
"""

# =====================
# Generate
# =====================
if st.button("生成旅遊行程"):
    with st.spinner("Gemini AI 規劃中..."):
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            result = response.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(text)
        else:
            st.error("Gemini API 呼叫失敗")
            st.code(response.text)

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")

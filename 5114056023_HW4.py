import streamlit as st
from datetime import date
import requests
import json

st.set_page_config(
    page_title="AI Travel Planner (Gemini)",
    page_icon="🧳"
)

st.title("🧳 AI 時間與地點感知旅遊行程生成系統 - Gemini")
st.caption("Generative AI × Gemini (REST API)")

# =====================
# API Key 從 Streamlit Secrets 讀取
# =====================
if "GEMINI_API_KEY" not in st.secrets:
    st.warning("請在 Streamlit Cloud 的 Settings → Secrets 設定 GEMINI_API_KEY")
    st.stop()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# =====================
# 請填入你實際可用的 Gemini 模型名稱
# 例如：gemini-1.5-pro 或 gemini-1.5-flash
# =====================
GEMINI_MODEL = "gemini-1.5-pro"  # 請確認你的 Key 可使用此模型

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"

# =====================
# 使用者輸入
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
# 生成行程
# =====================
if st.button("生成旅遊行程"):
    with st.spinner("Gemini AI 規劃中..."):
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if response.status_code == 200:
            result = response.json()
            try:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(text)
            except:
                st.error("API 回傳格式異常，請確認模型與 Key 是否正確")
                st.code(response.text)
        else:
            st.error("Gemini API 呼叫失敗")
            st.code(response.text)

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")


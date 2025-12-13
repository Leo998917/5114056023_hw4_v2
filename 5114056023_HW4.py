import streamlit as st
from datetime import date
from openai import OpenAI

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🧳"
)

st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption("Generative AI × LLM (OpenAI)")

# =====================
# API Key 從 Streamlit Secrets 讀取
# =====================
if "OPENAI_API_KEY" not in st.secrets:
    st.warning("請在 Streamlit Cloud 的 Settings → Secrets 設定 OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    with st.spinner("AI 規劃中..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是專業旅遊規劃 AI"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content
        st.markdown(result)

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")

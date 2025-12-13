import streamlit as st
from datetime import date
import google.generativeai as genai

# =====================
# Streamlit Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner (Gemini)",
    page_icon="🧳",
    layout="centered"
)

st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption("Generative AI × Gemini × Agent-based Design")

# =====================
# Gemini API Key (Streamlit Secrets)
# =====================
genai.configure(api_key=st.secrets["AIzaSyC63w_OUrzcg5EEVpihlj9FGKAIzQa30KA"])

model = genai.GenerativeModel("gemini-1.5-flash")

# =====================
# User Input
# =====================
city = st.text_input("📍 旅遊城市", "Tokyo")
start_date = st.date_input("📅 出發日期", date.today())
days = st.slider("🗓️ 旅遊天數", 1, 7, 3)

preference = st.multiselect(
    "🎯 旅遊偏好",
    ["美食", "拍照", "文化", "親子", "自然", "購物"],
    default=["美食", "拍照"]
)

# =====================
# Prompt Builder (Agent Concept)
# =====================
def build_prompt(city, start_date, days, preference):
    return f"""
你是一個專業的旅遊規劃 AI Agent，
請根據以下條件生成完整旅遊行程與攻略：

【旅遊資訊】
- 城市：{city}
- 出發日期：{start_date}
- 旅遊天數：{days} 天
- 旅遊偏好：{', '.join(preference)}

【規劃規則】
1. 每一天請分為：早上 / 下午 / 晚上
2. 行程需考慮地理合理性與移動距離
3. 結合生成式 AI 自然語言敘述
4. 最後請附上「旅遊小提醒」
5. 使用繁體中文輸出

請直接輸出完整旅遊行程與攻略內容。
"""

# =====================
# Generate Button
# =====================
if st.button("✨ 生成旅遊行程"):
    with st.spinner("Gemini AI 正在規劃行程中..."):
        prompt = build_prompt(city, start_date, days, preference)

        response = model.generate_content(prompt)
        result = response.text

    st.success("行程生成完成！")
    st.markdown(result)

# =====================
# Footer
# =====================
st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU｜Powered by Google Gemini")

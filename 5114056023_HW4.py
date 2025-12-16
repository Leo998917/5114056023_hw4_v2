import streamlit as st
from datetime import date
import google.generativeai as genai

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner (Gemini)",
    page_icon="🧳"
)

st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption("Powered by Google Gemini 1.5 Flash")

# =====================
# API Key 設定 (從 Secrets 讀取)
# =====================
# 檢查有沒有設定 Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("找不到 API Key！請在 Streamlit Cloud 的 Settings → Secrets 設定 GOOGLE_API_KEY")
    st.stop()

# 設定 Google Gemini
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"API Key 設定失敗: {e}")
    st.stop()

# =====================
# 使用者輸入
# =====================
col1, col2 = st.columns(2)

with col1:
    city = st.text_input("旅遊城市", "日本京都")
    days = st.slider("旅遊天數", 1, 7, 3)

with col2:
    start_date = st.date_input("出發日期", date.today())
    preference = st.multiselect(
        "旅遊偏好",
        ["美食", "拍照", "文化", "購物", "放鬆"],
        default=["美食", "文化"]
    )

# =====================
# Prompt 設計
# =====================
prompt = f"""
你是一個專業的旅遊規劃 AI Agent。

請根據以下資訊規劃行程：
- 目的地：{city}
- 日期：{start_date} 出發
- 天數：{days} 天
- 偏好：{', '.join(preference)}

任務要求：
1. 請產生每天「早上 / 下午 / 晚上」的具體行程。
2. 推薦真實存在的餐廳或景點。
3. 請使用繁體中文回答。
4. 格式請用 Markdown 整理清晰，重點景點請用粗體標示。
"""

# =====================
# 生成行程 (使用 Gemini 1.5 Flash)
# =====================
if st.button("生成旅遊行程"):
    with st.spinner("Gemini 正在為您規劃夢幻行程..."):
        try:
            # 1. 初始化模型 (使用目前最快且免費的 flash 模型)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 2. 發送請求
            response = model.generate_content(prompt)
            
            # 3. 顯示結果
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"生成失敗: {e}")
            st.info("若出現 404 錯誤，請確認 API Key 是否正確，且該 Google 帳號有權限使用 Gemini API。")

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")
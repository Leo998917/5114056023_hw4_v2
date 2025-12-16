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
st.caption("Powered by Google Gemini (Auto-Fallback)")

# =====================
# API Key 設定
# =====================
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
# 核心功能：智慧模型切換 (Smart Fallback)
# =====================
def generate_content_safe(prompt_text):
    # 定義嘗試順序：先試最快的 Flash，不行就換穩定的 Pro
    models_to_try = ['gemini-1.5-flash', 'gemini-pro']
    
    errors = []
    
    for model_name in models_to_try:
        try:
            # 建立模型實例
            model = genai.GenerativeModel(model_name)
            # 嘗試生成
            response = model.generate_content(prompt_text)
            return response.text, model_name # 成功就回傳結果和使用的模型
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue # 失敗就試下一個
            
    # 如果都失敗，拋出最後一個錯誤
    raise Exception(f"所有模型皆嘗試失敗。\n詳細錯誤: {errors}")

# =====================
# 觸發按鈕
# =====================
if st.button("生成旅遊行程"):
    with st.spinner("AI 正在規劃中 (自動選擇最佳模型)..."):
        try:
            result_text, used_model = generate_content_safe(prompt)
            
            st.success(f"✅ 行程生成成功！(使用模型: {used_model})")
            st.markdown("---")
            st.markdown(result_text)
            
        except Exception as e:
            st.error("生成失敗，請檢查 API Key 權限。")
            st.expander("查看錯誤詳情").write(e)

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")
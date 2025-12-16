import streamlit as st
from datetime import date
import google.generativeai as genai

# =====================
# 1. Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner (Auto-Detect)",
    page_icon="🧳"
)

# =====================
# 2. 安全性與 API 設定
# =====================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ 錯誤：未偵測到 API Key。請在 Streamlit Cloud 的 Settings → Secrets 設定 GOOGLE_API_KEY")
    st.stop()

# 設定 Gemini
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"❌ API Key 設定失敗: {e}")
    st.stop()

# =====================
# 3. 核心邏輯：自動偵測可用模型 (這是成功的關鍵！)
# =====================
target_model_name = ""
try:
    # 找出所有支援 'generateContent' 的模型
    available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        st.error("❌ 您的 API Key 連線成功，但該帳號沒有任何可用的模型權限 (Access Denied)。")
        st.stop()
    
    # 自動選用第一個可用的模型 (例如 'models/gemini-pro')
    target_model_object = available_models[0]
    target_model_name = target_model_object.name
    
except Exception as e:
    st.error(f"❌ 無法取得模型清單 (可能原因：API Key 錯誤或網路問題): {e}")
    st.stop()

# =====================
# 4. UI 介面
# =====================
st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption(f"🚀 System Status: Online | Using Model: `{target_model_name}`") # 顯示抓到的模型

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
# 5. Prompt 設計
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
# 6. 生成行程
# =====================
if st.button("生成旅遊行程"):
    with st.spinner(f"正在呼叫 {target_model_name} 為您規劃..."):
        try:
            # 使用剛剛自動抓到的模型名稱來初始化
            model = genai.GenerativeModel(target_model_name)
            
            # 發送請求
            response = model.generate_content(prompt)
            
            # 顯示結果
            st.markdown("---")
            st.markdown(response.text)
            st.success("✅ 行程生成完成！")
            
        except Exception as e:
            st.error(f"生成失敗: {e}")
            st.info("若出現錯誤，請確認您的 API 額度是否足夠。")

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")
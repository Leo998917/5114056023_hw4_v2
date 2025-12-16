import streamlit as st
from datetime import date
import google.generativeai as genai

# =====================
# 1. Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner (Final)",
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
# 3. 核心邏輯：智慧選擇最佳模型 (解決 429 錯誤的關鍵)
# =====================
target_model_name = ""
try:
    # 1. 找出帳號能用的所有模型
    available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    all_model_names = [m.name for m in available_models]
    
    if not available_models:
        st.error("❌ 您的 API Key 連線成功，但該帳號沒有任何可用的模型權限。")
        st.stop()
    
    # 2. 設定優先順序 (Priority)
    # 我們最想要 gemini-1.5-flash (速度快、額度高，每分鐘 15 次)
    # 我們最不想要 gemini-2.0-flash-exp (實驗版，每分鐘只有 5 次，容易報錯)
    
    if "models/gemini-1.5-flash" in all_model_names:
        target_model_name = "models/gemini-1.5-flash"
    elif "models/gemini-pro" in all_model_names:
        target_model_name = "models/gemini-pro"
    else:
        # 真的都沒有，才勉強用列表中的第一個
        target_model_name = all_model_names[0]
    
except Exception as e:
    st.error(f"❌ 無法取得模型清單: {e}")
    st.stop()

# =====================
# 4. UI 介面
# =====================
st.title("🧳 AI 時間與地點感知旅遊行程生成系統")
st.caption(f"🚀 System Online | 使用模型: `{target_model_name}` (已優化連線額度)")

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
            # 初始化模型
            model = genai.GenerativeModel(target_model_name)
            
            # 發送請求
            response = model.generate_content(prompt)
            
            # 顯示結果
            st.markdown("---")
            st.markdown(response.text)
            st.success("✅ 行程生成完成！")
            
        except Exception as e:
            # 這裡特別抓出 429 錯誤來提示使用者
            error_msg = str(e)
            if "429" in error_msg:
                st.error("⏳ 生成速度過快 (429 Too Many Requests)。請等待約 30 秒後再試一次。")
            else:
                st.error(f"生成失敗: {error_msg}")

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")
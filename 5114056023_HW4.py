import streamlit as st
from datetime import date
import google.generativeai as genai

# =====================
# 1. Page Config
# =====================
st.set_page_config(
    page_title="AI Travel Planner (Pro)",
    page_icon="🧳",
    layout="wide"
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
    # 找出帳號能用的所有模型
    available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    all_model_names = [m.name for m in available_models]
    
    if not available_models:
        st.error("❌ 您的 API Key 連線成功，但該帳號沒有任何可用的模型權限。")
        st.stop()
    
    # 設定優先順序：優先使用 1.5 Flash (速度快、額度高)
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
st.title("🧳 AI 智慧旅遊行程規劃師")
st.caption(f"🚀 System Status: Online | 使用模型: `{target_model_name}`")

col1, col2 = st.columns([1, 1])

with col1:
    city = st.text_input("📍 您想去哪裡旅遊？", "日本京都")
    days = st.slider("🗓️ 旅遊天數", 1, 10, 5)
    start_date = st.date_input("📅 出發日期", date.today())

with col2:
    # 定義 20 種豐富的旅遊風格標籤
    tags_options = [
        "美食探店 🍜", "歷史古蹟 🏯", "自然風景 🌲", "網美攝影 📸", 
        "購物血拼 🛍️", "放鬆療癒 💆", "親子同遊 👨‍👩‍👧‍👦", "文化藝術 🎨", 
        "冒險挑戰 🧗", "浪漫情侶 💑", "奢華享受 💎", "小資窮遊 💰", 
        "建築巡禮 🏛️", "博物館迷 🏛️", "熱鬧夜生活 🍸", "溫泉泡湯 ♨️", 
        "秘境探索 🗺️", "海島度假 🏖️", "登山健行 🥾", "在地體驗 🏘️"
    ]
    
    preference = st.multiselect(
        "🏷️ 選擇您的旅遊偏好 (可複選)",
        tags_options,
        default=["美食探店 🍜", "歷史古蹟 🏯"]
    )

# =====================
# 5. Prompt 設計
# =====================
prompt = f"""
你是一個擁有 20 年經驗的專業旅遊規劃 AI Agent。

請根據以下資訊，為使用者規劃一份詳細的旅遊行程：
- 目的地：{city}
- 日期：{start_date} 出發
- 天數：{days} 天
- 偏好風格：{', '.join(preference)}

任務要求：
1. 請產生從 Day 1 到 Day {days} 的完整行程。
2. 每天請分為「上午」、「下午」、「晚上」三個時段。
3. 針對使用者的「偏好風格」推薦最適合的景點與餐廳 (必須是真實存在的)。
4. 請提供每個景點之間的簡短交通建議。
5. 最後請附上 3 個針對該城市的「在地旅遊小貼士」(天氣、交通卡、禮儀等)。
6. 格式請用 Markdown 整理清晰，景點名稱請用 **粗體** 標示。
7. 請使用繁體中文回答。
"""

# =====================
# 6. 生成行程
# =====================
if st.button("🚀 開始生成夢幻行程"):
    if not city:
        st.warning("請輸入旅遊城市！")
        st.stop()
        
    with st.spinner(f"正在呼叫 {target_model_name} 為您規劃專屬行程..."):
        try:
            # 初始化模型
            model = genai.GenerativeModel(target_model_name)
            
            # 發送請求
            response = model.generate_content(prompt)
            
            # 顯示結果
            st.success("✅ 行程生成完成！祝您旅途愉快！")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("⏳ 呼叫太頻繁 (429 Too Many Requests)，請等待約 30 秒後再試。")
            else:
                st.error(f"生成失敗: {error_msg}")

st.markdown("---")
st.caption("TAICA AIGC 課程專題｜NCCU")
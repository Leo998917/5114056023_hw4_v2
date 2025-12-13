import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# ================= ⚠️ 安全設定 ⚠️ =================
# 在這裡填入你的 API Key
# 注意：上傳 GitHub 前請務必刪除此行，或改用 st.secrets，否則 Key 會外洩！
GOOGLE_API_KEY = "AIzaSyBeFmDMw6bDQ68Ofap6qwq2YVFy3xl2Hgc" 

# ================= 配置設定 =================
st.set_page_config(page_title="TravelGenie ✈️ 智慧旅遊規劃師 (Gemini版)", page_icon="✈️")

# 側邊欄 (只保留作者資訊，不再需要輸入 Key)
with st.sidebar:
    st.header("關於專案")
    st.markdown("此專題為 **Taica AIGC 課程** 作業展示")
    st.markdown("Powered by **Google Gemini**")
    st.markdown("Developed by [Your Name]")

# ================= 主介面設計 =================
st.title("🌍 TravelGenie 智慧旅遊規劃師")
st.markdown("### 輸入您的時間與地點，為您生成專屬旅遊攻略")

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("📍 您想去哪裡旅遊？", "日本京都")
    travel_style = st.selectbox(
        "🎒 您的旅遊風格是？",
        ["輕鬆慢活 (Relaxing)", "緊湊充實 (Packed)", "美食探店 (Foodie)", "文化歷史 (Cultural)", "親子同遊 (Family)"]
    )

with col2:
    travel_dates = st.date_input("📅 選擇旅遊日期範圍", [])
S
# ================= 核心邏輯 (Agent) =================
def generate_itinerary(dest, dates, style):
    # 使用全域變數的 API Key
    if not GOOGLE_API_KEY or "貼在這裡" in GOOGLE_API_KEY:
        return "⚠️ 請先在程式碼中填入正確的 Google API Key！"
    
    try:
        # 初始化 Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.7, 
            google_api_key=GOOGLE_API_KEY
        )
    except Exception as e:
        return f"API 設定錯誤: {str(e)}"

    # 計算天數
    if len(dates) == 2:
        start_date = dates[0]
        end_date = dates[1]
        days = (end_date - start_date).days + 1
        date_info = f"從 {start_date} 到 {end_date}，共 {days} 天"
    else:
        return "⚠️ 請選擇完整的開始與結束日期。"

    # Prompt 設計
    template = """
    你是一位擁有 20 年經驗的專業在地導遊與旅遊規劃師。
    請根據以下使用者的需求，規劃一份詳細的旅遊行程：

    **使用者需求：**
    - 目的地：{destination}
    - 時間範圍：{date_info}
    - 旅遊風格：{style}

    **你的任務：**
    1. 請為每一天規劃「上午」、「下午」、「晚上」的行程。
    2. 包含推薦的景點、必吃美食（請提供具體餐廳名稱）。
    3. 提供點對點之間的簡單交通建議。
    4. 根據「{style}」調整行程的節奏。
    
    **輸出格式要求：**
    - 請使用 Markdown 格式。
    - 每一天請用 H3 標題 (### 第 X 天：主題)。
    - 重要地點請用 **粗體** 標示。
    - 最後請附上一段 100 字以內的「旅遊小貼士」(天氣、穿著、注意事項)。

    開始規劃：
    """

    prompt = PromptTemplate(
        input_variables=["destination", "date_info", "style"],
        template=template
    )

    chain = prompt | llm
    
    with st.spinner('🤖 Gemini 導遊正在為您規劃行程中，請稍候...'):
        try:
            response = chain.invoke({
                "destination": dest,
                "date_info": date_info,
                "style": style
            })
            return response.content
        except Exception as e:
            return f"生成失敗，請檢查 API Key 是否正確。\n錯誤訊息: {e}"

# ================= 觸發按鈕 =================
if st.button("🚀 開始生成行程"):
    if destination and len(travel_dates) == 2:
        # 不再需要從前端傳入 API Key
        result = generate_itinerary(destination, travel_dates, travel_style)
        st.markdown("---")
        st.markdown(result)
    else:
        st.error("請確認「目的地」與「日期範圍」皆已填寫完整。")
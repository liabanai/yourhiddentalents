import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("<style>.stApp { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר API KEY ב-Secrets")
    st.stop()

# 3. מציאת המודל הזמין (התיקון לבאג ה-404)
if "model_name" not in st.session_state:
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # סדר עדיפויות: ננסה פלאש, אם לא אז פרו, אם לא אז הראשון ברשימה
        if 'models/gemini-1.5-flash' in available_models:
            st.session_state.model_name = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro' in available_models:
            st.session_state.model_name = 'models/gemini-pro'
        else:
            st.session_state.model_name = available_models[0]
    except:
        st.session_state.model_name = 'gemini-pro' # ברירת מחדל אחרונה

# 4. הוראות מערכת
SYSTEM_PROMPT = "You are a professional coach for the Zone of Genius. Conduct the session in Hebrew if the user chooses so."

# 5. ניהול שיחה
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "ברוך הבא! באיזו שפה נתחיל? (עברית / English)"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("הקלד/י כאן..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # שימוש בשם המודל שמצאנו באופן דינמי
        model = genai.GenerativeModel(model_name=st.session_state.model_name, system_instruction=SYSTEM_PROMPT)
        
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        
        response = model.generate_content(history)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"שגיאה: {e}")

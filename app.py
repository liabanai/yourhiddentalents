import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה ויישור לימין (RTL)
st.set_page_config(page_title="Genius Zone Coach", layout="centered")

# הוספת CSS לתיקון יישור לימין באופן גורף
st.markdown("""
    <style>
    /* הגדרת כיווניות כללית לאפליקציה */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* יישור הודעות הצ'אט */
    div[data-testid="stChatMessageContent"] {
        text-align: right;
        direction: rtl;
    }
    /* יישור תיבת הקלט */
    div[data-testid="stChatInput"] textarea {
        text-align: right;
        direction: rtl;
    }
    /* עיצוב כפתורים */
    .stButton button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        height: 3em;
    }
    /* התאמת כותרות */
    h1, h2, h3 {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API וזיהוי מודל
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    if "model_name" not in st.session_state:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.session_state.model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else 'models/gemini-pro'
except:
    st.error("שגיאה בחיבור ל-API. וודאו שהמפתח מוזן ב-Secrets.")
    st.stop()

# 3. הוראות המערכת (The System Prompt)
SYSTEM_PROMPT = """
You are an elite performance coach specializing in Dr. Gay Hendricks' 'Zone of Genius'. 
- Conduct the session ONLY in the language chosen by the user.
- Ask the 4 questions ONE BY ONE. Wait for a response before proceeding.
- Analysis: After 4 answers, provide: Genius DNA, Excellence Trap, and Genius Statement.
"""

# 4. מסך בחירת שפה
if "language" not in st.session_state:
    st.markdown("### Choose Your Language / בחרו שפה")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("English 🇺🇸"):
            st.session_state.language = "English"
            intro = "We are embarking on a journey to find your 'Zone of Genius'. This is the intersection of your passion, effortless skill, and unique value. Most people live in their 'Zone of Excellence' – doing things they are good at, but which ultimately drain them. Today, we will find what makes you truly unique."
            st.session_state.messages = [{"role": "assistant", "content": intro}]
            st.rerun()
            
    with col2:
        if st.button("עברית 🇮🇱"):
            st.session_state.language = "Hebrew"
            intro = """אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם. רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת."""
            st.session_state.messages = [{"role": "assistant", "content": intro}]
            st.rerun()
    st.stop()

# 5. הצגת היסטוריית הצ'אט
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. לוגיקת הצ'אט
if prompt := st.chat_input("השיבו כאן..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        model = genai.GenerativeModel(model_name=st.session_state.model_name, system_instruction=SYSTEM_PROMPT)
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        response = model.generate_content(history)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"אירעה שגיאה: {e}")

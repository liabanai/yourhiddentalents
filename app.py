import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה וכיווניות (RTL)
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    input, textarea { direction: rtl; text-align: right; }
    div[data-testid="stChatMessageContent"] { text-align: right; }
    .stButton button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API Key עם מנגנון בחירת מודל אוטומטי
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    if "model_name" not in st.session_state:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in available_models:
            st.session_state.model_name = 'models/gemini-1.5-flash'
        else:
            st.session_state.model_name = 'models/gemini-pro'
except:
    st.error("שגיאה: וודאי שה-API Key מוזן ב-Secrets.")
    st.stop()

# 3. הוראות המערכת (הלוגיקה המקצועית)
SYSTEM_PROMPT = """
You are an elite performance coach specializing in Dr. Gay Hendricks' 'Zone of Genius'. 
The user has already seen the introduction. Your task is to conduct the session in the chosen language.

If the language is Hebrew, ask these 4 questions ONE BY ONE (wait for an answer after each one):
1. "מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שאת/ה יכול/ה לעשות במשך שעות ועדיין להרגיש מלא/ה באנרגיה)."
2. "מהו החלק בעבודה שלך שמניב את היחס הגבוה ביותר של תוצאות לעומת זמן שהושקע?"
3. "מהי היכולת הייחודית שלך? (משהו שמרגיש לך כל כך טבעי, שאת/ה לפעמים מניח/ה שכולם יכולים לעשות אותו)."
4. "מהו הערך הייחודי שאת/ה מביא/ה לעולם כשאת/ה במיטבך?"

After the questions, provide 'Analysis Part A' (Genius DNA, Excellence Trap, Genius Statement).
Ask for approval before moving to Part B.
"""

# 4. הודעת פתיחה ובחירת שפה עם כפתורים
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "language" not in st.session_state:
    # הודעת הפתיחה מהתמונה שלך
    st.markdown("""
    ### ברוכים הבאים למסע לגילוי אזור הגאונות שלכם! 
    
    כאן נקלף יחד את שכבות ה'מצוינות' – הדברים שאתם טובים בהם אבל שואבים מכם אנרגיה – כדי לחשוף את ה**גאונות** האמיתית שלכם. 
    זהו המקום שבו הכישרון הייחודי שלכם פוגש תשוקה חסרת מאמץ.
    
    **באיזו שפה תרצו שננהל את התהליך?**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English 🇺🇸"):
            st.session_state.language = "English"
            intro_msg = "Great! Let's start. What is the one thing you love doing the most? (Something that gives you energy)."
            st.session_state.messages.append({"role": "assistant", "content": intro_msg})
            st.rerun()
    with col2:
        if st.button("עברית 🇮🇱"):
            st.session_state.language = "Hebrew"
            intro_msg = "נהדר, בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שאת/ה יכול/ה לעשות במשך שעות ועדיין להרגיש מלא/ה באנרגיה, ולא מרוקנ/ת ממנה)."
            st.session_state.messages.append({"role": "assistant", "content": intro_msg})
            st.rerun()
    st.stop()

# 5. הצגת היסטוריית הצ'אט
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. קלט ותגובה
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
        st.error(f"שגיאה: {e}")

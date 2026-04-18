import streamlit as st
import google.generativeai as genai

# 1. עיצוב ויישור לימין
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp, [data-testid="stChatMessageContent"] { direction: rtl !important; text-align: right !important; }
    h1, h3 { text-align: center !important; }
    .stButton button { width: 100%; border-radius: 25px; font-weight: bold; height: 3.5em; }
    .intro-box { font-size: 1.2rem; line-height: 1.8; text-align: center; padding: 25px; background-color: #f0f2f6; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. אתחול
if "step" not in st.session_state:
    st.session_state.step = "lang"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. חיבור ל-API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("בעיה ב-API Key")

# שלב 1: שפה
if st.session_state.step == "lang":
    st.markdown("### Choose Your Language / בחרו שפה")
    c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
    with c2:
        if st.button("English 🇺🇸"):
            st.session_state.lang = "en"; st.session_state.step = "intro"; st.rerun()
    with c3:
        if st.button("עברית 🇮🇱"):
            st.session_state.lang = "he"; st.session_state.step = "intro"; st.rerun()

# שלב 2: פתיחה
elif st.session_state.step == "intro":
    text = "ברוכים הבאים למסע לטרנספורמציה שלכם! היום נמצא את מה שהופך אתכם לייחודיים באמת." if st.session_state.lang == "he" else "Welcome! Today we find what makes you truly unique."
    btn = "מתחילים במסע ←" if st.session_state.lang == "he" else "Start Journey ←"
    st.markdown(f'<div class="intro-box">{text}</div>', unsafe_allow_html=True)
    if st.button(btn):
        msg = "נהדר! בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)." if st.session_state.lang == "he" else "Great! Let's begin. What is the one thing you love doing the most?"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.session_state.step = "chat"; st.rerun()

# שלב 3: צ'אט
elif st.session_state.step == "chat":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("כתבו כאן..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)

        try:
            # שימוש בשם המודל הקצר - הכי בטוח נגד 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # שליחת ההודעה האחרונה כטקסט פשוט
            response = model.generate_content(p)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            # אם יש שגיאה, ננסה את המודל השני כגיבוי מיידי
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(p)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except:
                st.error(f"שגיאה טכנית: {str(e)}")

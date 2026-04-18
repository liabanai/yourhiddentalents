import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה ויישור לימין
st.set_page_config(page_title="Genius Zone Coach", layout="centered")

st.markdown("""
    <style>
    .stApp, .stChatMessage, div[data-testid="stChatMessageContent"] {
        direction: rtl !important;
        text-align: right !important;
    }
    div[data-testid="stChatMessageContent"] p {
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        height: 3.5em;
    }
    .intro-box {
        font-size: 1.25rem;
        line-height: 1.8;
        text-align: center;
        padding: 30px;
        background-color: #f8f9fb;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid #e0e4e9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API
if "api_configured" not in st.session_state:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        st.session_state.api_configured = True
    except:
        st.error("שגיאה בחיבור ל-API.")
        st.stop()

# 3. ניהול שלבים
if "step" not in st.session_state:
    st.session_state.step = "language_selection"

# שלב 1: בחירת שפה
if st.session_state.step == "language_selection":
    st.markdown("<h3 style='text-align: center;'>Choose Your Language / בחרו שפה</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English 🇺🇸"):
            st.session_state.language = "English"
            st.session_state.step = "intro_text"
            st.rerun()
    with col2:
        if st.button("עברית 🇮🇱"):
            st.session_state.language = "Hebrew"
            st.session_state.step = "intro_text"
            st.rerun()

# שלב 2: טקסט השראה
elif st.session_state.step == "intro_text":
    if st.session_state.language == "Hebrew":
        st.markdown("""<div class="intro-box"><strong>ברוכים הבאים למסע לטרנספורמציה שלכם!</strong><br><br>אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם.<br><br>רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת.</div>""", unsafe_allow_html=True)
        if st.button("מתחילים במסע ←"):
            st.session_state.messages = [{"role": "assistant", "content": "נהדר! בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."}]
            st.session_state.step = "chat"
            st.rerun()
    else:
        st.markdown("""<div class="intro-box"><strong>Welcome to your Transformation Journey!</strong><br><br>We are embarking on a journey to find your 'Zone of Genius'. This is the intersection of your passion, effortless skill, and unique value.<br><br>Most people live in their 'Zone of Excellence' – doing things they are good at, but which ultimately drain them. Today, we will find what makes you truly unique.</div>""", unsafe_allow_html=True)
        if st.button("Start Journey ←"):
            st.session_state.messages = [{"role": "assistant", "content": "Great! Let's begin. What is the one thing you love doing the most? (Something that gives you energy)."}]
            st.session_state.step = "chat"
            st.rerun()

# שלב 3: הצ'אט
elif st.session_state.step == "chat":
    # הוראות מערכת
    SYSTEM_PROMPT = "You are a professional Zone of Genius coach. Conduct the session step-by-step. Ask 4 questions one-by-one."
    
    # הצגת הודעות
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # קלט משתמש
    if prompt := st.chat_input("השיבו כאן..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # שימוש במודל יציב
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
            history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
            response = model.generate_content(history)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"אירעה שגיאה: {e}")

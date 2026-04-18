import streamlit as st
import google.generativeai as genai

# 1. הגדרות דף ועיצוב CSS
st.set_page_config(page_title="Genius Zone Coach", layout="centered")

st.markdown("""
    <style>
    .stApp, [data-testid="stChatMessageContent"] {
        direction: rtl !important;
        text-align: right !important;
    }
    h1, h3 { text-align: center !important; }
    .stButton button {
        width: 100%;
        border-radius: 25px;
        font-weight: bold;
        height: 3.5em;
    }
    .intro-box {
        font-size: 1.25rem;
        line-height: 1.8;
        text-align: center;
        padding: 30px;
        background-color: #f0f2f6;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid #d1d5db;
    }
    /* מירכוז כפתורי השפה */
    .lang-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. אתחול
if "step" not in st.session_state:
    st.session_state.step = "language_selection"
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("חסר API Key ב-Secrets")
    st.stop()

# --- שלב 1: בחירת שפה ---
if st.session_state.step == "language_selection":
    st.markdown("### Choose Your Language / בחרו שפה")
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        if st.button("English 🇺🇸"):
            st.session_state.language = "English"
            st.session_state.step = "intro_text"
            st.rerun()
    with col3:
        if st.button("עברית 🇮🇱"):
            st.session_state.language = "Hebrew"
            st.session_state.step = "intro_text"
            st.rerun()

# --- שלב 2: טקסט השראה ---
elif st.session_state.step == "intro_text":
    if st.session_state.language == "Hebrew":
        st.markdown('<div class="intro-box"><strong>ברוכים הבאים למסע לטרנספורמציה שלכם!</strong><br><br>אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם.<br><br>רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת.</div>', unsafe_allow_html=True)
        col_empty, col_btn, col_empty2 = st.columns([1, 2, 1])
        with col_btn:
            if st.button("מתחילים במסע ←"):
                st.session_state.messages.append({"role": "assistant", "content": "נהדר! בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."})
                st.session_state.step = "chat"
                st.rerun()
    else:
        st.markdown('<div class="intro-box"><strong>Welcome to your Transformation Journey!</strong><br><br>We are embarking on a journey to find your \'Zone of Genius\'. This is the intersection of your passion, effortless skill, and unique value.<br><br>Most people live in their \'Zone of Excellence\' – doing things they are good at, but which ultimately drain them. Today, we will find what makes you truly unique.</div>', unsafe_allow_html=True)
        col_empty, col_btn, col_empty2 = st.columns([1, 2, 1])
        with col_btn:
            if st.button("Start Journey ←"):
                st.session_state.messages.append({"role": "assistant", "content": "Great! Let's begin. What is the one thing you love doing the most? (Something that gives you energy)."})
                st.session_state.step = "chat"
                st.rerun()

# --- שלב 3: הצ'אט ---
elif st.session_state.step == "chat":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("כתבו כאן..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # תיקון השגיאה: בניית ההיסטוריה בצורה שגוגל אוהב
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=[])
            
            # שליחת כל ההיסטוריה למעט ההודעה האחרונה כהקשר
            sys_prompt = "You are a professional performance coach. Ask 4 questions one by one. Be concise and supportive."
            
            # שליחת ההודעה האחרונה וקבלת תשובה
            response = chat.send_message(f"Context: {sys_prompt}\n\nUser says: {prompt}")
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"שגיאה: {e}")

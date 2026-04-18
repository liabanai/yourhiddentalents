import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp, [data-testid="stChatMessageContent"] { direction: rtl !important; text-align: right !important; }
    h1, h3 { text-align: center !important; }
    .stButton button { width: 100%; border-radius: 25px; font-weight: bold; height: 3.5em; }
    .intro-box { font-size: 1.2rem; line-height: 1.8; text-align: center; padding: 25px; background-color: #f0f2f6; border-radius: 20px; border: 1px solid #d1d5db; }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API
if "api_configured" not in st.session_state:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        st.session_state.api_configured = True
    except:
        st.error("חסר API Key")
        st.stop()

# 3. ניהול שלבים
if "step" not in st.session_state:
    st.session_state.step = "lang"
if "messages" not in st.session_state:
    st.session_state.messages = []

# שלב 1: שפה
if st.session_state.step == "lang":
    st.markdown("### Choose Your Language / בחרו שפה")
    c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
    with c2:
        if st.button("English 🇺🇸"):
            st.session_state.lang = "en"
            st.session_state.step = "intro"
            st.rerun()
    with c3:
        if st.button("עברית 🇮🇱"):
            st.session_state.lang = "he"
            st.session_state.step = "intro"
            st.rerun()

# שלב 2: הודעת פתיחה
elif st.session_state.step == "intro":
    if st.session_state.lang == "he":
        st.markdown('<div class="intro-box"><strong>ברוכים הבאים למסע לטרנספורמציה שלכם!</strong><br><br>אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם.<br><br>רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת.</div>', unsafe_allow_html=True)
        if st.button("מתחילים במסע ←"):
            st.session_state.messages.append({"role": "assistant", "content": "נהדר! בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."})
            st.session_state.step = "chat"
            st.rerun()
    else:
        st.markdown('<div class="intro-box"><strong>Welcome to your Transformation Journey!</strong><br><br>We are embarking on a journey to find your \'Zone of Genius\'. This is the intersection of your passion, effortless skill, and unique value.</div>', unsafe_allow_html=True)
        if st.button("Start Journey ←"):
            st.session_state.messages.append({"role": "assistant", "content": "Great! Let's begin. What is the one thing you love doing the most? (Something that gives you energy)."})
            st.session_state.step = "chat"
            st.rerun()

# שלב 3: צ'אט
elif st.session_state.step == "chat":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("כתבו כאן..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        try:
            # שימוש בשם מודל קצר בלבד! בלי models/
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # בניית היסטוריה פשוטה
            history = []
            for m in st.session_state.messages:
                history.append({"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]})
            
            response = model.generate_content(history)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            # אם גם זה נכשל, ננסה את השם הישן והבטוח
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(history)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except:
                st.error("אירעה שגיאה בחיבור לגוגל. נסו שוב בעוד דקה.")

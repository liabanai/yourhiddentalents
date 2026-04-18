import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה, יישור לימין (RTL) ושיפור קריאות
st.set_page_config(page_title="Genius Zone Coach", layout="centered")

st.markdown("""
    <style>
    .stApp, .stChatMessage, div[data-testid="stChatMessageContent"] {
        direction: rtl !important;
        text-align: right !important;
    }
    div[data-testid="stChatMessageContent"] p, div[data-testid="stChatMessageContent"] li {
        text-align: right !important;
        direction: rtl !important;
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
    div[data-testid="stChatInput"] textarea {
        text-align: right !important;
        direction: rtl !important;
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
        height: 3.5em;
        font-size: 1.1rem;
    }
    h1, h2, h3 { text-align: center !important; }
    .intro-text {
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

# 2. חיבור ל-API וקיבוע מודל (למניעת שגיאת 404)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # קיבוע המודל לגרסה היציבה ביותר
    st.session_state.model_name = 'gemini-1.5-flash'
except:
    st.error("שגיאה בחיבור ל-API. וודאו שהמפתח מוזן ב-Secrets.")
    st.stop()

# 3. הוראות המערכת
SYSTEM_PROMPT = """
You are an elite performance coach specializing in Dr. Gay Hendricks' 'Zone of Genius'. 
- Conduct the session ONLY in the language chosen by the user.
- Ask the 4 questions ONE BY ONE. Wait for a response before proceeding.
- Analysis: After 4 answers, provide: Genius DNA, Excellence Trap, and Genius Statement.
"""

# 4. ניהול שלבי הפתיחה
if "step" not in st.session_state:
    st.session_state.step = "language_selection"

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
    st.stop()

elif st.session_state.step == "intro_text":
    if st.session_state.language == "Hebrew":
        st.markdown("""
        <div class="intro-text">
        <strong>ברוכים הבאים למסע לטרנספורמציה שלכם!</strong><br><br>
        אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם.<br><br>
        רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת.
        </div>
        """, unsafe_allow_html=True)
        if st.button("מתחילים במסע ←"):
            st.session_state.messages = [{"role": "assistant", "content": "נהדר! בואו נתחיל במסע. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."}]
            st.session_state.step = "chat"
            st.rerun()
    else:
        st.markdown("""
        <div class="intro-text">
        <strong>Welcome to your Transformation Journey!</strong><br><br>
        We are embarking on a journey to find your 'Zone of Genius'. This is the intersection of your passion, effortless skill, and unique value.<br><br>
        Most people live in their 'Zone of Excellence' – doing things they are good at, but which ultimately drain them. Today, we will find what makes you truly unique.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Journey ←"):
            st.session_state.messages = [{"role": "assistant", "content": "Great! Let's begin. What is the one thing you love doing the most? (Something that gives you energy)."}]
            st.session_state.step = "chat"
            st.rerun()
    st.stop()

# 5. הצגת הצ'אט

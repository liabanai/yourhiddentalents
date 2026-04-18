import streamlit as st
import google.generativeai as genai

# 1. עיצוב ויישור לימין (RTL)
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp, [data-testid="stChatMessageContent"] { direction: rtl !important; text-align: right !important; }
    h1, h3 { text-align: center !important; }
    .stButton button { width: 100%; border-radius: 25px; font-weight: bold; height: 3.5em; }
    .intro-box { 
        font-size: 1.2rem; 
        line-height: 1.8; 
        text-align: center; 
        padding: 25px; 
        background-color: #f0f2f6; 
        border-radius: 20px; 
        border: 1px solid #d1d5db;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. אתחול משתנים
if "step" not in st.session_state:
    st.session_state.step = "lang"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "he"

# 3. חיבור ל-API
api_configured = False
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    api_configured = True
except KeyError:
    st.error("❌ חסר GOOGLE_API_KEY ב-Streamlit Secrets")
except Exception as e:
    st.error(f"❌ בעיה בחיבור ל-API: {str(e)}")

# פונקציה לקבלת תשובה מ-Gemini עם היסטוריה מלאה
def get_gemini_response(messages: list, lang: str) -> str:
    system_prompt = (
        "אתה מאמן ביצועים מקצועי ואמפתי המתמחה בעזרה לאנשים למצוא את 'אזור הגאונות' שלהם. "
        "נהל את השיחה בעברית. שאל שאלות ממוקדות, קצרות ועמוקות. "
        "הקשב לתשובות, עודד ותן תובנות. אל תרשום רשימות ארוכות – שמור על שיחה זורמת וחמה."
        if lang == "he" else
        "You are a professional and empathetic performance coach specializing in helping people find their 'Zone of Genius'. "
        "Conduct the session in English. Ask focused, short, and deep questions. "
        "Listen to answers, encourage, and give insights. Avoid long lists – keep the conversation flowing and warm."
    )

    # המרת היסטוריה לפורמט של Gemini
    gemini_history = []
    for msg in messages[:-1]:  # כל ההודעות חוץ מהאחרונה
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt
    )

    chat = model.start_chat(history=gemini_history)
    last_user_msg = messages[-1]["content"]
    response = chat.send_message(last_user_msg)
    return response.text


# שלב 1: בחירת שפה
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
        text = """<strong>ברוכים הבאים למסע לטרנספורמציה שלכם!</strong><br><br>
        אנחנו יוצאים למסע למציאת "אזור הגאונות" שלכם. זהו המפגש בין התשוקה שלכם, המיומנות חסרת המאמץ והערך הייחודי שלכם.<br><br>
        רוב האנשים חיים ב"אזור המצוינות" שלהם – עושים דברים שהם טובים בהם, אך בסופו של דבר מרוקנים אותם. היום, נמצא את מה שהופך אתכם לייחודיים באמת."""
        btn = "מתחילים במסע ←"
        first_msg = "נהדר! בואו נתחיל. מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."
    else:
        text = """<strong>Welcome to your Transformation Journey!</strong><br><br>
        We are embarking on a journey to find your 'Zone of Genius'. This is the intersection of your passion, effortless skill, and unique value.<br><br>
        Today, we will find what makes you truly unique."""
        btn = "Start Journey ←"
        first_msg = "Great! Let's begin. What is the one thing you love doing the most? (Something that gives you energy)."

    st.markdown(f'<div class="intro-box">{text}</div>', unsafe_allow_html=True)

    c_empty1, c_btn, c_empty2 = st.columns([1, 2, 1])
    with c_btn:
        if st.button(btn):
            st.session_state.messages.append({"role": "assistant", "content": first_msg})
            st.session_state.step = "chat"
            st.rerun()

# שלב 3: צ'אט
elif st.session_state.step == "chat":
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    placeholder_text = "כתבו כאן..." if st.session_state.lang == "he" else "Type here..."

    if p := st.chat_input(placeholder_text):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)

        if not api_configured:
            st.error("לא ניתן לשלוח הודעה – API לא מוגדר כראוי.")
        else:
            try:
                with st.spinner("..."):
                    reply = get_gemini_response(st.session_state.messages, st.session_state.lang)

                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

            except Exception as e:
                err_str = str(e)
                if "API_KEY" in err_str or "authentication" in err_str.lower():
                    st.error("❌ שגיאת אימות – בדוק שה-API Key תקין.")
                elif "quota" in err_str.lower() or "rate" in err_str.lower():
                    st.error("❌ חרגת ממכסת הבקשות. נסה שוב בעוד מספר שניות.")
                elif "blocked" in err_str.lower() or "safety" in err_str.lower():
                    st.warning("⚠️ התוכן נחסם על ידי מסנני הבטיחות. נסח מחדש את ההודעה.")
                else:
                    st.error(f"❌ שגיאה: {err_str}")

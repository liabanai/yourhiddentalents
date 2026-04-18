import streamlit as st
import google.generativeai as genai

# 1. הגדרות תצוגה וכיווניות (RTL)
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    input, textarea { direction: rtl; text-align: right; }
    div[data-testid="stChatMessageContent"] { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# 2. חיבור ל-API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("שגיאה: לא נמצא API Key ב-Secrets של Streamlit.")
    st.stop()

# 3. הוראות המערכת (הלוגיקה של המאמן)
SYSTEM_PROMPT = """
You are an elite performance coach specializing in Dr. Gay Hendricks' 'Zone of Genius'. 

Step 0: Start by welcoming the user and asking for language preference (Hebrew / English).
If Hebrew is chosen, use these questions:
1. "מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שמעניק לך אנרגיה)."
2. "מהו החלק בעבודה שלך שמניב את היחס הגבוה ביותר של תוצאות לעומת זמן?"
3. "מהי היכולת הייחודית שלך? משהו שמרגיש לך טבעי אבל לאחרים נראה קשה."
4. "מהו הערך הייחודי שאת/ה מביא/ה לעולם כשאת/ה במיטבך?"

Analysis: Identify the Genius DNA vs. Excellence Trap. 
Always ask for user approval before moving to Part B (Career Matches).
"""

# 4. ניהול זיכרון השיחה
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "ברוך הבא למסע לגילוי אזור הגאונות שלך! באיזו שפה תרצה/י שננהל את השיחה? (עברית / English)"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# 5. הצגת הודעות קודמות
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. קלט משתמש ותגובת מודל
if prompt := st.chat_input("הקלד/י כאן..."):
    # הצגת הודעת המשתמש
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # יצירת תשובה מה-AI (כאן הכל חייב להיות עם הזחה פנימה)
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
        
        # בניית היסטוריה לפורמט של גוגל
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
        
        response = model.generate_content(history)
        full_response = response.text
        
        # הצגת תשובת ה-AI
        with st.chat_message("assistant"):
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        st.error(f"אירעה שגיאה בחיבור למודל: {e}")

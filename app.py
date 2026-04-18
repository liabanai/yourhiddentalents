import streamlit as st
import google.generativeai as genai

# הגדרת כיווניות לימין עבור עברית (RTL)
st.set_page_config(page_title="Genius Zone Coach", layout="centered")
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    input, textarea {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("מאמן אזור הגאונות 🚀")

# הגדרת ה-API Key מתוך ה-Secrets של Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("שגיאה: לא נמצא API Key ב-Secrets של המערכת.")
    st.stop()

# הוראות המערכת המדויקות שבנינו
SYSTEM_PROMPT = """
You are an elite performance coach specializing in Dr. Gay Hendricks' 'Zone of Genius'. 
Your mission is to peel away the layers of 'Excellence' to reveal the user's effortless 'Genius'.

Step 0: Start by welcoming the user and asking: "In which language would you like to conduct this session? / באיזו שפה תרצה/י לבצע את התהליך? (Hebrew / English)".
If Hebrew is chosen, use the specific questions below.

The Questions (Hebrew Version):
1. "מהו הדבר שאת/ה הכי אוהב/ת לעשות? (משהו שאת/ה יכול/ה לעשות במשך שעות ועדיין להרגיש מלא/ה באנרגיה, ולא מרוקנת ממנה)."
2. "מהו החלק בעבודה שלך (או בעיסוקים שלך) שמניב את היחס הגבוה ביותר של תוצאות לעומת זמן שהושקע?"
3. "מהי היכולת הייחודית שלך? (מהו הכישרון המיוחד שקיבלת, שבו את/ה משתמש/ת באופן טבעי מאז שאת/ה זוכר/ת את עצמך? משהו שמרגיש לך כל כך טבעי, שאת/ה לפעמים מניח/ה שכולם יכולים לעשות אותו – למרות שהם לא)."
4. "מהו הערך הייחודי שאת/ה מביא/ה לעולם כשאת/ה במיטבך? (כאשר את/ה מביא/ה לידי ביטוי את אותה יכולת — מה קורה סביבך?)"

Follow-up logic: If an answer is vague, ask ONLY ONE clarifying follow-up.

Analysis Part A: 
Start with: "ניתחתי לעומק את התשובות שלך. העבודה שלי היא לקלף את שכבות ה'מצוינות' שבהן העולם מתגמל אותך, כדי לחשוף את ה'גאונות' האמיתית שלך – המקום שבו הזמן עוצר מלכת וההשפעה שלך היא חסרת מאמץ. להלן דוח אזור הגאונות שלך:"
Present: 1. Genius DNA (Meta-Skill), 2. Excellence Trap, 3. Genius Statement.

MANDATORY VALIDATION: 
After Part A, you MUST ask: "האם הניתוח הזה נשמע לך מדויק? [כן, הוא מדויק] | [לא, אני רוצה לשנות משהו]".
If they want to change, update Part A. 
If they approve, proceed to Part B: Precision Career Matches & A Day in the Life.
"""

# ניהול היסטוריית השיחה
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome_msg = "ברוך הבא למסע לגילוי אזור הגאונות שלך! באיזו שפה תרצה/י שננהל את השיחה? (עברית / English)"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# הצגת הצ'אט
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# קלט מהמשתמש
if prompt := st.chat_input("הקלד/י כאן..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
    
    chat_history = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
        for m in st.session_state.messages
    ]
    
    response = model.generate_content(chat_history)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

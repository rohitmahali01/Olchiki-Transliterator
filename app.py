import streamlit as st
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ol Chiki Transliterator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MAPPINGS ---
olchiki_to_latin = {
    'ᱚ': 'o', 'ᱟ': 'ā', 'ᱤ': 'i', 'ᱩ': 'u', 'ᱮ': 'e', 'ᱳ': 'o', 'ᱶ': 'ṅ', 'ᱠ': 'k', 'ᱜ': 'g',
    'ᱝ': 'ṃ', 'ᱪ': 'c', 'ᱡ': 'j', 'ᱧ': 'ñ', 'ᱴ': 'ṭ', 'ᱰ': 'ḍ', 'ᱬ': 'ṇ', 'ᱛ': 't', 'ᱫ': 'd',
    'ᱱ': 'n', 'ᱯ': 'p', 'ᱵ': 'b', 'ᱢ': 'm', 'ᱭ': 'y', 'ᱞ': 'l', 'ᱨ': 'r', 'ᱣ': 'w', 'ᱥ': 's',
    'ᱦ': 'ẖ', 'ᱲ': 'ṛ', 'ᱷ': 'h', '᱐': '0', '᱑': '1', '᱒': '2', '᱓': '3', '᱔': '4', '᱕': '5',
    '᱖': '6', '᱗': '7', '᱘': '8', '᱙': '9',
}
vowels_full = {'ᱚ': 'ओ', 'ᱟ': 'आ', 'ᱤ': 'इ', 'ᱩ': 'उ', 'ᱮ': 'ए', 'ᱳ': 'ओ'}
vowels_matra = {'ᱚ': 'ो', 'ᱟ': 'ा', 'ᱤ': 'ि', 'ᱩ': 'ु', 'ᱮ': 'े', 'ᱳ': 'ो'}
consonants = {
    'ᱶ': 'ङ', 'ᱠ': 'क', 'ᱜ': 'ग', 'ᱝ': 'ं', 'ᱪ': 'च', 'ᱡ': 'ज', 'ᱧ': 'ञ', 'ᱴ': 'ट', 'ᱰ': 'ड',
    'ᱬ': 'ण', 'ᱛ': 'त', 'ᱫ': 'द', 'ᱱ': 'न', 'ᱯ': 'प', 'ᱵ': 'ब', 'ᱢ': 'म', 'ᱭ': 'य', 'ᱞ': 'ल',
    'ᱨ': 'र', 'ᱣ': 'व', 'ᱥ': 'स', 'ᱦ': 'ह', 'ᱲ': 'ड़', 'ᱷ': 'ह',
}
digits = {'᱐': '०', '᱑': '१', '᱒': '२', '᱓': '३', '᱔': '४', '᱕': '५', '᱖': '६', '᱗': '७', '᱘': '८', '᱙': '९'}

# --- TRANSLITERATION LOGIC ---
@st.cache_data
def transliterate_to_latin(text: str) -> list[str]:
    words = text.strip().split()
    return [''.join(olchiki_to_latin.get(c, c) for c in word) for word in words]

@st.cache_data
def transliterate_to_devanagari(text: str) -> list[str]:
    words = text.strip().split()
    result = []
    for word in words:
        if not word:
            continue
        output_chars = []
        last_char_was_consonant = False
        for char in word:
            if char in consonants:
                output_chars.append(consonants[char])
                last_char_was_consonant = True
            elif char in vowels_full:
                if not last_char_was_consonant:
                    output_chars.append(vowels_full[char])
                else:
                    output_chars.append(vowels_matra[char])
                last_char_was_consonant = False
            elif char in digits:
                output_chars.append(digits[char])
                last_char_was_consonant = False
            else:
                output_chars.append(char)
                last_char_was_consonant = False
        result.append("".join(output_chars))
    return result

# --- UI TOOLTIP FUNCTION ---
def create_tooltip_words(words: list[str]) -> str:
    word_spans = (
        f'<span class="tooltip">{word}<span class="tooltiptext">#{i}</span></span>'
        for i, word in enumerate(words, 1)
    )
    return f'<div class="word-container">{" ".join(word_spans)}</div>'

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .word-container { font-size: 1.0em; line-height: 2.0em; text-align: left; word-wrap: break-word; }
    .tooltip {
        position: relative; display: inline-block; cursor: pointer;
        padding: 4px 8px; margin: 2px; border-radius: 7px;
        transition: background-color 0.3s ease;
    }
    .tooltip:hover { background-color: rgba(255, 255, 255, 0.1); }
    .tooltip .tooltiptext {
        visibility: hidden; background-color: #1E90FF; color: #fff;
        text-align: center; padding: 5px 10px; border-radius: 6px;
        position: absolute; z-index: 1; bottom: 130%; left: 50%;
        transform: translateX(-50%); opacity: 0; transition: opacity 0.3s;
        font-size: 0.9em; white-space: nowrap;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
    </style>
""", unsafe_allow_html=True)

# --- PAGE TITLE ---
st.title("Ol Chiki Transliterator")

# --- MAIN FORM ---
with st.form(key="transliteration_form"):
    st.subheader(" Input: Ol Chiki")
    input_text = st.text_area(
        "Type or paste Ol Chiki text here:",
        height=200,
        placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ"
    )
    script_choice = st.radio(
        "Choose Output Script:",
        ["Latin", "Devanagari"],
        horizontal=True,
        key="script_choice"
    )
    submitted = st.form_submit_button("Transliterate")

# --- PROCESSING ---
if submitted and input_text.strip():
    olchiki_words = input_text.strip().split()

    with st.spinner("Transliterating..."):
        start_time = time.time()
        translit_words = (
            transliterate_to_latin(input_text)
            if script_choice == 'Latin'
            else transliterate_to_devanagari(input_text)
        )
        end_time = time.time()

    processing_time = (end_time - start_time) * 1000

    st.markdown("---")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.success(" Transliteration Complete!")
    with col_b:
        st.metric(label="Speed", value=f"{processing_time:.2f} ms")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original (Ol Chiki)")
        st.markdown(create_tooltip_words(olchiki_words), unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <h3 style="margin-bottom: 0;">Output ({script_choice})</h3>
                <button onclick="copyOutput()" style="padding: 6px 12px; font-size: 0.9em;"> Copy</button>
            </div>
            <script>
            function copyOutput() {{
                let text = document.getElementById('output-plain-text').innerText;
                navigator.clipboard.writeText(text).then(() => {{
                    console.log("Copied!");
                }});
            }}
            </script>
        """, unsafe_allow_html=True)

        # Visible Output with Tooltip
        st.markdown(create_tooltip_words(translit_words), unsafe_allow_html=True)

        # Hidden div with plain text (for clipboard copy)
        st.markdown(f"""
            <div id="output-plain-text" style="display: none;">{" ".join(translit_words)}</div>
        """, unsafe_allow_html=True)


elif submitted:
    st.warning(" Please enter some Ol Chiki text to transliterate.")

# --- SECURE EMAIL USING st.secrets ---
EMAIL_SENDER = st.secrets["EMAIL_SENDER"]
EMAIL_RECEIVER = st.secrets["EMAIL_RECEIVER"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

def send_email(name, sender_email, message):
    subject = "Ol Chiki Transliterator Feedback"
    body = f"Name: {name or 'Anonymous'}\nEmail: {sender_email or 'Not provided'}\n\nFeedback:\n{message}"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

# --- FEEDBACK FORM ---
with st.expander(" Send Feedback (Click to Expand)", expanded=False):
    with st.form("feedback_form"):
        st.write("Want to suggest an improvement or feature? Send your feedback.")
        name = st.text_input("Name (optional):")
        user_email = st.text_input("Your Email (optional):")
        feedback = st.text_area("Your Feedback:", height=150)
        send = st.form_submit_button(" Send Feedback")

        if send:
            if feedback.strip():
                success = send_email(name, user_email, feedback)
                if success:
                    st.success(" Feedback sent successfully!")
                else:
                    st.error(" Failed to send feedback. Please try again later.")
            else:
                st.warning(" Feedback field cannot be empty.")

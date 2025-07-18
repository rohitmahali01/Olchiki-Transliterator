import streamlit as st
import time
import html
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Ol Chiki Transliterator", layout="wide", initial_sidebar_state="collapsed")

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

# --- TRANSLITERATION ---
@st.cache_data
def transliterate_to_latin(text: str) -> list[str]:
    words = text.strip().split()
    return [''.join(olchiki_to_latin.get(c, c) for c in word) for word in words]

@st.cache_data
def transliterate_to_devanagari(text: str) -> list[str]:
    words = text.strip().split()
    result = []
    for word in words:
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

# --- TOOLTIP ---
def create_tooltip_words(words: list[str]) -> str:
    word_spans = (
        f'<span class="tooltip">{html.escape(word)}<span class="tooltiptext">#{i}</span></span>'
        for i, word in enumerate(words, 1)
    )
    return f'<div class="word-container">{" ".join(word_spans)}</div>'

# --- CUSTOM CSS ---
st.markdown("""
<style>
.word-container { font-size: 1em; line-height: 2em; word-wrap: break-word; }
.tooltip { position: relative; display: inline-block; cursor: pointer; padding: 4px 8px; margin: 2px; border-radius: 7px; }
.tooltip:hover { background-color: rgba(255,255,255,0.1); }
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

# --- MAIN UI ---
st.title("Ol Chiki Transliterator")

with st.form(key="transliteration_form"):
    st.subheader("Input: Ol Chiki")
    input_text = st.text_area("Type or paste Ol Chiki text here:", height=200, placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ")
    script_choice = st.radio("Choose Output Script:", ["Latin", "Devanagari"], horizontal=True)
    submitted = st.form_submit_button("Transliterate")

if submitted and input_text.strip():
    olchiki_words = input_text.strip().split()
    with st.spinner("Transliterating..."):
        start = time.time()
        translit_words = transliterate_to_latin(input_text) if script_choice == "Latin" else transliterate_to_devanagari(input_text)
        end = time.time()
    st.success("Transliteration Complete!")
    st.metric("Processing Time", f"{(end - start) * 1000:.2f} ms")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original (Ol Chiki)")
        st.markdown(create_tooltip_words(olchiki_words), unsafe_allow_html=True)
    with col2:
        # Two-column layout: title and download button
        col2a, col2b = st.columns([5, 1])

        with col2a:
            st.subheader(f"Output ({script_choice})")

        with col2b:
            st.download_button(
                label=" Download",
                data=" ".join(translit_words),
                file_name="transliteration.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Display transliterated words below
        st.markdown(create_tooltip_words(translit_words), unsafe_allow_html=True)


elif submitted:
    st.warning("Please enter some Ol Chiki text.")

# --- SENDGRID EMAIL FUNCTION ---
def send_email_via_sendgrid(name, sender_email, feedback):
    SENDGRID_API_KEY = st.secrets["SENDGRID_API_KEY"]
    SENDER = st.secrets["EMAIL_SENDER"]
    RECEIVER = st.secrets["EMAIL_RECEIVER"]

    subject = "Ol Chiki Transliterator Feedback"
    content = f"Name: {name or 'Anonymous'}\nEmail: {sender_email or 'Not provided'}\n\nFeedback:\n{feedback}"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "personalizations": [{"to": [{"email": RECEIVER}]}],
        "from": {"email": SENDER},
        "subject": subject,
        "content": [{"type": "text/plain", "value": content}]
    }
    response = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data)
    return response.status_code == 202

# --- FEEDBACK FORM WITH RATE LIMITING ---
st.markdown("###  Feedback")
with st.expander("Send Feedback"):
    if "last_feedback_time" not in st.session_state:
        st.session_state.last_feedback_time = 0

    with st.form("feedback_form"):
        name = st.text_input("Name (optional)")
        user_email = st.text_input("Email (optional)")
        feedback = st.text_area("Your Feedback", height=150)
        submit = st.form_submit_button("Send")

        if submit:
            current_time = time.time()
            if current_time - st.session_state.last_feedback_time < 60:
                st.warning("Please wait a minute before sending feedback again.")
            elif feedback.strip():
                if send_email_via_sendgrid(name, user_email, feedback):
                    st.session_state.last_feedback_time = current_time
                    st.success("Feedback sent successfully.")
                else:
                    st.error("Failed to send feedback. Try again later.")
            else:
                st.warning("Feedback cannot be empty.")

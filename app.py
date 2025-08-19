import streamlit as st
import time
import html
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ol Chiki Transliterator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MAPPINGS (unchanged) ---
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


# --- TRANSLITERATION (unchanged) ---
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

# --- TOOLTIP (unchanged) ---
def create_tooltip_words(words: list[str]) -> str:
    word_spans = (
        f'<span class="tooltip">{html.escape(word)}<span class="tooltiptext">#{i}</span></span>'
        for i, word in enumerate(words, 1)
    )
    return f'<div class="word-container">{" ".join(word_spans)}</div>'

# --- MODERN UI CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    /* --- General Body Styles --- */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #1a1a2e; /* Dark blue-purple background */
    }
    .main {
        background-color: #1a1a2e;
        color: #e0e0e0;
    }

    /* --- Main Container & Header --- */
    .app-container {
        max-width: 1000px;
        margin: auto;
        padding-top: 2rem;
    }
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .app-header h1 {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 1px;
        background: -webkit-linear-gradient(45deg, #a29bfe, #74b9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* --- Card Styles --- */
    .card {
        background-color: #2a2a3e;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid #4a4a5e;
    }

    /* --- Form & Input Styles --- */
    .stTextArea, .stRadio {
        background-color: #1a1a2e;
    }
    .stTextArea textarea {
        background-color: #1a1a2e;
        color: #e0e0e0;
        border-radius: 10px;
        border: 1px solid #4a4a5e;
        font-size: 1.1rem;
    }
    div[data-baseweb="radio"] > label {
        background-color: #2a2a3e !important;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #4a4a5e;
        transition: all 0.3s ease;
    }
    div[data-baseweb="radio"] > label:hover {
        background-color: #3a3a4e !important;
        border-color: #a29bfe;
    }

    /* --- Button Styles --- */
    .stButton > button {
        background: linear-gradient(45deg, #a29bfe, #74b9ff);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(162, 155, 254, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(116, 185, 255, 0.5);
    }
    .stDownloadButton > button {
        background-color: #4a4a5e;
        color: #e0e0e0;
        border: 1px solid #74b9ff;
        border-radius: 8px;
    }
    .stDownloadButton > button:hover {
        background-color: #74b9ff;
        color: #1a1a2e;
    }

    /* --- Output & Tooltip Styles --- */
    .word-container { font-size: 1.2em; line-height: 2.2em; word-wrap: break-word; }
    .tooltip {
        position: relative; display: inline-block; cursor: pointer;
        padding: 5px 10px; margin: 3px; border-radius: 8px;
        background-color: #3a3a4e;
        transition: background-color 0.3s;
    }
    .tooltip:hover { background-color: #4a4a5e; }
    .tooltip .tooltiptext {
        visibility: hidden; background-color: #a29bfe; color: #fff;
        text-align: center; padding: 5px 10px; border-radius: 6px;
        position: absolute; z-index: 1; bottom: 130%; left: 50%;
        transform: translateX(-50%); opacity: 0; transition: opacity 0.3s;
        font-size: 0.9em; white-space: nowrap;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }

    /* --- Section Headers --- */
    h2, h3 {
        color: #ffffff;
        border-bottom: 2px solid #74b9ff;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* --- Expander/Feedback Form --- */
    .stExpander {
        border-color: #4a4a5e;
        border-radius: 10px;
    }
    .stExpander header {
        font-size: 1.2rem;
        font-weight: 500;
        color: #e0e0e0;
    }

</style>
""", unsafe_allow_html=True)

# --- MAIN UI with new structure ---
st.markdown('<div class="app-container">', unsafe_allow_html=True)
st.markdown('<div class="app-header"><h1>Ol Chiki Transliterator</h1></div>', unsafe_allow_html=True)

# --- Input Form Card ---
st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form(key="transliteration_form"):
    st.subheader("✍️ Input: Ol Chiki")
    input_text = st.text_area("Type or paste Ol Chiki text here:", height=200, placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ", label_visibility="collapsed")
    script_choice = st.radio("Choose Output Script:", ["Latin", "Devanagari"], horizontal=True)
    submitted = st.form_submit_button("Transliterate")
st.markdown('</div>', unsafe_allow_html=True)


if submitted and input_text.strip():
    olchiki_words = input_text.strip().split()
    with st.spinner("Transliterating..."):
        start = time.time()
        translit_words = transliterate_to_latin(input_text) if script_choice == "Latin" else transliterate_to_devanagari(input_text)
        end = time.time()

    st.success("Transliteration Complete!")
    st.metric("Processing Time", f"{(end - start) * 1000:.2f} ms")

    # --- Output Card ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📜 Original (Ol Chiki)")
        st.markdown(create_tooltip_words(olchiki_words), unsafe_allow_html=True)
    with col2:
        col2a, col2b = st.columns([4, 1])
        with col2a:
            st.subheader(f"🌐 Output ({script_choice})")
        with col2b:
            st.download_button(
                label="📥",
                data=" ".join(translit_words),
                file_name="transliteration.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download transliterated text"
            )
        st.markdown(create_tooltip_words(translit_words), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif submitted:
    st.warning("Please enter some Ol Chiki text.")

# --- SENDGRID EMAIL FUNCTION (unchanged) ---
def send_email_via_sendgrid(name, sender_email, feedback):
    # This function requires SendGrid credentials in st.secrets
    if "SENDGRID_API_KEY" not in st.secrets:
        st.error("Email sending is not configured.")
        return False

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

# --- FEEDBACK FORM (inside a card for consistency) ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🗣️ Feedback")
with st.expander("Send Feedback or Report an Issue"):
    if "last_feedback_time" not in st.session_state:
        st.session_state.last_feedback_time = 0

    with st.form("feedback_form", clear_on_submit=True):
        name = st.text_input("Name (optional)")
        user_email = st.text_input("Email (optional)")
        feedback = st.text_area("Your Feedback", height=150, placeholder="What did you like? What could be better?")
        submit = st.form_submit_button("Send Feedback")

        if submit:
            current_time = time.time()
            if current_time - st.session_state.last_feedback_time < 60:
                st.warning("Please wait a minute before sending feedback again.")
            elif feedback.strip():
                if send_email_via_sendgrid(name, user_email, feedback):
                    st.session_state.last_feedback_time = current_time
                    st.success("Feedback sent successfully. Thank you!")
                else:
                    st.error("Failed to send feedback. This might be a configuration issue. Please try again later.")
            else:
                st.warning("Feedback cannot be empty.")
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("</div>", unsafe_allow_html=True) # Close app-container
st.markdown("<hr style='border-color: #4a4a5e;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a8a9e;'>Made with Streamlit</p>", unsafe_allow_html=True)

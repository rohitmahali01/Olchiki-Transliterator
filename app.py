import streamlit as st
import time
import html
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ol Chiki Transliterator", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="🔤"
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

# --- TRANSLITERATION FUNCTIONS ---
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

# --- TOOLTIP FUNCTION ---
def create_tooltip_words(words: list[str]) -> str:
    word_spans = (
        f'<span class="tooltip">{html.escape(word)}<span class="tooltiptext">#{i}</span></span>'
        for i, word in enumerate(words, 1)
    )
    return f'<div class="word-container">{" ".join(word_spans)}</div>'

# --- PREMIUM MODERN CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    /* Title Styling */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: white !important;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        letter-spacing: -1px;
    }
    
    h3, .stSubheader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        margin-bottom: 1rem !important;
    }
    
    /* Input Styling */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
        background: linear-gradient(45deg, #FF5252, #26D0CE) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(45deg, #5a67d8, #6b46c1) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    
    .stRadio > div > label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Word Container & Tooltips */
    .word-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        font-size: 1.1em;
        line-height: 2.2em;
        word-wrap: break-word;
        font-family: 'Inter', sans-serif;
        color: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .word-container:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-1px);
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
        padding: 8px 12px;
        margin: 3px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .tooltip:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        text-align: center;
        padding: 8px 12px;
        border-radius: 8px;
        position: absolute;
        z-index: 1000;
        bottom: 130%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: all 0.3s ease;
        font-size: 0.85em;
        white-space: nowrap;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(-5px);
    }
    
    /* Metrics Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    /* Success/Warning Messages */
    .stSuccess {
        background: rgba(72, 187, 120, 0.1) !important;
        border: 1px solid rgba(72, 187, 120, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: rgba(237, 137, 54, 0.1) !important;
        border: 1px solid rgba(237, 137, 54, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: rgba(229, 62, 62, 0.1) !important;
        border: 1px solid rgba(229, 62, 62, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
    }
    
    /* Labels */
    label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.title("🔤 Ol Chiki Transliterator")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
with st.form(key="transliteration_form"):
    st.subheader("✍️ Input: Ol Chiki")
    input_text = st.text_area(
        "Type or paste Ol Chiki text here:", 
        height=200, 
        placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ",
        help="Enter your Ol Chiki text for transliteration"
    )
    
    st.subheader("🎯 Choose Output Script")
    script_choice = st.radio("", ["Latin", "Devanagari"], horizontal=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submitted = st.form_submit_button("🚀 Transliterate", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if submitted and input_text.strip():
    olchiki_words = input_text.strip().split()
    
    with st.spinner("✨ Transliterating your text..."):
        start = time.time()
        translit_words = transliterate_to_latin(input_text) if script_choice == "Latin" else transliterate_to_devanagari(input_text)
        end = time.time()
    
    st.success("🎉 Transliteration Complete!")
    
    # Metrics in a nice card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Processing Time", f"{(end - start) * 1000:.2f} ms")
    with col2:
        st.metric("📝 Words Processed", f"{len(olchiki_words)}")
    with col3:
        st.metric("🔤 Characters", f"{len(input_text)}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📜 Original (Ol Chiki)")
        st.markdown(create_tooltip_words(olchiki_words), unsafe_allow_html=True)
    
    with col2:
        col2a, col2b = st.columns([4, 1])
        with col2a:
            st.subheader(f"✨ Output ({script_choice})")
        with col2b:
            st.download_button(
                label="💾",
                data=" ".join(translit_words),
                file_name=f"transliteration_{script_choice.lower()}.txt",
                mime="text/plain",
                use_container_width=True,
                help=f"Download {script_choice} transliteration"
            )
        st.markdown(create_tooltip_words(translit_words), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif submitted:
    st.warning("⚠️ Please enter some Ol Chiki text to transliterate.")

# --- SENDGRID EMAIL FUNCTION ---
def send_email_via_sendgrid(name, sender_email, feedback):
    try:
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
    except:
        return False

# --- FEEDBACK SECTION ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("💬 We'd Love Your Feedback!")

with st.expander("Send Feedback", expanded=False):
    if "last_feedback_time" not in st.session_state:
        st.session_state.last_feedback_time = 0

    with st.form("feedback_form"):
        name = st.text_input("👤 Name (optional)", placeholder="Your name")
        user_email = st.text_input("📧 Email (optional)", placeholder="your.email@example.com")
        feedback = st.text_area("💭 Your Feedback", height=150, placeholder="Share your thoughts, suggestions, or report issues...")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("📤 Send Feedback", use_container_width=True)

        if submit:
            current_time = time.time()
            if current_time - st.session_state.last_feedback_time < 60:
                st.warning("⏰ Please wait a minute before sending feedback again.")
            elif feedback.strip():
                if send_email_via_sendgrid(name, user_email, feedback):
                    st.session_state.last_feedback_time = current_time
                    st.success("✅ Thank you! Your feedback has been sent successfully.")
                else:
                    st.error("❌ Failed to send feedback. Please try again later.")
            else:
                st.warning("📝 Please write some feedback before sending.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255, 255, 255, 0.6); font-family: 'Inter', sans-serif;">
    <p>Made with ❤️ for preserving Ol Chiki language and culture</p>
</div>
""", unsafe_allow_html=True)

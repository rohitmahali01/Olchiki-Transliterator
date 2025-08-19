import streamlit as st
import time
import html
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Ol Chiki Transliterator",
    page_icon="🔤",
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

# --- CUSTOM CSS (Modernized with better styling, shadows, and transitions) ---
st.markdown("""
<style>
    /* Global Styles */
    body { background-color: #f0f4f8; }
    .stApp { background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); padding: 20px; }
    
    /* Word Container */
    .word-container { 
        font-size: 1.2em; 
        line-height: 2em; 
        word-wrap: break-word; 
        background-color: #f9f9f9; 
        padding: 15px; 
        border-radius: 8px; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
    }
    
    /* Tooltip */
    .tooltip { 
        position: relative; 
        display: inline-block; 
        cursor: pointer; 
        padding: 6px 10px; 
        margin: 4px; 
        border-radius: 8px; 
        transition: background-color 0.3s ease, transform 0.2s ease; 
    }
    .tooltip:hover { 
        background-color: rgba(30, 144, 255, 0.1); 
        transform: translateY(-2px); 
    }
    .tooltip .tooltiptext {
        visibility: hidden; 
        background-color: #1E90FF; 
        color: #fff;
        text-align: center; 
        padding: 6px 12px; 
        border-radius: 6px;
        position: absolute; 
        z-index: 1; 
        bottom: 130%; 
        left: 50%;
        transform: translateX(-50%); 
        opacity: 0; 
        transition: opacity 0.3s ease, bottom 0.3s ease;
        font-size: 0.95em; 
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .tooltip:hover .tooltiptext { 
        visibility: visible; 
        opacity: 1; 
        bottom: 140%; 
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1E90FF;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0d6efd;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #218838;
    }
    
    /* Form and Inputs */
    .stTextArea textarea, .stTextInput input {
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 10px;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #e9ecef;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN UI (Modernized with containers, icons, and better layout) ---
st.title("🔤 Ol Chiki Transliterator")
st.markdown("Transliterate Ol Chiki script to Latin or Devanagari effortlessly.")

# Input Form in a Container
with st.container(border=True):
    st.subheader("📝 Input: Ol Chiki")
    input_text = st.text_area("Type or paste Ol Chiki text here:", height=200, placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ")
    
    script_choice = st.radio("Choose Output Script:", ["Latin", "Devanagari"], horizontal=True)
    
    submitted = st.form(key="transliteration_form", border=False).form_submit_button("Transliterate", type="primary")

if submitted and input_text.strip():
    olchiki_words = input_text.strip().split()
    with st.spinner("Transliterating..."):
        start = time.time()
        translit_words = transliterate_to_latin(input_text) if script_choice == "Latin" else transliterate_to_devanagari(input_text)
        end = time.time()
    
    st.success("Transliteration Complete!")
    st.metric("Processing Time", f"{(end - start) * 1000:.2f} ms")
    
    st.divider()
    
    # Two-Column Layout for Original and Output
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.subheader("📜 Original (Ol Chiki)")
        st.markdown(create_tooltip_words(olchiki_words), unsafe_allow_html=True)
    
    with col2:
        # Header with Title and Download Button
        col2a, col2b = st.columns([4, 2])
        with col2a:
            st.subheader(f"✨ Output ({script_choice})")
        with col2b:
            st.download_button(
                label="📥 Download",
                data=" ".join(translit_words),
                file_name="transliteration.txt",
                mime="text/plain",
                use_container_width=True,
                type="secondary"
            )
        # Display Transliterated Words
        st.markdown(create_tooltip_words(translit_words), unsafe_allow_html=True)

elif submitted:
    st.warning("Please enter some Ol Chiki text.")

# --- ADDITIONAL FEATURES (Filling the rest: Added history, clear button, and about section) ---
# Transliteration History (Using Session State)
if "history" not in st.session_state:
    st.session_state.history = []

if submitted and input_text.strip():
    st.session_state.history.append({
        "input": input_text,
        "output": " ".join(translit_words),
        "script": script_choice
    })
    if len(st.session_state.history) > 5:  # Limit to last 5
        st.session_state.history = st.session_state.history[-5:]

# Display History in Sidebar
with st.sidebar:
    st.title("🕒 Recent Transliterations")
    if st.session_state.history:
        for idx, entry in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"History #{idx}: {entry['script']}"):
                st.text_area("Input", entry["input"], height=100, disabled=True)
                st.text_area("Output", entry["output"], height=100, disabled=True)
    else:
        st.info("No history yet.")
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.markdown("### ℹ️ About")
    st.markdown("This app transliterates Ol Chiki script to Latin or Devanagari. Built with Streamlit.")

# --- SENDGRID EMAIL FUNCTION (Unchanged) ---
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

# --- FEEDBACK FORM (Modernized with icons and better layout) ---
st.divider()
st.subheader("💬 Feedback")
with st.expander("Send Us Your Thoughts"):
    if "last_feedback_time" not in st.session_state:
        st.session_state.last_feedback_time = 0
    
    with st.form("feedback_form"):
        name = st.text_input("Name (optional)", placeholder="Your name")
        user_email = st.text_input("Email (optional)", placeholder="your.email@example.com")
        feedback = st.text_area("Your Feedback", height=150, placeholder="Share your suggestions or issues...")
        submit = st.form_submit_button("📤 Send Feedback", type="primary")
        
        if submit:
            current_time = time.time()
            if current_time - st.session_state.last_feedback_time < 60:
                st.warning("Please wait a minute before sending feedback again.")
            elif feedback.strip():
                if send_email_via_sendgrid(name, user_email, feedback):
                    st.session_state.last_feedback_time = current_time
                    st.success("Feedback sent successfully. Thank you!")
                else:
                    st.error("Failed to send feedback. Please try again later.")
            else:
                st.warning("Feedback cannot be empty.")

# --- FOOTER (Added for modernity) ---
st.markdown("---")
st.caption(f"© {time.strftime('%Y')} Ol Chiki Transliterator | Powered by Streamlit | Last updated: August 19, 2025")

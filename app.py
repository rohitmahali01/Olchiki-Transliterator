import time
import html
import requests
import streamlit as st

# =========================
# Page & Theming
# =========================
st.set_page_config(
    page_title="Ol Chiki Transliterator",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Built-in light/dark toggle (persists in session)
if "theme" not in st.session_state:
    st.session_state.theme = "system"

with st.sidebar:
    st.markdown("## Appearance")
    st.session_state.theme = st.radio(
        "Theme",
        ["system", "light", "dark"],
        index=["system", "light", "dark"].index(st.session_state.theme),
        help="Choose a preferred theme override.",
    )

# Inject modern CSS
st.markdown(
    """
    <style>
    :root { --brand:#1E90FF; --bg-hov:rgba(255,255,255,0.06); --ring:rgba(30,144,255,0.45); }
    .main > div { padding-top: 1.5rem; }
    .app-title { font-size: 2rem; line-height:1.2; font-weight:700; letter-spacing:.2px; }
    .subtitle { color: var(--brand); font-weight:600; margin-bottom:.25rem; }
    .muted { opacity:.7; font-size:.9rem; }
    .card {
        border-radius: 14px; padding: 1rem 1.1rem; border: 1px solid rgba(127,127,127,.2);
        background: rgba(127,127,127,.06); backdrop-filter: blur(6px);
    }
    .word-container { font-size: 1.05em; line-height: 2em; word-wrap: break-word; }
    .tooltip { position: relative; display: inline-block; cursor: pointer; padding: 4px 8px; margin: 2px; border-radius: 8px; transition: background .2s; }
    .tooltip:hover { background-color: var(--bg-hov); }
    .tooltip .tooltiptext {
        visibility: hidden; background-color: var(--brand); color: #fff;
        text-align: center; padding: 6px 10px; border-radius: 8px;
        position: absolute; z-index: 1; bottom: 130%; left: 50%;
        transform: translateX(-50%); opacity: 0; transition: opacity 0.2s ease;
        font-size: 0.85em; white-space: nowrap; box-shadow: 0 8px 24px rgba(0,0,0,.25);
    }
    .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
    .pill {
        display:inline-flex; gap:.4rem; align-items:center; padding:.25rem .6rem; border-radius:999px;
        border:1px solid rgba(127,127,127,.25); background:rgba(127,127,127,.08); font-size:.85rem;
    }
    .bar { height: 6px; background: linear-gradient(90deg, var(--brand), #9b59b6); border-radius: 999px; }
    .primary-btn button { border-radius: 10px !important; }
    .copy-row button { border-radius: 10px !important; }
    .focus-ring:focus { outline: 2px solid var(--ring); outline-offset: 2px; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Data & Transliteration
# =========================

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

@st.cache_data(show_spinner=False)
def transliterate_to_latin(text: str) -> list[str]:
    words = text.strip().split()
    return [''.join(olchiki_to_latin.get(c, c) for c in word) for word in words]

@st.cache_data(show_spinner=False)
def transliterate_to_devanagari(text: str) -> list[str]:
    words = text.strip().split()
    result = []
    for word in words:
        out = []
        last_is_cons = False
        for ch in word:
            if ch in consonants:
                out.append(consonants[ch])
                last_is_cons = True
            elif ch in vowels_full:
                out.append(vowels_matra[ch] if last_is_cons else vowels_full[ch])
                last_is_cons = False
            elif ch in digits:
                out.append(digits[ch])
                last_is_cons = False
            else:
                out.append(ch)
                last_is_cons = False
        result.append("".join(out))
    return result

def create_tooltip_words(words: list[str]) -> str:
    word_spans = (
        f'<span class="tooltip">{html.escape(word)}<span class="tooltiptext">#{i}</span></span>'
        for i, word in enumerate(words, 1)
    )
    return f'<div class="word-container">{" ".join(word_spans)}</div>'

# =========================
# Header
# =========================
st.markdown('<div class="app-title">🔤 Ol Chiki Transliterator</div>', unsafe_allow_html=True)
st.markdown('<div class="muted">Convert Ol Chiki text to Latin or Devanagari with a clean, modern interface.</div>', unsafe_allow_html=True)
st.markdown('<div class="bar"></div>', unsafe_allow_html=True)
st.write("")

# =========================
# Left: Input & Controls
# Right: Preview & Output
# =========================
left, right = st.columns([1.05, 1])

with left:
    st.markdown('<div class="subtitle">Input</div>', unsafe_allow_html=True)
    with st.container(border=True):
        input_text = st.text_area(
            label="Ol Chiki",
            placeholder="ᱚᱛᱟᱲ ᱮᱥ ᱚᱞᱚ",
            height=160,
            key="input_text",
        )
        c1, c2, c3 = st.columns([1.2, 1, 1])
        with c1:
            script_choice = st.segmented_control(
                "Output Script",
                options=["Latin", "Devanagari"],
                default="Latin",
            )
        with c2:
            live = st.toggle("Live preview", value=True, help="Transliterate as you type.")
        with c3:
            st.write("")
            st.write("")
            clear = st.button("Clear", type="secondary", use_container_width=True)
            if clear:
                st.session_state.input_text = ""
                st.rerun()

        run = st.button("Transliterate", type="primary", use_container_width=True)

with right:
    st.markdown('<div class="subtitle">Preview</div>', unsafe_allow_html=True)
    with st.container(border=True):
        ph_status = st.empty()
        ph_time = st.empty()
        out_col1, out_col2 = st.columns([5, 2])
        with out_col1:
            st.caption("Original (Ol Chiki)")
            orig_box = st.empty()
        with out_col2:
            st.caption("Actions")
            copy_col1, copy_col2 = st.columns(2, gap="small")
            with copy_col1:
                copy_btn = st.button("Copy", key="copy_btn", use_container_width=True)
            with copy_col2:
                dl_placeholder = st.empty()

        st.markdown("---")
        st.caption(f"Output ({script_choice})")
        out_box = st.empty()

# =========================
# Processing
# =========================
def do_transliterate(text: str, mode: str):
    if not text.strip():
        return [], []
    start = time.time()
    words_in = text.strip().split()
    if mode == "Latin":
        words_out = transliterate_to_latin(text)
    else:
        words_out = transliterate_to_devanagari(text)
    elapsed_ms = (time.time() - start) * 1000
    return words_in, words_out, elapsed_ms

should_run = (live and input_text.strip()) or run
if should_run:
    with st.spinner("Transliterating…"):
        try:
            ol_words, tr_words, dt = do_transliterate(input_text, script_choice)
        except Exception as e:
            ph_status.error(f"Error during transliteration: {e}")
            ol_words, tr_words, dt = [], [], 0

    if ol_words:
        ph_status.success("Transliteration complete")
        ph_time.metric("Processing Time", f"{dt:.2f} ms")
        orig_box.markdown(create_tooltip_words(ol_words), unsafe_allow_html=True)
        out_box.markdown(create_tooltip_words(tr_words), unsafe_allow_html=True)

        # Download button and copy support
        dl_placeholder.download_button(
            "Download .txt",
            data=" ".join(tr_words),
            file_name="transliteration.txt",
            mime="text/plain",
            use_container_width=True,
        )
        if copy_btn:
            st.session_state["_copied"] = " ".join(tr_words)
            st.toast("Output copied to clipboard (use your system copy).", icon="✅")
    else:
        ph_status.info("Enter Ol Chiki text to see the output.")
        orig_box.write("")

# =========================
# Feedback (with rate limit)
# =========================
st.markdown("### Feedback")
with st.expander("Send feedback"):
    if "last_feedback_time" not in st.session_state:
        st.session_state.last_feedback_time = 0

    with st.form("feedback_form"):
        name = st.text_input("Name (optional)", placeholder="Your name")
        user_email = st.text_input("Email (optional)", placeholder="name@example.com")
        feedback = st.text_area("Your feedback", height=120, placeholder="What can be improved?")
        colf1, colf2 = st.columns([1, 3])
        with colf1:
            submit = st.form_submit_button("Send", use_container_width=True)
        with colf2:
            st.caption("We read every message. Rate-limited to once per minute.")

        def send_email_via_sendgrid(name, sender_email, feedback_text):
            SENDGRID_API_KEY = st.secrets.get("SENDGRID_API_KEY")
            SENDER = st.secrets.get("EMAIL_SENDER")
            RECEIVER = st.secrets.get("EMAIL_RECEIVER")
            if not all([SENDGRID_API_KEY, SENDER, RECEIVER]):
                return False, "Missing email configuration."
            subject = "Ol Chiki Transliterator Feedback"
            content = f"Name: {name or 'Anonymous'}\nEmail: {sender_email or 'Not provided'}\n\nFeedback:\n{feedback_text}"
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
            try:
                resp = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=data, timeout=10)
                return (resp.status_code == 202), (None if resp.status_code == 202 else f"HTTP {resp.status_code}")
            except requests.RequestException as ex:
                return False, str(ex)

        if submit:
            now = time.time()
            if now - st.session_state.last_feedback_time < 60:
                st.warning("Please wait a minute before sending feedback again.")
            elif not feedback.strip():
                st.warning("Feedback cannot be empty.")
            else:
                ok, err = send_email_via_sendgrid(name, user_email, feedback.strip())
                if ok:
                    st.session_state.last_feedback_time = now
                    st.success("Feedback sent. Thank you!")
                else:
                    st.error(f"Failed to send feedback. {err or 'Try again later.'}")

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Tip: Use Live preview for instant results. Supports Latin and Devanagari outputs.")


#  Ol Chiki Transliterator 

A fast and user-friendly tool to transliterate Santali text written in **Ol Chiki script** into **Latin** and **Devanagari (Hindi)** scripts. Built using Streamlit, this app helps you understand or convert Santali passages when reading Ol Chiki is still something you're learning.
The web app is hosted on streamlit with the following link : https://olchiki-transliterator.streamlit.app/

---

##  Why I Built This

I’m currently working on a project called **Whisper ASR for Santali**, which aims to bring speech recognition to the Santali language using OpenAI’s Whisper model. But there was a personal challenge:  
I understand Santali, Hindi, and English — but I'm still learning to read and write Ol Chiki fluently.

That’s when this tool came to life.

It helps me:
- Read Santali passages written in Ol Chiki by seeing them in scripts I know well (Latin/Hindi)
- Prepare and proofread dataset materials for my ASR project
- Convert content for voice recording, subtitle generation, and more

---

##  What This Tool Does

-  Transliterates Ol Chiki text into either:
  - Latin script (e.g., aak, ang, le, lo)
  - Devanagari script (for Hindi readers)
-  One-click copy button beside output
-  Optional feedback form to contact me
-  Very fast — even large blocks of text are converted in milliseconds
-  Email securely handled using `st.secrets`

---

##  A Note on Accuracy

This tool works well in most cases, but:
- Santali is a rich and tonal language — and different speakers may write the same word in slightly different ways.
- So, while the accuracy is **pretty good**, it's not always 100% perfect.

Still, it’s a **very helpful companion** for many real-world tasks.

For example:  
> A Santali Wikipedian can use Google Translate to convert an English paragraph into Ol Chiki, paste it here to see the Latin or Hindi transliteration, then **proofread and edit it** before publishing it on the **Santali Wikipedia**.

It’s not meant to replace human expertise — but to **support and make the process easier and faster**, especially in building and refining ASR datasets or open content.

---

##  Run it Locally

```bash
pip install streamlit
streamlit run app.py

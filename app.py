import html
import streamlit as st
st.set_page_config(page_title="College Document Q&A", page_icon=":material/school:", layout="centered")
from rag import ask, docs, topics
from ingest import index

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
:root{--bg:#fff;--surface:#F8F9FA;--text:#202124;--muted:#5F6368;--line:#DADCE0;--blue:#1A73E8;--blue-bg:#E8F0FE;--blue-ink:#174EA6}
html, body, .stApp, p, li, label, input, textarea, button, h1, h2, h3, h4, .stMarkdown, [data-testid="stCaptionContainer"]
 {font-family:'Poppins',system-ui,sans-serif !important; color:var(--text)}
#MainMenu, footer, header [data-testid="stToolbar"] {visibility:hidden}
.stApp{background:var(--bg)}
.block-container{max-width:780px; padding-top:2.2rem; padding-bottom:7rem}

/* header */
.brand{display:flex; align-items:center; gap:.65rem; margin-bottom:.2rem}
.logo{width:34px;height:34px;border-radius:10px;background:var(--blue);display:flex;align-items:center;justify-content:center;
      color:#fff;font-weight:600;font-size:.95rem}
.brand h1{font-size:1.35rem;font-weight:500;margin:0;padding:0;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:.9rem;font-weight:300;margin:.1rem 0 1.4rem}
hr.thin{border:none;border-top:1px solid var(--line);margin:0 0 1.2rem}

/* empty state */
.hero{text-align:center;margin:3.2rem 0 1.6rem}
.hero h2{font-size:2rem;font-weight:500;letter-spacing:-.02em;margin:0 0 .4rem}
.hero p{color:var(--muted);font-weight:300;margin:0}

/* buttons: outlined google style */
.stButton>button{border:1px solid var(--line);border-radius:20px;background:#fff;color:var(--blue);font-weight:500;
  font-size:.85rem;padding:.35rem 1rem;transition:all .15s ease;box-shadow:none}
.stButton>button:hover{background:var(--blue-bg);border-color:var(--blue-bg);color:var(--blue-ink)}
.stButton>button:focus{box-shadow:0 0 0 3px rgba(26,115,232,.2);border-color:var(--blue)}

/* sidebar */
[data-testid=stSidebar]{background:var(--surface);border-right:1px solid var(--line)}
[data-testid=stSidebar] h3{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
[data-testid=stFileUploaderDropzone]{background:#fff;border:1px dashed var(--line);border-radius:12px}
[data-testid=stFileUploaderDropzone]:hover{border-color:var(--blue);background:var(--blue-bg)}
.doc{padding:.6rem .8rem;margin:.4rem 0;border:1px solid var(--line);border-radius:12px;background:#fff}
.doc b{display:block;font-weight:500;font-size:.82rem;word-break:break-word}
.doc span{color:var(--muted);font-size:.74rem;font-weight:300}
.empty{color:var(--muted);font-size:.82rem;font-weight:300;padding:.3rem 0}

/* chat */
[data-testid=stChatMessageAvatarUser],[data-testid=stChatMessageAvatarAssistant]{display:none}
[data-testid=stChatMessage]{background:transparent;padding:.4rem 0}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]){flex-direction:row-reverse}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]) [data-testid=stChatMessageContent]{
  background:var(--blue-bg);color:var(--blue-ink);border-radius:20px 20px 4px 20px;padding:.7rem 1.1rem;max-width:80%;margin-left:auto}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant]) [data-testid=stChatMessageContent]{
  border-left:3px solid var(--blue);padding:.15rem 0 .15rem 1rem;line-height:1.7}
.chips{margin:.5rem 0 .2rem}
.chip{display:inline-block;padding:.22rem .75rem;margin:.15rem .3rem .15rem 0;border:1px solid var(--line);border-radius:999px;
      background:#fff;color:var(--muted);font-size:.76rem}
.tchip{display:inline-block;padding:.3rem .85rem;margin:.2rem .35rem .2rem 0;border-radius:999px;background:var(--blue-bg);
       color:var(--blue-ink);font-size:.82rem;font-weight:500}
[data-testid=stExpander]{border:1px solid var(--line);border-radius:12px;background:#fff}
[data-testid=stExpander] summary{font-size:.85rem;font-weight:500}
.pass{border-left:2px solid var(--line);padding:.1rem 0 .1rem .8rem;margin:.55rem 0;font-size:.82rem;color:var(--muted);font-weight:300}
.pass b{color:var(--text);font-weight:500}

/* input: pill */
[data-testid=stBottom]>div{background:linear-gradient(transparent,#fff 35%)}
[data-testid=stChatInput]{border:1px solid var(--line);border-radius:28px;background:#fff;box-shadow:0 1px 3px rgba(60,64,67,.12);transition:box-shadow .15s}
[data-testid=stChatInput]:focus-within{box-shadow:0 2px 10px rgba(60,64,67,.25);border-color:transparent}
[data-testid=stChatInput] textarea{font-family:'Poppins',sans-serif !important;font-size:.95rem}
</style>""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("msgs", []); ss.setdefault("done", set()); ss.setdefault("pending", None)

with st.sidebar:
    st.markdown("### Documents")
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    new = [f for f in up or [] if (f.name, f.size) not in ss.done]
    if new:
        with st.spinner(f"Indexing {len(new)} file(s)"):
            n = index([(f.name, f) for f in new])
        ss.done |= {(f.name, f.size) for f in new}
        st.success(f"Added {n} passages")
    try: kb = docs()
    except Exception: kb = []
    if kb:
        for name, n in kb:
            st.markdown(f'<div class="doc"><b>{html.escape(name)}</b><span>{n} passages indexed</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">No documents yet. Upload PDFs above; they are indexed automatically.</div>', unsafe_allow_html=True)
    if ss.msgs and st.button("New conversation", use_container_width=True):
        ss.msgs = []; st.rerun()

st.markdown('<div class="brand"><div class="logo">Q</div><h1>College Document Q&amp;A</h1></div>'
            '<p class="sub">Answers grounded strictly in your documents, with sources.</p><hr class="thin">', unsafe_allow_html=True)

if kb and not ss.msgs:
    st.markdown('<div class="hero"><h2>How can I help?</h2><p>Ask anything about your uploaded documents.</p></div>', unsafe_allow_html=True)
    ex = ["What is the minimum attendance required?", "Summarise the key rules", "What documents are required for registration?"]
    cols = st.columns(len(ex))
    for col, e in zip(cols, ex):
        if col.button(e, use_container_width=True): ss.pending = e; st.rerun()
    with st.expander("Explore topics in a document"):
        pick = st.selectbox("Document", [k for k, _ in kb], label_visibility="collapsed")
        if st.button("Show topics"):
            with st.spinner("Reading document"):
                try: st.markdown("".join(f'<span class="tchip">{html.escape(t)}</span>' for t in topics(pick)), unsafe_allow_html=True)
                except Exception: st.warning("Could not load topics. Please try again.")

for m in ss.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["text"])
        if m.get("srcs"):
            seen = sorted({(s, p) for s, p, _ in m["srcs"]})
            st.markdown('<div class="chips">' + "".join(f'<span class="chip">{html.escape(s)} · p.{p}</span>' for s, p in seen) + '</div>', unsafe_allow_html=True)
            with st.expander("View source passages"):
                for s, p, t in m["srcs"]:
                    st.markdown(f'<div class="pass"><b>{html.escape(s)}</b> · page {p}<br>{html.escape(t[:380])}</div>', unsafe_allow_html=True)

q = ss.pending or st.chat_input("Ask about your documents" if kb else "Upload a PDF to begin", disabled=not kb)
ss.pending = None
if q:
    ss.msgs.append({"role": "user", "text": q})
    with st.spinner("Searching your documents"):
        try: a, s = ask(q.strip())
        except Exception: a, s = "Something went wrong while searching. Please try again.", []
    ss.msgs.append({"role": "assistant", "text": a, "srcs": s}); st.rerun()

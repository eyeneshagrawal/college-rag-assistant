import html, uuid, time
import streamlit as st
st.set_page_config(page_title="College Assistant", page_icon=":material/school:", layout="wide", initial_sidebar_state="expanded")
from rag import ask, docs, topics
from ingest import index

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
:root{--blue:#4D6BFE;--blue-bg:#EAF0FF;--text:#1F2329;--muted:#6B7280;--line:#E5E7EB;--side:#F7F8FA;--bubble:#F1F3F6}
html,body,.stApp,p,li,label,input,textarea,button,h1,h2,h3,h4,.stMarkdown,[data-testid="stCaptionContainer"]{font-family:'Poppins',system-ui,sans-serif !important;color:var(--text)}
#MainMenu,footer,header [data-testid="stToolbar"]{visibility:hidden}
.stApp{background:#fff}
.block-container{max-width:800px;padding-top:2rem;padding-bottom:8rem}

/* ---------- sidebar ---------- */
[data-testid=stSidebar]{background:var(--side);border-right:1px solid var(--line)}
[data-testid=stSidebar] .block-container{padding-top:1.2rem}
.side-brand{display:flex;align-items:center;gap:.6rem;font-weight:600;font-size:1.02rem;margin:.1rem 0 1rem}
.side-logo{width:28px;height:28px;border-radius:8px;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:600}
.side-h{font-size:.72rem;font-weight:500;color:var(--muted);margin:1.1rem 0 .3rem .2rem}
.st-key-newchat button{background:var(--blue-bg);color:var(--blue);border:none;border-radius:12px;font-weight:500;width:100%;justify-content:flex-start;padding:.55rem .9rem}
.st-key-newchat button:hover{background:#DCE6FF;color:var(--blue)}
[class*="st-key-chat_"] button{background:transparent;border:none;border-radius:10px;width:100%;justify-content:flex-start;text-align:left;
   font-weight:400;font-size:.86rem;padding:.45rem .7rem;color:var(--text);box-shadow:none}
[class*="st-key-chat_"] button p{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
[class*="st-key-chat_"] button:hover{background:#ECEEF2}
[class*="st-key-act_"] button{background:var(--blue-bg) !important;color:var(--blue) !important;font-weight:500}
[class*="st-key-del_"] button{background:transparent;border:none;color:var(--muted);padding:.3rem;box-shadow:none;min-height:0}
[class*="st-key-del_"] button:hover{background:#FDE8E8;color:#D92D20}
[data-testid=stFileUploaderDropzone]{background:#fff;border:1px dashed #CBD2DC;border-radius:12px}
[data-testid=stFileUploaderDropzone]:hover{border-color:var(--blue);background:var(--blue-bg)}
.doc{padding:.55rem .75rem;margin:.35rem 0;border:1px solid var(--line);border-radius:10px;background:#fff}
.doc b{display:block;font-weight:500;font-size:.8rem;word-break:break-word}
.doc span{color:var(--muted);font-size:.72rem}
.empty{color:var(--muted);font-size:.8rem;padding:.2rem .2rem}

/* ---------- main ---------- */
.hero{text-align:center;margin:4.5vh 0 1.8rem}
.hero .logo{width:52px;height:52px;border-radius:16px;background:var(--blue);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:600;font-size:1.3rem;margin-bottom:1rem}
.hero .t{font-size:1.7rem;font-weight:600;letter-spacing:-.01em}
.hero .s{color:var(--muted);font-weight:300;margin-top:.35rem}
.stButton>button{border:1px solid var(--line);border-radius:14px;background:#fff;font-weight:400;font-size:.84rem;padding:.55rem .9rem;transition:all .15s;box-shadow:none;height:auto}
.stButton>button p{white-space:normal;text-align:left}
.stButton>button:hover{border-color:var(--blue);color:var(--blue);background:#FAFBFF}
.tchip{display:inline-block;padding:.3rem .85rem;margin:.2rem .35rem .2rem 0;border-radius:999px;background:var(--blue-bg);color:var(--blue);font-size:.82rem;font-weight:500}
[data-testid=stExpander]{border:1px solid var(--line);border-radius:14px;background:#fff}
[data-testid=stExpander] summary{font-size:.86rem;font-weight:500}

[data-testid=stChatMessageAvatarUser],[data-testid=stChatMessageAvatarAssistant]{display:none}
[data-testid=stChatMessage]{background:transparent;padding:.5rem 0}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]){flex-direction:row-reverse}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]) [data-testid=stChatMessageContent]{background:var(--bubble);border-radius:18px;padding:.7rem 1.1rem;max-width:80%;margin-left:auto}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant]) [data-testid=stChatMessageContent]{line-height:1.75}
.chip{display:inline-block;padding:.2rem .7rem;margin:.15rem .3rem .15rem 0;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--muted);font-size:.75rem}
.pass{border-left:2px solid var(--line);padding:.1rem 0 .1rem .8rem;margin:.55rem 0;font-size:.82rem;color:var(--muted);font-weight:300}
.pass b{color:var(--text);font-weight:500}

[data-testid=stBottom]>div{background:linear-gradient(transparent,#fff 30%)}
[data-testid=stChatInput]{border:1px solid var(--line);border-radius:24px;background:var(--side);box-shadow:none;transition:all .15s}
[data-testid=stChatInput]:focus-within{border-color:var(--blue);background:#fff;box-shadow:0 0 0 3px rgba(77,107,254,.12)}
[data-testid=stChatInput] textarea{font-size:.95rem;min-height:44px}
[data-testid=stChatInputSubmitButton]{background:var(--blue) !important;color:#fff !important;border-radius:50%}
</style>""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("chats", {}); ss.setdefault("order", []); ss.setdefault("cur", None)
ss.setdefault("done", set()); ss.setdefault("pending", None)

def new_chat():
    ss.cur = None
def get_chat():
    if ss.cur is None or ss.cur not in ss.chats:
        cid = uuid.uuid4().hex[:8]; ss.chats[cid] = {"title": "New chat", "msgs": []}; ss.order.insert(0, cid); ss.cur = cid
    return ss.chats[ss.cur]

try: kb = docs()
except Exception: kb = []

# ---------- take input first so the sidebar title updates immediately ----------
q = ss.pending or st.chat_input("Message College Assistant" if kb else "Upload a PDF in the sidebar to begin", disabled=not kb)
ss.pending = None
if q:
    chat = get_chat()
    if not chat["msgs"]: chat["title"] = q.strip()[:40]
    chat["msgs"].append({"role": "user", "text": q.strip()})

# ---------- sidebar ----------
with st.sidebar:
    st.markdown('<div class="side-brand"><div class="side-logo">C</div>College Assistant</div>', unsafe_allow_html=True)
    if st.button("New chat", icon=":material/add:", key="newchat", use_container_width=True):
        new_chat(); st.rerun()
    st.markdown('<div class="side-h">Recent chats</div>', unsafe_allow_html=True)
    if not ss.order: st.markdown('<div class="empty">No conversations yet.</div>', unsafe_allow_html=True)
    for cid in list(ss.order):
        a, b = st.columns([6, 1], vertical_alignment="center")
        with a:
            with st.container(key=f"{'act' if cid == ss.cur else 'chat'}_{cid}"):
                if st.button(ss.chats[cid]["title"], key=f"open_{cid}", use_container_width=True): ss.cur = cid; st.rerun()
        with b:
            with st.container(key=f"del_{cid}"):
                if st.button("", icon=":material/close:", key=f"x_{cid}", help="Delete chat"):
                    ss.order.remove(cid); ss.chats.pop(cid, None)
                    if ss.cur == cid: ss.cur = None
                    st.rerun()
    st.markdown('<div class="side-h">Knowledge base</div>', unsafe_allow_html=True)
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    new = [f for f in up or [] if (f.name, f.size) not in ss.done]
    if new:
        with st.spinner(f"Indexing {len(new)} file(s)"):
            n = index([(f.name, f) for f in new])
        ss.done |= {(f.name, f.size) for f in new}
        st.success(f"Indexed {n} passages"); st.rerun()
    if kb:
        for name, n in kb:
            st.markdown(f'<div class="doc"><b>{html.escape(name)}</b><span>{n} passages indexed</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">No documents yet. PDFs are indexed automatically on upload.</div>', unsafe_allow_html=True)

# ---------- main ----------
chat = ss.chats.get(ss.cur)
msgs = chat["msgs"] if chat else []

def show_sources(srcs):
    if not srcs: return
    seen = sorted({(s, p) for s, p, _ in srcs})
    st.markdown("".join(f'<span class="chip">{html.escape(s)} · p.{p}</span>' for s, p in seen), unsafe_allow_html=True)
    with st.expander("View source passages"):
        for s, p, t in srcs:
            st.markdown(f'<div class="pass"><b>{html.escape(s)}</b> · page {p}<br>{html.escape(t[:380])}</div>', unsafe_allow_html=True)

if not msgs:
    st.markdown('<div class="hero"><div class="logo">C</div><div class="t">Hi, how can I help you today?</div>'
                '<div class="s">Ask anything about your college documents. Every answer cites its source.</div></div>', unsafe_allow_html=True)
    if kb:
        ex = ["What is the minimum attendance required?", "Summarise the key rules", "What documents are required for registration?", "What is the exam revaluation procedure?"]
        c1, c2 = st.columns(2)
        for i, e in enumerate(ex):
            if (c1 if i % 2 == 0 else c2).button(e, key=f"ex{i}", use_container_width=True): ss.pending = e; st.rerun()
        with st.expander("Explore topics in a document"):
            pick = st.selectbox("Document", [k for k, _ in kb], label_visibility="collapsed")
            if st.button("Show topics", key="topics"):
                with st.spinner("Reading document"):
                    try: st.markdown("".join(f'<span class="tchip">{html.escape(t)}</span>' for t in topics(pick)), unsafe_allow_html=True)
                    except Exception: st.warning("Could not load topics. Please try again.")
    else:
        st.info("Upload one or more PDFs in the sidebar to get started.")

history = msgs[:-1] if (q and msgs) else msgs
for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["text"]); show_sources(m.get("srcs"))

if q:
    with st.chat_message("user"): st.markdown(q.strip())
    with st.chat_message("assistant"):
        with st.spinner("Searching your documents"):
            try: a, s = ask(q.strip())
            except Exception: a, s = "Something went wrong while searching. Please try again.", []
        def gen():
            for w in a.split(" "): yield w + " "; time.sleep(0.012)
        st.write_stream(gen()); show_sources(s)
    chat["msgs"].append({"role": "assistant", "text": a, "srcs": s})

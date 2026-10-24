import html, uuid, time, urllib.parse
import streamlit as st
st.set_page_config(page_title="TRAG AI", page_icon=":material/school:", layout="wide", initial_sidebar_state="expanded")
from rag import ask, docs, topics
from ingest import index as index_files

FOX = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
       '<defs><linearGradient id="tg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6C86FF"/><stop offset="1" stop-color="#3550E8"/></linearGradient></defs>'
       '<rect width="32" height="32" rx="9" fill="url(#tg)"/>'
       '<path fill="#fff" d="M8.6 8.4l3.6 2.5c2.5-1.1 5.1-1.1 7.6 0l3.6-2.5v9.1c0 4.7-3 7.6-7.4 8.1-4.4-.5-7.4-3.4-7.4-8.1z"/>'
       '<circle cx="12.7" cy="15.4" r="3" fill="#3550E8"/><circle cx="19.3" cy="15.4" r="3" fill="#3550E8"/>'
       '<circle cx="12.7" cy="15.4" r="1.15" fill="#fff"/><circle cx="19.3" cy="15.4" r="1.15" fill="#fff"/>'
       '<path fill="#F5A524" d="M14.7 19.2h2.6L16 21.6z"/></svg>')
FOX_URI = "data:image/svg+xml;utf8," + urllib.parse.quote(FOX)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Rock+Salt&display=swap');
:root{{--bg:#17171A;--side:#1D1E21;--line:#2B2C30;--hover:#27282C;--active:#2F3035;--box:#2A2B2F;--text:#E8E9EC;--muted:#8D9098;--blue:#4D6BFE}}
html,body,.stApp,p,li,label,input,textarea,button,h1,h2,h3,h4,.stMarkdown,[data-testid="stCaptionContainer"]{{font-family:'Poppins',system-ui,sans-serif !important}}
footer,#MainMenu,[data-testid=stMainMenu],[data-testid=stAppDeployButton],[data-testid=stToolbarActions],[data-testid=stDecoration]{{display:none !important}}
header[data-testid=stHeader]{{background:transparent}}
[data-testid=stExpandSidebarButton],[data-testid=stSidebarCollapsedControl],[data-testid=stSidebarCollapseButton],[data-testid=collapsedControl]{{visibility:visible !important;display:flex !important;color:var(--muted)}}
.stApp{{background:var(--bg)}}
.block-container{{max-width:800px;padding-top:2rem;padding-bottom:11rem}}

/* ===== sidebar ===== */
[data-testid=stSidebar]{{background:var(--side);border-right:1px solid var(--line)}}
[data-testid=stSidebar][aria-expanded=true]{{min-width:300px;width:300px}}
[data-testid=stSidebar] .block-container{{padding-top:1rem}}
.brand{{display:flex;align-items:center;gap:.7rem;margin:.1rem 0 1.2rem}}
.brand span,.hello .bn{{font-family:'Rock Salt',cursive !important;font-weight:400;letter-spacing:.02em;color:#8EA2FF}}
.brand span{{font-size:1.15rem}}
.brand svg{{width:36px;height:36px;flex:0 0 36px}}
.st-key-newchat button{{background:#37383D;color:#fff;border:none;border-radius:999px;height:46px;font-weight:500;width:100%}}
.st-key-newchat button:hover{{background:#424348;color:#fff}}
.side-h{{font-size:.75rem;font-weight:500;color:var(--muted);margin:1.3rem 0 .35rem .35rem}}
[class*="st-key-chat_"] button,[class*="st-key-act_"] button{{background:transparent;border:none;border-radius:10px;width:100%;justify-content:flex-start;
   text-align:left;font-weight:400;font-size:.88rem;padding:.5rem .75rem;color:var(--text);box-shadow:none}}
[class*="st-key-chat_"] button p,[class*="st-key-act_"] button p{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
[class*="st-key-chat_"] button:hover{{background:var(--hover)}}
[class*="st-key-act_"] button{{background:var(--active) !important}}
[class*="st-key-del_"] button{{background:transparent;border:none;color:var(--muted);padding:.2rem;min-height:0;box-shadow:none}}
[class*="st-key-del_"] button:hover{{background:#3A2226;color:#FF6B6B}}
.empty{{color:var(--muted);font-size:.82rem;padding:.2rem .35rem}}
[data-testid=stFileUploaderDropzone]{{background:var(--box);border:1px dashed #44464C;border-radius:12px}}
[data-testid=stFileUploaderDropzone]:hover{{border-color:var(--blue)}}
.doc{{padding:.5rem .75rem;margin:.35rem 0;border:1px solid var(--line);border-radius:10px;background:var(--box)}}
.doc b{{display:block;font-weight:500;font-size:.8rem;word-break:break-word;color:var(--text)}}
.doc span{{color:var(--muted);font-size:.72rem}}
.who{{display:flex;align-items:center;gap:.7rem;font-size:.9rem;font-weight:500;margin-top:1.2rem;padding-top:1rem;border-top:1px solid var(--line)}}
.who i{{width:34px;height:34px;border-radius:50%;background:#D0451B;color:#fff;font-style:normal;display:flex;align-items:center;justify-content:center;font-weight:600}}
[data-testid=stExpander]{{border:1px solid var(--line);border-radius:12px;background:transparent}}
[data-testid=stExpander] summary{{font-size:.86rem;font-weight:500}}

/* ===== greeting ===== */
.hello{{display:flex;align-items:center;justify-content:center;gap:.7rem;margin-top:21vh;margin-bottom:1.6rem;font-size:1.65rem;font-weight:600;color:var(--text)}}
.hello svg{{width:40px;height:40px}}

/* ===== composer ===== */
[class*="st-key-cmp_"] [data-testid=stForm]{{background:var(--box);border:1px solid #36373C;border-radius:22px;padding:.9rem 1.1rem .8rem}}
[class*="st-key-cmp_"] [data-testid=stForm]:focus-within{{border-color:#4A5CC6}}
[class*="st-key-cmp_"] input{{background:transparent !important;border:none !important;box-shadow:none !important;font-size:1rem;color:var(--text);padding:.4rem 0 .9rem}}
[class*="st-key-cmp_"] [data-testid=stTextInput]>div,[class*="st-key-cmp_"] [data-testid=stTextInputRootElement]{{border:none !important;background:transparent !important;box-shadow:none !important}}
[data-testid=InputInstructions]{{display:none}}
[class*="st-key-cmp_"] button[kind=secondaryFormSubmit],[class*="st-key-cmp_"] [data-testid=stFormSubmitButton] button{{background:var(--blue);border:none;border-radius:50%;width:38px;height:38px;min-height:0;padding:0;color:#fff;float:right}}
[class*="st-key-cmp_"] [data-testid=stFormSubmitButton] button:hover{{background:#6F87FF;color:#fff}}
[class*="st-key-cmp_"] [data-testid=stPills] button{{border-radius:999px;font-size:.82rem;font-weight:500;padding:.3rem .85rem;border:1px solid #484A51;background:transparent;color:var(--text)}}
[class*="st-key-cmp_"] [data-testid=stPills] button[aria-checked=true],[class*="st-key-cmp_"] [data-testid=stPills] button[kind=pillsActive]{{background:#25306B;border-color:var(--blue);color:#9FB1FF}}
.st-key-cmp_fixed{{position:fixed;bottom:1.4rem;left:calc((100vw + 300px)/2);transform:translateX(-50%);width:min(780px,calc(100vw - 300px - 3rem));z-index:99}}
.stApp:has([data-testid=stSidebar][aria-expanded=false]) .st-key-cmp_fixed{{left:50%;width:min(780px,calc(100vw - 3rem))}}
.note{{text-align:center;color:var(--muted);font-size:.72rem;margin-top:.5rem}}

/* ===== messages ===== */
[data-testid=stChatMessageAvatarUser],[data-testid=stChatMessageAvatarAssistant]{{display:none}}
[data-testid=stChatMessage]{{background:transparent;padding:.55rem 0}}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]){{flex-direction:row-reverse}}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarUser]) [data-testid=stChatMessageContent]{{background:var(--box);border-radius:18px;padding:.7rem 1.1rem;max-width:80%;margin-left:auto}}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant])::before{{content:"";flex:0 0 30px;height:30px;margin-right:.8rem;margin-top:.15rem;
   background:url("{FOX_URI}") no-repeat center/contain}}
[data-testid=stChatMessage]:has([data-testid=stChatMessageAvatarAssistant]) [data-testid=stChatMessageContent]{{line-height:1.75}}
.chip{{display:inline-block;padding:.2rem .7rem;margin:.15rem .3rem .15rem 0;border:1px solid #3A3C42;border-radius:999px;color:var(--muted);font-size:.75rem}}
.tchip{{display:inline-block;padding:.3rem .85rem;margin:.2rem .35rem .2rem 0;border-radius:999px;background:#25306B;color:#9FB1FF;font-size:.82rem;font-weight:500}}
.pass{{border-left:2px solid #3A3C42;padding:.1rem 0 .1rem .8rem;margin:.55rem 0;font-size:.82rem;color:var(--muted);font-weight:300}}
.pass b{{color:var(--text);font-weight:500}}
.stButton>button{{border:1px solid #3A3C42;border-radius:14px;background:transparent;color:var(--text);font-weight:400;font-size:.84rem;padding:.55rem .9rem;height:auto;box-shadow:none}}
.stButton>button p{{white-space:normal;text-align:left}}
.stButton>button:hover{{border-color:var(--blue);color:#9FB1FF;background:#1F2133}}
</style>""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("chats", {}); ss.setdefault("order", []); ss.setdefault("cur", None)
ss.setdefault("done", set()); ss.setdefault("pending", None)

try: kb = docs()
except Exception: kb = []

# ---- read submitted input BEFORE layout (widget state is available at run start) ----
q = ss.pending
if not q and (ss.get("send") or "send" not in ss): q = (ss.get("txt") or "").strip()
ss.pending = None
chat = ss.chats.get(ss.cur)
empty = not (chat and chat["msgs"]) and not q
modes = ss.get("modes") or []
deep, wide = "Deep Think" in modes, "Wide Search" in modes

def composer(key):
    with st.container(key=key):
        with st.form(key + "_f", clear_on_submit=True, border=False):
            st.text_input("msg", key="txt", placeholder="Message TRAG AI" if kb else "Upload a PDF in the sidebar to begin",
                          label_visibility="collapsed", disabled=not kb)
            a, b = st.columns([6, 1], vertical_alignment="center")
            with a: st.pills("modes", ["Deep Think", "Wide Search"], selection_mode="multi", key="modes", label_visibility="collapsed")
            with b:
                try: st.form_submit_button("", icon=":material/arrow_upward:", key="send")
                except TypeError: st.form_submit_button("", icon=":material/arrow_upward:")

def show_sources(srcs):
    if not srcs: return
    seen = sorted({(s, p) for s, p, _ in srcs})
    st.markdown("".join(f'<span class="chip">{html.escape(s)} · p.{p}</span>' for s, p in seen), unsafe_allow_html=True)
    with st.expander("View source passages"):
        for s, p, t in srcs:
            st.markdown(f'<div class="pass"><b>{html.escape(s)}</b> · page {p}<br>{html.escape(t[:380])}</div>', unsafe_allow_html=True)

# ---- main ----
if empty:
    st.markdown(f'<div class="hello">{FOX}<span>Hi! What\'s on your mind today?</span></div>', unsafe_allow_html=True)
    composer("cmp_mid")
    if kb:
        st.write("")
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
else:
    if q:
        if not chat:
            cid = uuid.uuid4().hex[:8]; ss.chats[cid] = {"title": q[:40], "msgs": []}; ss.order.insert(0, cid); ss.cur = cid; chat = ss.chats[cid]
        chat["msgs"].append({"role": "user", "text": q})
    for m in chat["msgs"]:
        with st.chat_message(m["role"]):
            st.markdown(m["text"]); show_sources(m.get("srcs"))
    if q:
        with st.chat_message("assistant"):
            with st.spinner("Thinking" if deep else "Searching your documents"):
                try: a, s = ask(q, deep, wide)
                except Exception: a, s = "Something went wrong while searching. Please try again.", []
            def gen():
                for w in a.split(" "): yield w + " "; time.sleep(0.012)
            st.write_stream(gen()); show_sources(s)
        chat["msgs"].append({"role": "assistant", "text": a, "srcs": s})
    composer("cmp_fixed")

# ---- sidebar (rendered last so titles include the new chat) ----
with st.sidebar:
    st.markdown(f'<div class="brand">{FOX}<span>TRAG AI</span></div>', unsafe_allow_html=True)
    if st.button("New chat", icon=":material/add_circle:", key="newchat", use_container_width=True):
        ss.cur = None; st.rerun()
    st.markdown('<div class="side-h">Today</div>', unsafe_allow_html=True)
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
            n = index_files([(f.name, f) for f in new])
        ss.done |= {(f.name, f.size) for f in new}
        st.success(f"Indexed {n} passages"); st.rerun()
    for name, n in kb:
        st.markdown(f'<div class="doc"><b>{html.escape(name)}</b><span>{n} passages indexed</span></div>', unsafe_allow_html=True)
    if not kb: st.markdown('<div class="empty">No documents yet. PDFs are indexed automatically on upload.</div>', unsafe_allow_html=True)
    st.markdown('<div class="who"><i>G</i>Guest</div>', unsafe_allow_html=True)

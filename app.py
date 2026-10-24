import html, uuid, time
import streamlit as st
st.set_page_config(page_title="TRAG AI", page_icon=":material/school:", layout="wide", initial_sidebar_state="expanded")
from rag import ask, docs, topics
from ingest import index as index_files, remove as remove_doc
from style import css, OWL

ss = st.session_state
ss.setdefault("theme", st.query_params.get("theme", "light") if st.query_params.get("theme") in ("light", "dark") else "light")
for k, v in dict(chats={}, order=[], cur=None, done=set(), pending=None, view="chat", bm=[], tc={}).items(): ss.setdefault(k, v)
st.markdown(css(ss.theme), unsafe_allow_html=True)

@st.cache_data(ttl=30, show_spinner=False)
def kb_list(): return docs()
try: kb = kb_list()
except Exception: kb = []

# ---------- read submitted input before layout ----------
q = ss.pending
if not q and (ss.get("send") or "send" not in ss): q = (ss.get("txt") or "").strip()
ss.pending = None
if q: ss.view = "chat"
chat = ss.chats.get(ss.cur)
deep, wide = bool(ss.get("deep")), bool(ss.get("wide"))
TITLES = {"docs": "Documents", "topics": "Explore topics", "bm": "Bookmarks"}

def handle_upload(files):
    new = [f for f in files or [] if (f.name, f.size) not in ss.done]
    if new:
        with st.spinner(f"Indexing {len(new)} file(s)"):
            n = index_files([(f.name, f) for f in new])
        ss.done |= {(f.name, f.size) for f in new}; kb_list.clear()
        st.toast(f"Indexed {n} passages from {len(new)} file(s)", icon=":material/check_circle:"); st.rerun()

def set_theme(t):
    ss.theme = t; st.query_params["theme"] = t; st.rerun()

def topbar(title):
    _, c, r = st.columns([1, 5, 2], vertical_alignment="center")
    c.markdown(f'<div class="ttl">{html.escape(title)}</div>', unsafe_allow_html=True)
    with r:
        a, b, s = st.columns(3)
        with a, st.container(key=("tba_" if ss.theme == "light" else "tb_") + "sun"):
            if st.button("", icon=":material/light_mode:", key="sun", help="Light theme"): set_theme("light")
        with b, st.container(key=("tba_" if ss.theme == "dark" else "tb_") + "moon"):
            if st.button("", icon=":material/dark_mode:", key="moon", help="Dark theme"): set_theme("dark")
        with s, st.container(key="settings"):
            with st.popover("", icon=":material/settings:"):
                st.markdown("**Answer settings**")
                st.toggle("Deep Think (longer reasoning)", key="deep")
                st.toggle("Wide Search (8 passages)", key="wide")
    st.markdown('<div class="topline"></div>', unsafe_allow_html=True)

def show_sources(srcs):
    if not srcs: return
    seen = sorted({(s, p) for s, p, _ in srcs})
    st.markdown("".join(f'<span class="chip">{html.escape(s)} · p.{p}</span>' for s, p in seen), unsafe_allow_html=True)
    with st.expander("View source passages"):
        for s, p, t in srcs:
            st.markdown(f'<div class="pass"><b>{html.escape(s)}</b> · page {p}<br>{html.escape(t[:380])}</div>', unsafe_allow_html=True)

def bookmark(key, question, a, srcs):
    on = any(b["a"] == a for b in ss.bm)
    with st.container(key=("bmon_" if on else "bm_") + key):
        if st.button("", icon=":material/bookmark:", key="b" + key, help="Remove bookmark" if on else "Bookmark this answer"):
            ss.bm = [b for b in ss.bm if b["a"] != a] if on else ss.bm + [{"q": question, "a": a, "srcs": srcs}]
            st.rerun()

def composer():
    with st.container(key="cmp"):
        with st.popover("", icon=":material/attach_file:"):
            st.markdown("**Add PDFs to the knowledge base**")
            up = st.file_uploader("PDF", type="pdf", accept_multiple_files=True, key="up_clip", label_visibility="collapsed")
        with st.form("cmp_f", clear_on_submit=True, border=False):
            a, b = st.columns([14, 1], vertical_alignment="center")
            with a: st.text_input("msg", key="txt", label_visibility="collapsed",
                                  placeholder="Message TRAG AI" if kb else "Add documents first (paperclip icon)")
            with b:
                try: st.form_submit_button("", icon=":material/arrow_upward:", key="send")
                except TypeError: st.form_submit_button("", icon=":material/arrow_upward:")
        st.markdown('<div class="note">TRAG AI can make mistakes. Please verify important information.</div>', unsafe_allow_html=True)
    handle_upload(up)

# ======================= MAIN =======================
view = ss.view
topbar(TITLES.get(view) or (chat["title"] if chat else (q[:40] if q else "New Chat")))

if view == "docs":
    st.markdown('<h3 class="pg">Documents</h3><p class="pgs">PDFs are chunked, embedded and indexed automatically when uploaded.</p>', unsafe_allow_html=True)
    handle_upload(st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="up_docs", label_visibility="collapsed"))
    if not kb: st.markdown('<div class="card"><span>No documents yet. Upload PDFs above to start.</span></div>', unsafe_allow_html=True)
    for name, n in kb:
        a, b = st.columns([9, 1], vertical_alignment="center")
        a.markdown(f'<div class="card"><b>{html.escape(name)}</b><br><span>{n} passages indexed</span></div>', unsafe_allow_html=True)
        if b.button("", icon=":material/delete:", key=f"rm_{name}", help="Remove document"):
            remove_doc(name); ss.done = {d for d in ss.done if d[0] != name}; kb_list.clear(); st.rerun()

elif view == "topics":
    st.markdown('<h3 class="pg">Explore topics</h3><p class="pgs">Pick a document, see what it covers, and ask about any topic in one click.</p>', unsafe_allow_html=True)
    if not kb: st.markdown('<div class="card"><span>Add a document first.</span></div>', unsafe_allow_html=True)
    else:
        pick = st.selectbox("Document", [k for k, _ in kb], label_visibility="collapsed")
        if st.button("Generate topics", key="gen", icon=":material/auto_awesome:"):
            with st.spinner("Reading document"):
                try: ss.tc[pick] = topics(pick)
                except Exception: st.toast("Could not read this document. Try again.")
        cols = st.columns(2)
        for i, t in enumerate(ss.tc.get(pick, [])):
            if cols[i % 2].button(t, key=f"tp{i}", use_container_width=True): ss.pending = f"Explain: {t}"; st.rerun()

elif view == "bm":
    st.markdown('<h3 class="pg">Bookmarks</h3><p class="pgs">Answers you saved for later.</p>', unsafe_allow_html=True)
    if not ss.bm: st.markdown('<div class="card"><span>Nothing saved yet. Use the bookmark icon under any answer.</span></div>', unsafe_allow_html=True)
    for i, b in enumerate(list(ss.bm)):
        x, y = st.columns([12, 1], vertical_alignment="top")
        x.markdown(f'<div class="card"><div class="q">{html.escape(b["q"])}</div>{html.escape(b["a"])}</div>', unsafe_allow_html=True)
        if y.button("", icon=":material/close:", key=f"rb{i}", help="Remove"): ss.bm.pop(i); st.rerun()

else:  # chat
    if q and not chat:
        cid = uuid.uuid4().hex[:8]; ss.chats[cid] = {"title": q[:40], "msgs": []}; ss.order.insert(0, cid); ss.cur = cid; chat = ss.chats[cid]
    if q: chat["msgs"].append({"role": "user", "text": q})
    if not (chat and chat["msgs"]):
        st.markdown(f'<div class="hero">{OWL}<div class="t">Welcome</div>'
                    '<div class="s">Ask anything about your college documents, or pick a starting point below.</div></div>', unsafe_allow_html=True)
        if kb:
            ex = [("Summarise key rules", ":material/description:", "Give a short summary of the key rules in my documents"),
                  ("Attendance rules", ":material/event_available:", "What is the minimum attendance required to appear for the semester examination?"),
                  ("Exam revaluation", ":material/fact_check:", "What is the procedure for examination revaluation?"),
                  ("Registration documents", ":material/folder_open:", "What documents are required for registration?"),
                  ("Placement eligibility", ":material/work:", "What is the eligibility criterion for placement?"),
                  ("Fee and refund rules", ":material/payments:", "What are the fee payment and refund rules?")]
            cols = st.columns(3)
            for i, (lab, ico, qq) in enumerate(ex):
                if cols[i % 3].button(lab, icon=ico, key=f"ex{i}", use_container_width=True): ss.pending = qq; st.rerun()
        else:
            if st.button("Add documents to begin", icon=":material/upload_file:", key="go_docs"): ss.view = "docs"; st.rerun()
    else:
        msgs = chat["msgs"]
        for i, m in enumerate(msgs):
            with st.chat_message(m["role"]):
                st.markdown(m["text"])
                if m["role"] == "assistant":
                    show_sources(m.get("srcs")); bookmark(f"{ss.cur}_{i}", msgs[i - 1]["text"], m["text"], m.get("srcs"))
        if q:
            with st.chat_message("assistant"):
                with st.spinner("Thinking" if deep else "Searching your documents"):
                    try: a, s = ask(q, deep, wide)
                    except Exception: a, s = "Something went wrong while searching. Please try again.", []
                def gen():
                    for w in a.split(" "): yield w + " "; time.sleep(0.012)
                st.write_stream(gen()); show_sources(s)
            msgs.append({"role": "assistant", "text": a, "srcs": s}); bookmark(f"{ss.cur}_{len(msgs)-1}", q, a, s)
    composer()

# ======================= SIDEBAR =======================
with st.sidebar:
    st.markdown(f'<div class="brand">{OWL}<span>TRAG AI</span></div>', unsafe_allow_html=True)
    if st.button("New Chat", icon=":material/add:", key="newchat", use_container_width=True): ss.cur = None; ss.view = "chat"; st.rerun()
    st.write("")
    for key, label, ico in [("chat", "Home", ":material/home:"), ("docs", "Documents", ":material/folder:"),
                            ("topics", "Explore topics", ":material/explore:"), ("bm", "Bookmarks", ":material/bookmark:")]:
        with st.container(key=("navact_" if ss.view == key else "nav_") + key):
            if st.button(label, icon=ico, key="n_" + key, use_container_width=True): ss.view = key; st.rerun()
    st.markdown('<div class="side-h">Today</div>', unsafe_allow_html=True)
    if not ss.order: st.markdown('<div class="empty">No conversations yet.</div>', unsafe_allow_html=True)
    for cid in list(ss.order):
        a, b = st.columns([6, 1], vertical_alignment="center")
        with a, st.container(key=f"{'act' if cid == ss.cur and ss.view == 'chat' else 'chat'}_{cid}"):
            if st.button(ss.chats[cid]["title"], icon=":material/chat_bubble_outline:", key=f"open_{cid}", use_container_width=True): ss.cur = cid; ss.view = "chat"; st.rerun()
        with b, st.container(key=f"del_{cid}"):
            if st.button("", icon=":material/close:", key=f"x_{cid}", help="Delete chat"):
                ss.order.remove(cid); ss.chats.pop(cid, None)
                if ss.cur == cid: ss.cur = None
                st.rerun()
    st.markdown(f'<div class="who"><i>G</i><div><b>Guest</b><small>{len(kb)} documents indexed</small></div></div>', unsafe_allow_html=True)

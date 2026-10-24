import streamlit as st
st.set_page_config(page_title="College Document Q&A", page_icon="🎓", layout="centered")
from rag import ask, docs, topics
from ingest import index
import config as c

st.markdown("""<style>
#MainMenu, footer {visibility:hidden}
.block-container {padding-top:2rem; max-width:820px}
h1 {font-weight:700; letter-spacing:-.02em; margin-bottom:0}
.sub {color:#64748B; margin:.2rem 0 1.4rem}
[data-testid=stSidebar] {background:#fff; border-right:1px solid #E2E8F0}
.doc {display:flex; justify-content:space-between; padding:.45rem .7rem; margin:.25rem 0; border:1px solid #E2E8F0;
      border-radius:8px; font-size:.88rem; background:#F8FAFC}
.doc span:last-child {color:#64748B}
.chip {display:inline-block; padding:.2rem .65rem; margin:.15rem .2rem .15rem 0; border-radius:999px;
       background:#EEF2FF; color:#3730A3; font-size:.82rem}
.src {font-size:.8rem; color:#475569}
</style>""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("msgs", []); ss.setdefault("done", set())

with st.sidebar:
    st.markdown("### 📚 Knowledge base")
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    new = [f for f in up or [] if (f.name, f.size) not in ss.done]
    if new:
        with st.spinner(f"Indexing {len(new)} file(s)…"):
            n = index([(f.name, f) for f in new])
        ss.done |= {(f.name, f.size) for f in new}
        st.success(f"Indexed {n} chunks")
    try: kb = docs()
    except Exception: kb = []
    if kb:
        for name, n in kb: st.markdown(f'<div class="doc"><span>📄 {name}</span><span>{n} chunks</span></div>', unsafe_allow_html=True)
    else:
        st.caption("No documents yet. Upload PDFs above — they are indexed automatically.")
    if st.button("Clear chat", use_container_width=True): ss.msgs = []; st.rerun()

st.markdown("# 🎓 College Document Q&A")
st.markdown('<p class="sub">Ask in plain language. Answers come only from your uploaded documents, with sources.</p>', unsafe_allow_html=True)

if kb:
    with st.expander("💡 What can I ask? (topics per document)"):
        pick = st.selectbox("Document", [k for k, _ in kb], label_visibility="collapsed")
        if st.button("Show topics"):
            with st.spinner("Reading document…"):
                st.markdown("".join(f'<span class="chip">{t}</span>' for t in topics(pick)), unsafe_allow_html=True)

for m in ss.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["text"])
        if m.get("srcs"):
            with st.expander(f"Sources ({len(m['srcs'])})"):
                for s, p, t in m["srcs"]:
                    st.markdown(f'<div class="src"><b>{s}</b> · page {p}</div>', unsafe_allow_html=True); st.caption(t[:350] + "…")

if q := st.chat_input("Ask about your documents…" if kb else "Upload a PDF first"):
    ss.msgs.append({"role": "user", "text": q})
    with st.chat_message("user"): st.markdown(q)
    with st.chat_message("assistant"):
        if not kb:
            a, s = "Please upload and index at least one PDF first.", []
        else:
            with st.spinner("Searching documents…"):
                try: a, s = ask(q.strip())
                except Exception: a, s = "Something went wrong while searching. Please try again.", []
        st.markdown(a)
    ss.msgs.append({"role": "assistant", "text": a, "srcs": s}); st.rerun()

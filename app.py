import streamlit as st
from rag import ask
st.title("College Document Q&A Assistant")

with st.sidebar:
    st.header("Add documents")
    up = st.file_uploader("Upload college PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Index PDFs") and up:
        from ingest import index
        with st.spinner("Indexing..."):
            n = index([(f.name, f) for f in up])
        st.success(f"Indexed {n} chunks")

q = st.text_input("Enter your question")
if st.button("Ask") and q.strip():
    try:
        with st.spinner("Searching documents..."):
            ans, srcs = ask(q.strip())
    except Exception:
        st.warning("No documents indexed yet. Upload PDFs in the sidebar and click Index PDFs.")
        st.stop()
    st.write(ans)
    if srcs:
        st.caption("Sources: " + "; ".join(f"{s} (p.{p})" for s, p in srcs))

import streamlit as st
from rag import ask
st.title("College Document Q&A Assistant")
q = st.text_input("Enter your question")
if st.button("Ask") and q.strip():
    with st.spinner("Searching documents..."):
        ans, srcs = ask(q.strip())
    st.write(ans)
    if srcs:
        st.caption("Sources: " + "; ".join(f"{s} (p.{p})" for s, p in srcs))

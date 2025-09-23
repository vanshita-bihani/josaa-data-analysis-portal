import streamlit as st

def load_developers():
    st.title("Meet the Developers")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.image("assets/sanskar.jpg", caption="Sanskar")

    with col2:
        # FIX: Make sure this filename EXACTLY matches the file in your GitHub assets folder.
        # For example, if your file is actually "vanshita.JPG", you must use that.
        st.image("assets/vanshita.jpg", caption="Vanshita")
 
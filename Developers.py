import streamlit as st

def load_developers():
    st.title("Meet the Developers")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("assets/sanskar.jpg", caption="Sanskar")

    with col2:
        # FIX: Make sure this filename EXACTLY matches the file in your GitHub assets folder.
        # For example, if your file is actually "vanshita.JPG", you must use that.
        st.image("assets/vanshita.png", caption="Vanshita")
        
    with col3:
        st.image("assets.abhishek.jpg", caption="Abhishek")

    with col4:
        st.image("assets/devi.jpg", caption="Devi")
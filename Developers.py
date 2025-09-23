import streamlit as st

def load_developers():
    st.title("Meet the Developers")
    st.markdown("---")

    # FIX: Create 4 columns and assign them to 4 variables
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Using the assets folder and the built-in caption for a cleaner look
        st.image("assets/sanskar.jpg", caption="Sanskar")

    with col2:
        st.image("assets/vanshita.png", caption="Vanshita")
        
    with col3:
        # NOTE: Add the correct image file for the other developers
        st.image("assets/abhishek.jpg", caption="Abhishek")

    with col4:
        st.image("assets/devi.jpg", caption="Devi")
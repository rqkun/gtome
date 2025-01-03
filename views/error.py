import streamlit as st
import lib.headers as header
header.add_error_header()
st.error("""
            ### Supabase Connection Error
            Follow the instructions [here](https://docs.streamlit.io/develop/tutorials/databases/supabase) \
            to create your credentials and save it to your `.streamlit/secrets.toml` file.
        """)
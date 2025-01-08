import streamlit as st
from classes.messages import AppMessages
import lib.utils as utils
st.session_state.language = "vi"
utils.add_header()
app_lang = AppMessages(st.session_state.language)
st.error(f"""
            ### {AppMessages.SUPABASE_ERROR_DESCRIPTION}
            Follow the instructions [here](https://docs.streamlit.io/develop/tutorials/databases/supabase) \
            to create your credentials and save it to your `.streamlit/secrets.toml` file.
        """)
import streamlit as st
import lib.headers as header

def login():
    with st.container(border=True):
        st.header("Authentication")
        col1,col2 = st.columns([9,1],vertical_alignment="bottom")
        with col1:
            account = st.text_input(":material/person: Username")
        with col2:
            header.add_change_theme()
        col1,col2 = st.columns([5,1],vertical_alignment="bottom")
        with col1:
            password = st.text_input(":material/lock: Password",type="password")
        with col2:
            login_bttn = st.button("Login",use_container_width=True,type="primary",icon=":material/key:")
        if login_bttn:
            if (st.secrets.account.admin == account and st.secrets.account.password == password):
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Wrong account or password.",icon=":material/sentiment_stressed:")
        
    
        
def logout():
    st.session_state.login = False
    st.rerun()

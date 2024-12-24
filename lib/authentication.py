import streamlit as st
import lib.headers as header

def login():
    if st.secrets.account.admin is None or st.secrets.account.password is None:
        pass
    else:
        with st.container(border=True):
            _,col2 = st.columns([10,1],vertical_alignment="bottom")
            with col2:
                header.add_change_theme()
            st.markdown("""
                        <div style="text-align: center; font-size: 100px; font-weight: bold;">GTOME</div>
                        """,unsafe_allow_html=True)
            account = st.text_input(":material/person: Username")
            password = st.text_input(":material/lock: Password",type="password")
            st.write("")
            login_bttn = st.button("Login",use_container_width=True,type="primary",icon=":material/key:")
            st.write("")
            if login_bttn:
                if (st.secrets.account.admin == account and st.secrets.account.password == password):
                    st.session_state.login = True
                    st.rerun()
                else:
                    st.error("Wrong account or password.",icon=":material/sentiment_stressed:")
            
    
        
def logout():
    st.session_state.login = False
    st.rerun()

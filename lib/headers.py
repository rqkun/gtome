import streamlit as st
import lib.authentication as auth
  
def ChangeTheme():
  previous_theme = st.session_state.themes["current_theme"]
  tdict = st.session_state.themes["light"] if st.session_state.themes["current_theme"] == "light" else st.session_state.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  st.session_state.themes["refreshed"] = False
  if previous_theme == "dark": st.session_state.themes["current_theme"] = "light"
  elif previous_theme == "light": st.session_state.themes["current_theme"] = "dark"

@st.fragment
def add_change_theme():
    btn_face = st.session_state.themes["light"]["button_face"] if st.session_state.themes["current_theme"] == "light" else st.session_state.themes["dark"]["button_face"]
    st.button(btn_face,on_click=ChangeTheme,use_container_width=True)
            
    if st.session_state.themes["refreshed"] == False:
        st.session_state.themes["refreshed"] = True
        st.rerun()

def add_header():
    with st.header(""):
        col1, col2,_,col3,col4 = st.columns([1,1,4,2,1])
        if col2.button(":material/home:",type="secondary",use_container_width=True):
                st.switch_page("views/home.py")
        if col4.button(":material/exit_to_app:",type="secondary",use_container_width=True):
                    auth.logout()

        with col3:
            with st.popover("Menu",use_container_width=True, icon=":material/menu:"):
                st.page_link("views/add.py", label="Insert", icon=":material/add_task:",use_container_width=True)
                st.page_link("views/view.py", label="Dashboard", icon=":material/empty_dashboard:",use_container_width=True)
                st.page_link("views/manage.py", label="Manage", icon=":material/lists:",use_container_width=True)
                st.page_link("https://github.com/rqkun/gtome/issues", label="Report", icon=":material/bug_report:",use_container_width=True)
        with col1:
            # Create a toggle button
            add_change_theme()
import streamlit as st
import lib.authentication as auth

ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "dark",
                    "refreshed": True,
                    
                    "light": {"theme.base": "dark",
                              "button_face": ":material/dark_mode:"},

                    "dark":  {"theme.base": "light",
                              "button_face": ":material/light_mode:"},
                    }
  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"

@st.fragment
def add_change_theme():
    btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
    st.button(btn_face,on_click=ChangeTheme,use_container_width=True)
            
    if ms.themes["refreshed"] == False:
        ms.themes["refreshed"] = True
        st.rerun()

def add_header():
    with st.header(""):
        left, _,_,misc, right = st.columns([2,2,4,1,1])
        if left.button("Menu","", use_container_width=True,type="secondary", icon=":material/menu_open:"):
            st.switch_page("views/home.py")
        if right.button(":material/exit_to_app:","", use_container_width=True,type="secondary"):
            auth.logout()
        with misc:
            # Create a toggle button
            add_change_theme()
import streamlit as st


def google_sign_in_button(
        componet, url: str, color="#FD504D"
    ):
        componet.markdown(
        f"""

        <a href="{url}" target="{st.secrets.host.target}">
            <button class="gsi-material-button" style="-moz-user-select:none;-webkit-user-select:none;-ms-user-select:none;-webkit-appearance:none;background-color:#f2f2f2;background-image:none;border-style:none;-webkit-border-radius:4px;border-radius:4px;-webkit-box-sizing:border-box;box-sizing:border-box;color:#1f1f1f;cursor:pointer;font-family:'Roboto', arial, sans-serif;font-size:14px;height:40px;letter-spacing:0.25px;outline-style:none;overflow:hidden;padding-top:0;padding-bottom:0;padding-right:12px;padding-left:12px;position:relative;text-align:center;-webkit-transition:background-color .218s, border-color .218s, box-shadow .218s;transition:background-color .218s, border-color .218s, box-shadow .218s;vertical-align:middle;white-space:nowrap;width:100%;max-width:400px;min-width:min-content;" >
                <div class="gsi-material-button-state" style="-webkit-transition:opacity .218s;transition:opacity .218s;bottom:0;left:0;opacity:0;position:absolute;right:0;top:0" ></div>
                <div class="gsi-material-button-content-wrapper" style="-webkit-align-items:center;align-items:center;display:flex;-webkit-flex-direction:row;flex-direction:row;-webkit-flex-wrap:nowrap;flex-wrap:nowrap;height:100%;justify-content:space-between;position:relative;width:100%;" >
                <div class="gsi-material-button-icon" style="height:20px;margin-right:1px;min-width:20px;width:20px;" >
                    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display:block;" >
                    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                    <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                    <path fill="none" d="M0 0h48v48H0z"></path>
                    </svg>
                </div>
                <span class="gsi-material-button-contents" style="-webkit-flex-grow:1;flex-grow:1;font-family:'Roboto', arial, sans-serif;font-weight:500;overflow:hidden;text-overflow:ellipsis;vertical-align:top;" >Sign in with Google</span>
                <span style="display:none;" >Sign in with Google</span>
                </div>
            </button>
        </a>
        
        """,
            unsafe_allow_html=True,
        )
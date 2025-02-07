import streamlit as st
from configs.messages import AppMessages
import components.custom_components as utils

utils.error_page_header()
app_lang = AppMessages(st.session_state.language)
if st.session_state.language == "vi":
    if st.session_state.connection_error["GSheet"]["connected"] is False:
        gcontainer = st.expander(app_lang.GSHEET_CONNECTION_ERROR)
        gcontainer.error(f"""
                    ### {app_lang.GSHEET_CONNECTION_ERROR}
                    - Làm theo hướng dẫn [tại đây](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) để tạo thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
                    - Truy cập [tại đây](https://console.cloud.google.com/) và tạo một Client xác thực và sao chép thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
                """)
        gcontainer.write(st.session_state.connection_error["GSheet"]["error"].args[0].json())
else:
    if st.session_state.connection_error["GSheet"]["connected"] is False:
        gcontainer = st.expander(app_lang.GSHEET_CONNECTION_ERROR)
        gcontainer.error(f"""
                    ### {app_lang.GSHEET_CONNECTION_ERROR}
                    - Follow the instructions [here](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) to create your credentials and save it to your `.streamlit/secrets.toml` file.
                    - Go to [here](https://console.cloud.google.com/) and create an authentication Client and copy your credentials and save it to your `.streamlit/secrets.toml` file.
                    - Go to [here](https://firebase.google.com/) and create an authentication app and add your API_KEY to `.streamlit/secrets.toml` file.
                """)
        gcontainer.write(st.session_state.connection_error["GSheet"]["error"].args[0].json())
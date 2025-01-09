import streamlit as st
from classes.messages import AppMessages
import lib.utils as utils

utils.add_error_header()
app_lang = AppMessages(st.session_state.language)
if st.session_state.language == "vi":
    if st.session_state.connection_error["Supabase"]["connected"] is False:
        scontainer = st.expander(app_lang.SUPABASE_ERROR_DESCRIPTION)
        scontainer.error(f"""
                    ### {app_lang.SUPABASE_ERROR_DESCRIPTION}
                    Làm theo hướng dẫn [tại đây](https://docs.streamlit.io/develop/tutorials/databases/supabase)\
                    để tạo thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
                """)
        scontainer.write(st.session_state.connection_error["Supabase"]["error"])
    if st.session_state.connection_error["GSheet"]["connected"] is False:
        gcontainer = st.expander(app_lang.GSHEET_CONNECTION_ERROR)
        gcontainer.error(f"""
                    ### {app_lang.GSHEET_CONNECTION_ERROR}
                    - Làm theo hướng dẫn [tại đây](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) để tạo thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
                    - Truy cập [tại đây](https://console.cloud.google.com/) và tạo một Client xác thực và sao chép thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
                    - Truy cập [tại đây](https://firebase.google.com/) và tạo một ứng dụng xác thực và thêm API_KEY của bạn vào tệp `.streamlit/secrets.toml`.
                    - Mở bảng điều khiển firebase của bạn và đi tới Authentication > Sign-in methods và thêm nhà cung cấp Email/Password.
                    - Mở bảng điều khiển firebase của bạn và đi tới Authentication > Sign-in methods và thêm nhà cung cấp Google, điền vào trường `client_id` và `secret`.
                """)
        gcontainer.write(st.session_state.connection_error["GSheet"]["error"].args[0].json())
else:
    if st.session_state.connection_error["Supabase"]["connected"] is False:
        scontainer = st.expander(app_lang.SUPABASE_ERROR_DESCRIPTION)
        scontainer.error(f"""
                    ### {app_lang.SUPABASE_ERROR_DESCRIPTION}
                    Follow the instructions [here](https://docs.streamlit.io/develop/tutorials/databases/supabase) \
                    to create your credentials and save it to your `.streamlit/secrets.toml` file.
                """)
        scontainer.write(st.session_state.connection_error["Supabase"]["error"])
    if st.session_state.connection_error["GSheet"]["connected"] is False:
        gcontainer = st.expander(app_lang.GSHEET_CONNECTION_ERROR)
        gcontainer.error(f"""
                    ### {app_lang.GSHEET_CONNECTION_ERROR}
                    - Follow the instructions [here](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) to create your credentials and save it to your `.streamlit/secrets.toml` file.
                    - Go to [here](https://console.cloud.google.com/) and create an authentication Client and copy your credentials and save it to your `.streamlit/secrets.toml` file.
                    - Go to [here](https://firebase.google.com/) and create an authentication app and add your API_KEY to `.streamlit/secrets.toml` file.
                    - Open your firebase console and go to Authentication > Sign-in methods and add the Email/Password provider.
                    - Open your firebase console and go to Authentication > Sign-in methods and add the Google provider, fill the `client_id` and `secret` field.
                """)
        gcontainer.write(st.session_state.connection_error["GSheet"]["error"].args[0].json())
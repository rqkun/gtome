[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rqkun-gtome.streamlit.app/)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/rqkun/gtome/blob/main/readme.md)
[![vi](https://img.shields.io/badge/lang-vn-yellow.svg)](https://github.com/rqkun/gtome/blob/main/readme_vn.md)

# Ứng dụng GTOME Streamlit

Chào mừng bạn đến với ứng dụng GTOME Streamlit! Ứng dụng thân thiện với người dùng này được thiết kế để đơn giản hóa GTOME của bạn bằng cách nhập dữ liệu từ Google Sheets một cách liền mạch. Với ứng dụng này, bạn có thể theo dõi chi tiêu, quản lý ngân sách và tạo các báo cáo chi tiêu chi tiết một cách dễ dàng.
Kiểm tra trang web [tại đây](https://rqkun-gtome.streamlit.app/)
## Tính năng

- **Tích hợp Google Sheets**: Dễ dàng lưu trữ dữ liệu chi tiêu của bạn từ Google Sheets.
- **Theo dõi chi tiêu**: Theo dõi chi tiêu của bạn một cách dễ dàng.
- **Lưới dữ liệu**: Đặt và quản lý ngân sách bằng cách sử dụng các lưới dữ liệu.
- **Trực quan hóa dữ liệu**: Trực quan hóa dữ liệu chi tiêu của bạn bằng các biểu đồ và đồ thị để hiểu rõ hơn.

## Bắt đầu

### Yêu cầu

- Python 3.9 trở lên
- Streamlit
- Thông tin đăng nhập API của Google

### Cài đặt

1. Clone repository:
    ```sh
    git clone https://github.com/rqkun/gtome.git
    ```

2. Cài đặt các phụ thuộc cần thiết:
    ```sh
    pip install -r requirements.txt
    ```

3. Thiết lập thông tin đăng nhập API của Google:
    - Làm theo hướng dẫn [tại đây](https://github.com/streamlit/gsheets-connection?tab=readme-ov-file#service-account--crud-example) để tạo thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.
    - Truy cập [tại đây](https://console.cloud.google.com/) và tạo một Client xác thực và sao chép thông tin đăng nhập của bạn và lưu vào tệp `.streamlit/secrets.toml`.

4. Tệp `.streamlit/secrets.toml` và secret của Streamlit Cloud của bạn sẽ trông như thế này:
    ```
    [auth]
    redirect_uri = "http://localhost:8501/oauth2callback"
    cookie_secret = "" # self generated
    client_id = ""
    client_secret = ""
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

    [connections.gsheets]
    spreadsheet = "<googlesheet_url>"
    type = "service_account"
    project_id = ""
    private_key_id= ""
    private_key=""
    client_email= ""
    client_id= ""
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri ="https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url =""
    ```
### Chạy ứng dụng

1. Khởi động ứng dụng Streamlit:
    ```sh
    streamlit run app.py
    ```

2. Mở trình duyệt web của bạn và truy cập `http://localhost:8501` để truy cập ứng dụng.

## Sử dụng

1. **Google Sheet**: Sử dụng ứng dụng để lưu trữ dữ liệu chi tiêu của bạn vào Google Sheets.
2. **Theo dõi chi tiêu**: Thêm, chỉnh sửa và xóa các mục chi tiêu để cập nhật hồ sơ của bạn.
3. **Trực quan hóa dữ liệu**: Xem dữ liệu chi tiêu của bạn thông qua các biểu đồ và đồ thị khác nhau để có cái nhìn sâu sắc hơn.

---

Cảm ơn bạn đã sử dụng ứng dụng GTOME Streamlit! Chúng tôi hy vọng nó sẽ giúp bạn quản lý chi tiêu của mình hiệu quả hơn.
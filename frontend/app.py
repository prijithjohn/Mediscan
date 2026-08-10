import streamlit as st

from frontend.api_client import (
    ApiClientError,
    get_alerts,
    get_prescription,
    get_prescriptions,
    get_usage,
    health_check,
    login,
    logout,
    register,
    upload_prescription,
)


def initialize_state() -> None:
    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None
        st.session_state.username = ""
        st.session_state.email = ""
        st.session_state.usage = None
        st.session_state.prescriptions = []
        st.session_state.alerts = []
        st.session_state.selected_prescription_id = None
        st.session_state.selected_prescription = None
        st.session_state.last_upload_response = None
        st.session_state.notification = None


def set_notification(message: str, level: str = "info") -> None:
    st.session_state.notification = {"message": message, "level": level}


def clear_auth() -> None:
    st.session_state.auth_token = None
    st.session_state.username = ""
    st.session_state.email = ""
    st.session_state.usage = None
    st.session_state.prescriptions = []
    st.session_state.alerts = []
    st.session_state.selected_prescription_id = None
    st.session_state.selected_prescription = None
    st.session_state.last_upload_response = None
    st.session_state.notification = None


def fetch_dashboard_data() -> None:
    if not st.session_state.auth_token:
        return

    try:
        st.session_state.usage = get_usage(st.session_state.auth_token)
    except ApiClientError as exc:
        set_notification(f"Unable to load usage: {exc}", "error")
        st.session_state.usage = None

    try:
        st.session_state.prescriptions = get_prescriptions(st.session_state.auth_token)
    except ApiClientError as exc:
        set_notification(f"Unable to load prescriptions: {exc}", "error")
        st.session_state.prescriptions = []

    try:
        st.session_state.alerts = get_alerts(st.session_state.auth_token)
    except ApiClientError as exc:
        set_notification(f"Unable to load alerts: {exc}", "error")
        st.session_state.alerts = []

    if st.session_state.prescriptions and st.session_state.selected_prescription_id is None:
        st.session_state.selected_prescription_id = st.session_state.prescriptions[0]["id"]


def get_selected_prescription() -> dict | None:
    if not st.session_state.selected_prescription_id:
        return None
    if (
        st.session_state.selected_prescription
        and st.session_state.selected_prescription.get("id") == st.session_state.selected_prescription_id
    ):
        return st.session_state.selected_prescription
    try:
        selected = get_prescription(st.session_state.auth_token, st.session_state.selected_prescription_id)
        st.session_state.selected_prescription = selected
        return selected
    except ApiClientError as exc:
        set_notification(f"Unable to load selected prescription: {exc}", "error")
        return None


def show_auth_form() -> None:
    with st.expander("Login / Register", expanded=True):
        auth_mode = st.radio("Authentication", ["Login", "Register"])
        username = st.text_input("Username", value=st.session_state.username, key="auth_username")
        password = st.text_input("Password", type="password", key="auth_password")
        email = st.text_input("Email", value=st.session_state.email, key="auth_email") if auth_mode == "Register" else None

        if st.button("Submit", key="auth_submit"):
            if auth_mode == "Register":
                if not username or not password or not email:
                    set_notification("Username, email and password are required.", "error")
                else:
                    try:
                        result = register(username, email, password)
                        st.session_state.auth_token = result["access_token"]
                        st.session_state.username = username
                        st.session_state.email = email
                        set_notification("Registration successful. Logged in.", "success")
                        fetch_dashboard_data()
                    except ApiClientError as exc:
                        set_notification(str(exc), "error")
            else:
                if not username or not password:
                    set_notification("Username and password are required.", "error")
                else:
                    try:
                        result = login(username, password)
                        st.session_state.auth_token = result["access_token"]
                        st.session_state.username = username
                        set_notification("Login successful.", "success")
                        fetch_dashboard_data()
                    except ApiClientError as exc:
                        set_notification(str(exc), "error")


def show_upload_panel() -> None:
    with st.expander("Upload Prescription Image", expanded=True):
        uploaded_file = st.file_uploader("Upload a handwriting image", type=["jpg", "jpeg", "png", "webp"], key="upload_file")
        if uploaded_file is not None:
            if st.button("Process Prescription", key="process_prescription"):
                try:
                    response = upload_prescription(
                        token=st.session_state.auth_token,
                        file_name=uploaded_file.name,
                        file_bytes=uploaded_file.getvalue(),
                        content_type=uploaded_file.type,
                    )
                    st.session_state.last_upload_response = response
                    set_notification("Prescription processed successfully.", "success")
                    fetch_dashboard_data()
                except ApiClientError as exc:
                    set_notification(str(exc), "error")

        if st.session_state.last_upload_response:
            st.markdown("**Last processed prescription:**")
            st.json(st.session_state.last_upload_response)


def show_dashboard() -> None:
    st.success(f"Logged in as {st.session_state.username}")
    cols = st.columns([3, 1])
    with cols[1]:
        if st.button("Refresh dashboard", key="refresh_dashboard"):
            fetch_dashboard_data()
        if st.button("Logout", key="logout"):
            logout()
            clear_auth()
            st.experimental_rerun()

    if st.session_state.usage:
        usage = st.session_state.usage
        st.metric("Used", usage.get("used", 0))
        st.metric("Remaining", usage.get("remaining", 0))
        st.metric("Limit", usage.get("limit", 0))
    else:
        st.info("Usage summary will appear once you have logged in and refreshed the dashboard.")

    show_upload_panel()

    with st.expander("Prescription History", expanded=True):
        if not st.session_state.prescriptions:
            st.info("No prescriptions found yet.")
        else:
            options = [f"{item['created_at']} - {item.get('summary', '')[:60]}" for item in st.session_state.prescriptions]
            selected_index = st.selectbox("Select a prescription", range(len(options)), format_func=lambda i: options[i], key="prescription_index")
            selected = st.session_state.prescriptions[selected_index]
            st.session_state.selected_prescription_id = selected["id"]
            prescription = get_selected_prescription()
            if prescription:
                st.markdown("**Prescription details**")
                st.write(f"**Summary:** {prescription.get('summary', 'N/A')}")
                st.write(f"**Original text:** {prescription.get('original_text', 'N/A')}")
                st.write(f"**Medicines:** {', '.join(prescription.get('medicines') or [])}")
                st.write(f"**Possible conditions:** {', '.join(prescription.get('possible_conditions') or [])}")
                st.write(f"**Warnings:** {prescription.get('warnings', 'N/A')}")

    with st.expander("Alerts", expanded=True):
        if not st.session_state.alerts:
            st.info("No alerts have been generated yet.")
        else:
            for alert in st.session_state.alerts:
                st.markdown(f"**{alert['subject']}**")
                st.write(f"Status: {alert['status']}")
                st.write(f"Recipient: {alert['email']}")
                st.write(f"Message: {alert['message']}")
                st.write(f"Created at: {alert['created_at']}")
                st.divider()


def main() -> None:
    initialize_state()
    st.title("MediScan Frontend")

    backend_status = None
    try:
        backend_status = health_check()
    except ApiClientError as exc:
        st.error(f"Backend health check failed: {exc}")
    except Exception as exc:
        st.error(f"Backend health check failed: {exc}")

    if backend_status:
        st.success("Backend is healthy and ready")

    if st.session_state.notification:
        notification = st.session_state.notification
        if notification["level"] == "error":
            st.error(notification["message"])
        elif notification["level"] == "success":
            st.success(notification["message"])
        else:
            st.info(notification["message"])

    if not st.session_state.auth_token:
        show_auth_form()
    else:
        if st.session_state.usage is None and st.session_state.prescriptions == [] and st.session_state.alerts == []:
            fetch_dashboard_data()
        show_dashboard()


if __name__ == "__main__":
    main()

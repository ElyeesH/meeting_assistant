import streamlit as st
import requests
import re
import os

st.set_page_config(page_title="Meeting Assistant", layout="wide")
st.title("Meeting Assistant — Report Generator")

default_url = os.getenv("API_URL", "http://localhost:8000")

base_url = st.sidebar.text_input("API base URL", value=default_url)
st.sidebar.markdown("Make sure the backend is running and accessible at the URL above.")

st.header("Health Check")
if st.button("Check health"):
    try:
        r = requests.get(f"{base_url}/health", timeout=5)
        if r.ok:
            st.success("Healthy ✅")
            st.json(r.json())
        else:
            st.error(f"Unhealthy — status code {r.status_code}")
            st.text(r.text)
    except Exception as e:
        st.error(f"Health check failed: {e}")

st.markdown("---")

st.header("Generate report from audio")
uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "flac", "ogg", "webm"], help="Upload a meeting recording (wav/mp3/m4a)")

if uploaded_file is not None:
    # Playback in the browser
    try:
        st.audio(uploaded_file)
    except Exception:
        pass

    if st.button("Generate report"):
        with st.spinner("Uploading and generating report... (this may take a while)" ):
            try:
                files = {"audio": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")}
                r = requests.post(f"{base_url}/api/v1/generate-report", files=files, timeout=180)

                if r.status_code == 200:
                    # Try to extract filename from Content-Disposition
                    filename = "report.md"
                    cd = r.headers.get("content-disposition")
                    if cd and "filename=" in cd:
                        m = re.search(r'filename="?([^";]+)"?', cd)
                        if m:
                            filename = m.group(1)

                    text = r.content.decode("utf-8")
                    st.success("Report generated! ✅")
                    st.download_button("Download markdown", data=text, file_name=filename, mime="text/markdown")
                    st.markdown("---")
                    st.markdown(text)
                else:
                    st.error(f"Server returned {r.status_code}")
                    try:
                        st.text(r.json().get("detail", r.text))
                    except Exception:
                        st.text(r.text)
            except Exception as e:
                st.error(f"Request failed: {e}")

st.markdown("---")
st.sidebar.markdown("**Tips:**\n- Ensure the backend is running (`uvicorn app.main:app --reload`).\n- Large audio files may take several seconds to process.")

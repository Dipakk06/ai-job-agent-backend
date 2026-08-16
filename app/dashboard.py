import streamlit as st
import requests


API_URL = "http://localhost:8000"


st.set_page_config(
    page_title="AI Job Agent",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 AI Job Agent")

st.caption(
    "Search jobs, analyze matches and chat with your job opportunities."
)


# Sidebar
with st.sidebar:

    st.header("🔎 Job Agent")

    st.write("Your AI-powered job search assistant.")

    if st.button("🔄 Refresh Jobs"):
        st.rerun()


# Main layout
jobs_tab, chat_tab = st.tabs([
    "💼 Jobs",
    "💬 AI Assistant",
])


# -----------------------------
# JOBS
# -----------------------------

with jobs_tab:

    st.header("Top Job Matches")

    try:

        response = requests.get(
            f"{API_URL}/api/jobs",
            timeout=10,
        )

        if response.status_code == 200:

            jobs = response.json()

            if not jobs:

                st.info("No jobs available yet.")

            for index, job in enumerate(jobs, start=1):

                score = job.get(
                    "match_score",
                    job.get("score", 0)
                )

                with st.container():

                    col1, col2 = st.columns([5, 1])

                    with col1:

                        st.subheader(
                            f"{index}. {job.get('title', 'Unknown Job')}"
                        )

                        st.write(
                            f"🏢 {job.get('company', 'Unknown')}"
                        )

                        st.write(
                            f"📍 {job.get('location', 'Unknown')}"
                        )

                    with col2:

                        st.metric(
                            "Match",
                            f"{score}%"
                        )

                    st.write(
                        job.get(
                            "description",
                            ""
                        )[:500]
                    )

                    if job.get("url"):

                        st.link_button(
                            "View Job",
                            job["url"]
                        )

                    st.divider()

        else:

            st.error("Could not load jobs.")

    except Exception as e:

        st.error(
            f"Backend is not running: {e}"
        )


# -----------------------------
# CHATBOT
# -----------------------------

with chat_tab:

    st.header("💬 AI Job Assistant")

    st.write(
        "Ask anything about your matched jobs."
    )


    if "messages" not in st.session_state:

        st.session_state.messages = []


    # Show previous messages
    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # User input
    prompt = st.chat_input(
        "Ask about your jobs..."
    )


    if prompt:

        # User message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):

            st.markdown(prompt)


        # Call backend
        try:

            response = requests.post(
                f"{API_URL}/api/chat",
                json={
                    "message": prompt
                },
                timeout=60,
            )

            if response.status_code == 200:

                answer = response.json()["response"]

            else:

                answer = (
                    "Sorry, the chatbot API returned an error."
                )

        except Exception as e:

            answer = (
                f"Could not connect to backend: {e}"
            )


        # Assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
        })

        with st.chat_message("assistant"):

            st.markdown(answer)
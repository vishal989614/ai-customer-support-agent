import streamlit as st
import requests


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🤖 AI Customer Support Agent")

st.write(
    "Test your food-delivery customer support backend "
    "through a simple chat interface."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("Customer")

user_id = st.sidebar.number_input(
    "User ID",
    min_value=1,
    value=4,
    step=1
)

st.sidebar.info(
    "Try different User IDs to test "
    "order, payment and ticket ownership."
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            if "details" in message:

                details = message["details"]

                with st.expander("Technical Details"):

                    st.write(
                        "Capability:",
                        details.get("capability")
                    )

                    st.write(
                        "Intent:",
                        details.get("intent")
                    )

                    st.write(
                        "Order ID:",
                        details.get("order_id")
                    )

                    st.write(
                        "Restaurant:",
                        details.get("restaurant_name")
                    )

                    st.write(
                        "Payment ID:",
                        details.get("payment_id")
                    )

                    st.write(
                        "Ticket ID:",
                        details.get("ticket_id")
                    )

                    st.write(
                        "Verification:",
                        details.get("verification")
                    )


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask me anything about your order..."
)


# ---------------------------------------------------------
# SEND REQUEST
# ---------------------------------------------------------

if question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)


    # Call backend

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "question": question,
                        "user_id": user_id
                    },
                    timeout=120
                )


                # Check HTTP response

                response.raise_for_status()

                data = response.json()


                # Get answer

                answer = data.get(
                    "answer",
                    "No response received."
                )


                st.write(answer)


                # Technical information

                with st.expander("Technical Details"):

                    st.write(
                        "Capability:",
                        data.get("capability")
                    )

                    st.write(
                        "Intent:",
                        data.get("intent")
                    )

                    st.write(
                        "Order ID:",
                        data.get("order_id")
                    )

                    st.write(
                        "Restaurant:",
                        data.get("restaurant_name")
                    )

                    st.write(
                        "Payment ID:",
                        data.get("payment_id")
                    )

                    st.write(
                        "Ticket ID:",
                        data.get("ticket_id")
                    )

                    st.write(
                        "Verification:",
                        data.get("verification")
                    )


                # Save response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "details": data
                    }
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running on "
                    "http://127.0.0.1:8000"
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The backend took too long to respond."
                )


            except requests.exceptions.HTTPError as e:

                st.error(
                    f"Backend returned an HTTP error: {e}"
                )


            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )
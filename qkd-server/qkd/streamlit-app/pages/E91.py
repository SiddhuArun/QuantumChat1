import streamlit as st
import sys
import time

sys.path.append('C:\\Users\\avina\\PycharmProjects\\QC-API-v1')
from qkd.generate_e91_key import e91_qkd_protocol_v2

def page_e91_shared_key():
    st.title("🔑 E91 Protocol - Generate Shared Key")
    st.markdown(
        "#### Please enter the desired key length and click the button to generate a secure shared key using the E91 quantum key distribution protocol."
    )

    with st.container(border=True):
        st.markdown("### Key Generation Input")
        desired_key_length = st.number_input('Enter desired key length:', min_value=1, max_value=1000, value=10)

    if st.button('Generate Shared Key', key='generate_e91_shared_key', use_container_width=True):
        start_time = time.time()

        alice_key, bob_key, qber = e91_qkd_protocol_v2(desired_key_length)

        end_time = time.time()
        time_taken = end_time - start_time

        # Store the results in session state
        st.session_state['e91_alice_key'] = alice_key
        st.session_state['e91_bob_key'] = bob_key
        st.session_state['e91_qber'] = qber
        st.session_state['e91_time_taken'] = time_taken

    # Retrieve the results from session state
    if 'e91_alice_key' in st.session_state:
        alice_key = st.session_state['e91_alice_key']
        bob_key = st.session_state['e91_bob_key']
        qber = st.session_state['e91_qber']
        time_taken = st.session_state['e91_time_taken']

        with st.container(border=True):
            st.markdown("### Generated Keys")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.subheader('Alice Key')
                    st.markdown(f"## {alice_key}")
            with col2:
                with st.container(border=True):
                    st.subheader('Bob Key')
                    st.markdown(f"## {bob_key}")

            with col1:
                with st.container(border=True):
                    st.markdown(f"#### Time taken to generate the key: {time_taken:.2f} seconds")
            with col2:
                with st.container(border=True, height=100):
                    st.markdown(f"#### QBER: {qber:.4f}")
            with st.container(border=True):
                # Calculate and display key match rate
                key_match_rate = sum(a == b for a, b in zip(alice_key, bob_key)) / len(alice_key)
                st.markdown(f"#### Key Match Rate: {key_match_rate:.4f}")
                st.session_state['e91_key_match_rate'] = key_match_rate

page_e91_shared_key()

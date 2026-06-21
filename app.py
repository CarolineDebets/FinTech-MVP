import streamlit as st


st.set_page_config(
    page_title="SmartRetireNL",
    page_icon="SR",
    layout="centered",
)

st.title("Retire Smart with Technology")

st.write(
    "SmartRetireNL helps people explore retirement decisions with Monte Carlo "
    "simulation, Dutch tax-aware planning, and AI explanations in plain language."
)

if st.button("Start analyse", type="primary"):
    st.info("The analysis flow will be added in a future MVP step.")

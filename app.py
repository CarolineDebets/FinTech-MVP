import streamlit as st
from src.profiler import render_user_input_form, get_saved_profile

st.set_page_config(
    page_title="SmartRetireNL",
    page_icon="SR",
    layout="centered",
)

if "page" not in st.session_state:
    st.session_state["page"] = "landing"

page = st.session_state["page"]

if page == "landing":
    st.title("Retire Smart with Technology")

    st.write(
        "SmartRetireNL helps people explore retirement decisions with Monte Carlo "
        "simulation, Dutch tax-aware planning, and AI explanations in plain language."
    )

    if st.button("Start analyse", type="primary"):
        st.session_state["page"] = "profiler"
        st.rerun()

elif page == "profiler":
    profile = render_user_input_form()

    if profile:
        st.info("Profiel opgeslagen. U kunt nu doorgaan naar de resultaten.")
        if st.button("Ga naar resultaten"):
            st.session_state["page"] = "results"
            st.rerun()

elif page == "results":
    st.title("Resultaten Dashboard")
    saved = get_saved_profile()

    if saved:
        st.success("Profiel succesvol geladen.")
        st.json(saved.to_dict())
        st.write("Hier kun je later simulation.py, tax_engine.py en scenario_compare.py aan koppelen.")
    else:
        st.warning("Geen profiel gevonden. Ga eerst terug en vul het formulier in.")
        if st.button("Terug naar start"):
            st.session_state["page"] = "landing"
            st.rerun()


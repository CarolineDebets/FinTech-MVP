import streamlit as st
import plotly.express as px

from src.simulation import build_demo_projection

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

if st.button("Start analyse", type="primary"):
    st.info("The analysis flow will be added in a future MVP step.")

st.divider()

st.header("Results Dashboard")
st.caption("Demo results using mock data until the profiler feature is connected.")

projection = build_demo_projection()

median_col, chance_col, gap_col, risk_col = st.columns(4)
median_col.metric(
    "Expected median retirement pot",
    f"EUR {projection['median_pot']:,.0f}",
)
chance_col.metric(
    "Chance of achieving target",
    f"{projection['chance_of_target']:.0%}",
)
gap_col.metric(
    "Projected pension gap",
    f"EUR {projection['pension_gap']:,.0f}",
)
risk_col.metric("Risk label", projection["risk_label"])

fig = px.histogram(
    projection["outcomes"],
    nbins=35,
    labels={"value": "Projected retirement pot", "count": "Simulation runs"},
    title="Monte Carlo Simulation Outcomes",
)
fig.add_vline(
    x=projection["target_pot"],
    line_dash="dash",
    line_color="red",
    annotation_text="Target",
)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

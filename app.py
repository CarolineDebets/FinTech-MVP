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


def render_landing_page() -> None:
    st.title("Slim met technologie met pensioen")

    st.write(
        "SmartRetireNL helpt u pensioenkeuzes te verkennen met Monte Carlo-simulatie, "
        "Nederlandse belastingbewuste planning en AI-uitleg in begrijpelijke taal."
    )

    if st.button("Start analyse", type="primary", key="landing_start_analysis"):
        st.session_state["page"] = "profiler"
        st.rerun()


def render_profile_summary() -> None:
    profile = get_saved_profile()
    if not profile:
        st.warning("Geen profiel gevonden. Ga terug en vul het formulier in.")
        return

    st.success("Basisscenario berekend en profiel opgeslagen.")
    st.subheader("Samenvatting van uw gegevens")

    left, right = st.columns(2)

    with left:
        st.write(f"Leeftijd: {profile.leeftijd}")
        st.write(f"Gewenste pensioenleeftijd: {profile.gewenste_pensioenleeftijd}")
        st.write(f"Huishoudtype: {profile.huishoudtype}")
        st.write(f"Partner aanwezig: {'Ja' if profile.partner_aanwezig else 'Nee'}")
        st.write(f"Aantal kinderen: {profile.aantal_kinderen}")
        st.write(f"Werkstatus: {profile.werkstatus}")

    with right:
        st.write(f"Huidig vermogen: EUR {profile.huidig_vermogen:,.2f}")
        st.write(f"Huidige pensioenopbouw: EUR {profile.huidige_pensioenopbouw:,.2f}")
        st.write(f"Maandelijkse extra inleg: EUR {profile.maandelijkse_extra_inleg:,.2f}")
        st.write(f"Gewenst pensioeninkomen: EUR {profile.gewenst_pensioeninkomen:,.2f}")
        st.write(f"Risicoprofiel: {profile.risicoprofiel}")


def render_results_dashboard() -> None:
    st.header("Resultaten Dashboard")
    st.caption("Demoresultaten met mockdata totdat de profiler volledig is gekoppeld.")

    projection = build_demo_projection()

    median_col, chance_col, gap_col, risk_col = st.columns(4)
    median_col.metric(
        "Verwachte mediane pensioenpot",
        f"EUR {projection['median_pot']:,.0f}",
    )
    chance_col.metric(
        "Kans om het doel te halen",
        f"{projection['chance_of_target']:.0%}",
    )
    gap_col.metric(
        "Verwacht pensioengat",
        f"EUR {projection['pension_gap']:,.0f}",
    )
    risk_col.metric("Risicolabel", projection["risk_label"])

    fig = px.histogram(
        projection["outcomes"],
        nbins=35,
        labels={"value": "Verwachte pensioenpot", "count": "Simulatieruns"},
        title="Uitkomsten Monte Carlo-simulatie",
    )
    fig.add_vline(
        x=projection["target_pot"],
        line_dash="dash",
        line_color="red",
        annotation_text="Doel",
    )
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


def render_tax_pension_insights() -> None:
    st.header("Nederlandse belasting- en pensioeninzichten")
    st.caption("Demo-inzichten op basis van transparante regels.")

    profile = get_saved_profile()
    if not profile:
        st.info("Vul eerst het gebruikersprofiel in om inzichten te tonen.")
        return

    st.write("- AOW-leeftijd en aanvullend pensioen worden later gekoppeld aan de echte rekenregels.")
    st.write("- Extra maandelijkse inleg kan helpen om het verwachte pensioengat te verkleinen.")
    st.write("- Fiscale behandeling is afhankelijk van persoonlijke situatie en actuele wetgeving.")

    with st.expander("Gebruikte demo-regels"):
        st.write("- Regel 1: toon inzichten pas nadat het basisscenario is berekend.")
        st.write("- Regel 2: gebruik het opgeslagen profiel als bron voor toekomstige berekeningen.")
        st.write("- Regel 3: geef nog geen persoonlijk belastingadvies in deze MVP-stap.")


def render_profiler_page() -> None:
    profile = render_user_input_form(show_summary=False)

    if profile:
        st.session_state["page"] = "results"
        st.rerun()


def render_results_page() -> None:
    if not get_saved_profile():
        st.warning("Geen profiel gevonden. Ga terug en vul het formulier in.")
        if st.button("Terug", key="results_back_without_profile"):
            st.session_state["page"] = "profiler"
            st.rerun()
        return

    render_profile_summary()
    st.divider()
    render_results_dashboard()

    back_col, next_col = st.columns(2)
    with back_col:
        if st.button("Terug", key="results_back"):
            st.session_state["page"] = "profiler"
            st.rerun()
    with next_col:
        if st.button("Bekijk belasting- en pensioeninzichten", type="primary"):
            st.session_state["page"] = "insights"
            st.rerun()


def render_insights_page() -> None:
    if not get_saved_profile():
        st.warning("Geen profiel gevonden. Ga terug en vul het formulier in.")
        if st.button("Terug", key="insights_back_without_profile"):
            st.session_state["page"] = "profiler"
            st.rerun()
        return

    render_tax_pension_insights()

    if st.button("Terug naar resultaten"):
        st.session_state["page"] = "results"
        st.rerun()


if page == "landing":
    render_landing_page()
elif page == "profiler":
    render_profiler_page()
elif page == "results":
    render_results_page()
elif page == "insights":
    render_insights_page()
else:
    st.session_state["page"] = "landing"
    st.rerun()

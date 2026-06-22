# profiler.py

"""
Streamlit user-input form for SmartRetireNL (Dutch).
- Renders Persoonlijk / Werk / Vermogen / Doel sections
- Validates inputs
- Builds a UserProfile dataclass
- Saves profile to st.session_state for other modules
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, Tuple, List
import datetime
import streamlit as st


@dataclass
class UserProfile:
    """Dataclass to store the user profile from the form."""
    leeftijd: int
    gewenste_pensioenleeftijd: int
    huishoudtype: str
    partner_aanwezig: bool
    aantal_kinderen: int
    werkstatus: str
    huidig_vermogen: float
    huidige_pensioenopbouw: float
    maandelijkse_extra_inleg: float
    gewenst_pensioeninkomen: float
    risicoprofiel: str
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict representation of the profile."""
        return asdict(self)


def validate_profile(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the raw input values.
    Returns (is_valid, errors).
    """
    errors: List[str] = []

    leeftijd = data.get("leeftijd")
    if leeftijd is None:
        errors.append("Leeftijd is verplicht.")
    else:
        try:
            leeftijd = int(leeftijd)
            if not (18 <= leeftijd <= 100):
                errors.append("Leeftijd moet tussen 18 en 100 liggen.")
        except Exception:
            errors.append("Leeftijd moet een geldig geheel getal zijn.")

    pensioenleeftijd = data.get("gewenste_pensioenleeftijd")
    if pensioenleeftijd is None:
        errors.append("Gewenste pensioenleeftijd is verplicht.")
    else:
        try:
            pensioenleeftijd = int(pensioenleeftijd)
            if isinstance(leeftijd, int) and pensioenleeftijd <= leeftijd:
                errors.append("Gewenste pensioenleeftijd moet groter zijn dan huidige leeftijd.")
            if pensioenleeftijd > 80:
                errors.append("Pensioenleeftijd moet realistisch zijn (maximaal 80).")
        except Exception:
            errors.append("Gewenste pensioenleeftijd moet een geldig geheel getal zijn.")

    if not data.get("huishoudtype"):
        errors.append("Huishoudtype is verplicht.")

    if "partner_aanwezig" not in data:
        errors.append("Partnerstatus is verplicht.")

    aantal_kinderen = data.get("aantal_kinderen")
    if aantal_kinderen is None:
        errors.append("Aantal kinderen is verplicht.")
    else:
        try:
            aantal_kinderen = int(aantal_kinderen)
            if aantal_kinderen < 0:
                errors.append("Aantal kinderen mag niet negatief zijn.")
        except Exception:
            errors.append("Aantal kinderen moet een geldig geheel getal zijn.")

    if not data.get("werkstatus"):
        errors.append("Werkstatus is verplicht.")

    if not data.get("risicoprofiel"):
        errors.append("Risicoprofiel is verplicht.")

    money_fields = [
        ("huidig_vermogen", "Huidig vermogen"),
        ("huidige_pensioenopbouw", "Huidige pensioenopbouw"),
        ("maandelijkse_extra_inleg", "Maandelijkse extra inleg"),
        ("gewenst_pensioeninkomen", "Gewenst pensioeninkomen"),
    ]

    for key, label in money_fields:
        value = data.get(key)
        if value is None:
            errors.append(f"{label} is verplicht.")
        else:
            try:
                value = float(value)
                if value < 0:
                    errors.append(f"{label} mag niet negatief zijn.")
            except Exception:
                errors.append(f"{label} moet een geldig getal zijn.")

    is_valid = len(errors) == 0
    return is_valid, errors


def build_user_profile(data: Dict[str, Any]) -> UserProfile:
    """
    Convert validated input dict into UserProfile dataclass.
    """
    return UserProfile(
        leeftijd=int(data["leeftijd"]),
        gewenste_pensioenleeftijd=int(data["gewenste_pensioenleeftijd"]),
        huishoudtype=str(data["huishoudtype"]),
        partner_aanwezig=bool(data["partner_aanwezig"]),
        aantal_kinderen=int(data["aantal_kinderen"]),
        werkstatus=str(data["werkstatus"]),
        huidig_vermogen=float(data["huidig_vermogen"]),
        huidige_pensioenopbouw=float(data["huidige_pensioenopbouw"]),
        maandelijkse_extra_inleg=float(data["maandelijkse_extra_inleg"]),
        gewenst_pensioeninkomen=float(data["gewenst_pensioeninkomen"]),
        risicoprofiel=str(data["risicoprofiel"]),
    )


def get_saved_profile() -> Optional[UserProfile]:
    """Return the saved UserProfile from session_state if present."""
    return st.session_state.get("user_profile")


def render_user_input_form(key_prefix: str = "main") -> Optional[UserProfile]:
    """
    Render the Streamlit user input form.
    On successful submit:
    - saves profile to st.session_state
    - shows a confirmation summary
    - returns the UserProfile
    """
    form_key = f"user_input_form_{key_prefix}"

    with st.form(form_key):
        st.title("Gebruikersprofiel")
        st.write("Vul hieronder uw gegevens in voor de pensioenanalyse.")

        st.subheader("Persoonlijk")
        col1, col2 = st.columns(2)

        with col1:
            leeftijd = st.number_input(
                "Leeftijd",
                min_value=18,
                max_value=100,
                value=40,
                step=1
            )

        with col2:
            gewenste_pensioenleeftijd = st.number_input(
                "Gewenste pensioenleeftijd",
                min_value=19,
                max_value=80,
                value=67,
                step=1
            )

        huishoudtype = st.selectbox(
            "Huishoudtype",
            options=[
                "Alleenstaand",
                "Samenwonend",
                "Gehuwd",
                "Alleenstaande ouder"
            ],
            index=1
        )

        col3, col4 = st.columns(2)

        with col3:
            partner_aanwezig = st.selectbox(
                "Partner aanwezig",
                options=["Ja", "Nee"],
                index=0
            )

        with col4:
            aantal_kinderen = st.number_input(
                "Aantal kinderen",
                min_value=0,
                max_value=10,
                value=2,
                step=1
            )

        st.subheader("Werk")
        werkstatus = st.radio(
            "Werkstatus",
            options=["Werknemer", "ZZP", "Mixed"],
            index=0
        )

        st.subheader("Vermogen")
        c1, c2 = st.columns(2)

        with c1:
            huidig_vermogen = st.number_input(
                "Huidig vermogen (€)",
                min_value=0.0,
                value=20000.0,
                step=500.0,
                format="%.2f"
            )

        with c2:
            huidige_pensioenopbouw = st.number_input(
                "Huidige pensioenopbouw (€)",
                min_value=0.0,
                value=50000.0,
                step=1000.0,
                format="%.2f"
            )

        maandelijkse_extra_inleg = st.number_input(
            "Maandelijkse extra inleg (€)",
            min_value=0.0,
            value=200.0,
            step=10.0,
            format="%.2f"
        )

        st.subheader("Doel")
        d1, d2 = st.columns(2)

        with d1:
            gewenst_pensioeninkomen = st.number_input(
                "Gewenst pensioeninkomen per maand (€)",
                min_value=0.0,
                value=2000.0,
                step=50.0,
                format="%.2f"
            )

        with d2:
            risicoprofiel = st.selectbox(
                "Risicoprofiel",
                options=["Conservatief", "Neutraal", "Risicovol"],
                index=1
            )

        submitted = st.form_submit_button("Bereken basisscenario")

    if submitted:
        raw = {
            "leeftijd": leeftijd,
            "gewenste_pensioenleeftijd": gewenste_pensioenleeftijd,
            "huishoudtype": huishoudtype,
            "partner_aanwezig": partner_aanwezig == "Ja",
            "aantal_kinderen": aantal_kinderen,
            "werkstatus": werkstatus,
            "huidig_vermogen": huidig_vermogen,
            "huidige_pensioenopbouw": huidige_pensioenopbouw,
            "maandelijkse_extra_inleg": maandelijkse_extra_inleg,
            "gewenst_pensioeninkomen": gewenst_pensioeninkomen,
            "risicoprofiel": risicoprofiel,
        }

        is_valid, errors = validate_profile(raw)

        if not is_valid:
            st.error("Er zijn fouten gevonden in het formulier:")
            for error in errors:
                st.error(f"• {error}")
            return None

        profile = build_user_profile(raw)

        st.session_state["user_profile"] = profile
        st.session_state["user_profile_dict"] = profile.to_dict()

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
            st.write(f"Huidig vermogen: €{profile.huidig_vermogen:,.2f}")
            st.write(f"Huidige pensioenopbouw: €{profile.huidige_pensioenopbouw:,.2f}")
            st.write(f"Maandelijkse extra inleg: €{profile.maandelijkse_extra_inleg:,.2f}")
            st.write(f"Gewenst pensioeninkomen: €{profile.gewenst_pensioeninkomen:,.2f}")
            st.write(f"Risicoprofiel: {profile.risicoprofiel}")

        return profile

    return None


if __name__ == "__main__":
    st.set_page_config(page_title="SmartRetireNL - Profiler", layout="centered")
    render_user_input_form()



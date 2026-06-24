# SmartRetireNL MVP

SmartRetireNL is a Streamlit MVP for exploring retirement planning concepts for Dutch households. The app demonstrates a simple flow from a Dutch landing page to a user profile form, demo retirement outcome results, and transparent Dutch tax and pension insights.

## Problem And Solution

Retirement planning can be difficult to understand because users often need to combine personal savings, pension expectations, uncertainty, and tax-aware decisions. SmartRetireNL addresses this by turning a basic user profile into a clear demo journey with plain-language outputs and visual retirement outcome signals.

This MVP is intentionally limited: it shows the product flow and demo calculations, but it does not yet provide real financial advice or a production-grade pension/tax engine.

## Current App Features

- Dutch landing page with a short explanation of the SmartRetireNL concept.
- User profile form for personal, work, wealth, retirement goal, and risk profile inputs.
- Step-based Streamlit flow using session state.
- Results page with a saved profile summary.
- Results dashboard with demo KPI cards:
  - expected median retirement pot
  - chance of achieving the target
  - projected pension gap
  - risk label
- Plotly histogram of mock Monte Carlo retirement outcomes.
- Separate Dutch Tax & Pension Insights page with transparent demo rules.

## Current User Flow

1. The user starts on the Dutch landing page.
2. The user clicks `Start analyse`.
3. The user completes the profile form and clicks `Bereken basisscenario`.
4. The app navigates to the results page with the profile summary and demo dashboard.
5. The user can continue to the separate tax and pension insights page.
6. The user can navigate back to the previous step with simple buttons.

## Tech Stack

- Python
- Streamlit
- NumPy
- Pandas
- Plotly
- Pytest

## Project Structure

```text
.
├── app.py                  # Main Streamlit app and page flow
├── requirements.txt        # Python dependencies
├── README.md               # Project overview and setup
├── CODEX.md                # AI agent usage and collaboration notes
├── AGENTS.md               # Agent instructions used in the project
└── src/
    ├── profiler.py         # User profile form and validation
    ├── simulation.py       # Demo projection helper for dashboard output
    ├── tax_engine.py       # Placeholder for future tax logic
    ├── scenario_compare.py # Placeholder for future scenario comparison
    └── action_plan.py      # Placeholder for future action plan logic
```

## Installation

Create and activate a virtual environment if desired, then install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run The App

```bash
python3 -m streamlit run app.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## MVP Scope And Limitations

- Dashboard results currently use mock/demo Monte Carlo data from `src/simulation.py`.
- The profile form is saved in Streamlit session state and is not persisted to a database.
- Dutch tax and pension insights are transparent demo rules, not a full tax engine.
- Scenario comparison, AI action plans, and production financial advice are not implemented.
- The app is intended for assignment demonstration and prototype validation only.

## AI Agent Usage

Codex was used as the coding assistant for incremental implementation, refactoring, and documentation cleanup. Prompts were scoped by feature so the repository history could show step-by-step collaboration. Generated code and documentation were reviewed manually before being accepted into the project.

## Team And Collaboration

This project was developed collaboratively for a fintech assignment by Caroline Debets and Pascale Breugem. The repository was built in small commits to make the contribution history and AI-assisted development process transparent.

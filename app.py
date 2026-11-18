"""Entry point for the Retail Sales Intelligence Dashboard."""

import streamlit as st


def main() -> None:
    """Render the initial application shell."""
    st.set_page_config(
        page_title="Retail Sales Intelligence Dashboard",
        page_icon="📊",
        layout="wide",
    )
    st.title("Retail Sales Intelligence Dashboard")
    st.caption("A local workspace for exploring retail sales data.")
    st.info(
        "Project foundation is ready. Data upload, cleaning, analytics, and "
        "visualizations will be added in the next development phase."
    )


if __name__ == "__main__":
    main()

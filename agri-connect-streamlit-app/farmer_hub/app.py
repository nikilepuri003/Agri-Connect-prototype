import streamlit as st

try:
	from .ui import run
except ImportError:
	from farmer_hub.ui import run


def main() -> None:
	st.set_page_config(
		page_title="AgriConnect",
		page_icon="🌾",
		layout="wide",
		initial_sidebar_state="expanded",
	)
	run()

if __name__ == "__main__":
	main()
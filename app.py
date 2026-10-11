import streamlit as st
from graph import build_graph

st.set_page_config(page_title="🎬 Movie Recommender", layout="centered")

st.title("🎬 سیستم پیشنهاد فیلم")
st.write("IMDb پیشنهاد فیلم بر اساس درخواست")

user_input = st.text_input(
    "چی دوست داری ببینی؟",
    placeholder="مثلاً: یه فیلم علمی تخیلی خفن"
)

if "app" not in st.session_state:
    st.session_state.app = build_graph()

if st.button("پیشنهاد بده") and user_input:
    with st.spinner("...در حال بررسی دیتابیس فیلم‌ها"):
        result = st.session_state.app.invoke(
            {
                "user_message": user_input
            }
        )

    st.success("پیشنهادها آماده است")
    st.write(result["response"])
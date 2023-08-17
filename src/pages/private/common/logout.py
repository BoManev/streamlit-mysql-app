import streamlit as st

st.title("👋 Logout")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
)
st.markdown("Click to logout. Have a nice day!")

def logout_on_click():
    import time
    from src.lib.sql_wrapper import ROLES
    st.session_state["auth"] = ROLES.PUBLIC
    st.balloons()
    time.sleep(2)
    query_dict = {}
    st.experimental_set_query_params(**query_dict)

st.button("Logout", on_click=logout_on_click)
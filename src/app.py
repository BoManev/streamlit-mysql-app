import streamlit as st
import streamlit_book as stb

st.set_page_config(layout="wide")

def main():
    from src.lib.sql_wrapper import check_connection, ROLES
    
    if not check_connection():
        st.warning('No Database Connection!')

    if 'auth' in st.session_state:
        if st.session_state["auth"] == ROLES.OWNER:
            display_owner()
        elif st.session_state["auth"] == ROLES.PILOT:
            display_pilot()
        elif st.session_state["auth"] == ROLES.SERVICE:
            display_service()
        elif st.session_state["auth"] == ROLES.WORKER:
            display_worker()
        else:
            display_public()
    else:
        display_public() 

def display_public():
    stb.set_book_config(
        menu_title="Public View",
        menu_icon="people",
        options=[
            "Home",   
            "Login",
            "Old"
            ], 
        paths=[
            "src/pages/public/home.py",  
            "src/pages/public/login.py",
            "src/pages/public/old.py",
            ],
        save_answers=False,
        styles={
            "nav-link": {"--hover-color": "#e9f6fb"},
            "nav-link-selected": {"background-color": "#87CEEB"},
        }
        )

def display_owner():
    stb.set_book_config(
    menu_title="Owner View",
    menu_icon="shield",
    options=[
        "Home",   
        "Logout", 
        ], 
    paths=[
        "src/pages/private/owner/home.py",  
        "src/pages/private/common/logout.py", 
        ],
    save_answers=False,
    styles={
        "nav-link": {"--hover-color": "#e9f6fb"},
        "nav-link-selected": {"background-color": "#87CEEB"},
    }
    )

def display_pilot():
    stb.set_book_config(
    menu_title="Pilot View",
    menu_icon="shield",
    options=[
        "Home",   
        "Logout", 
        ], 
    paths=[
        "src/pages/private/pilot/home.py",  
        "src/pages/private/common/logout.py", 
        ],
    save_answers=False,
    styles={
        "nav-link": {"--hover-color": "#e9f6fb"},
        "nav-link-selected": {"background-color": "#87CEEB"},
    }
    )

def display_service():
    stb.set_book_config(
    menu_title="Service View",
    menu_icon="shield",
    options=[
        "Home",   
        "Logout", 
        ], 
    paths=[
        "src/pages/private/service/home.py",  
        "src/pages/private/common/logout.py", 
        ],
    save_answers=False,
    styles={
        "nav-link": {"--hover-color": "#e9f6fb"},
        "nav-link-selected": {"background-color": "#87CEEB"},
    }
    )

def display_worker():
    stb.set_book_config(
    menu_title="Worker View",
    menu_icon="shield",
    options=[
        "Home",   
        "Logout", 
        ], 
    paths=[
        "src/pages/private/worker/home.py",  
        "src/pages/private/common/logout.py", 
        ],
    save_answers=False,
    styles={
        "nav-link": {"--hover-color": "#e9f6fb"},
        "nav-link-selected": {"background-color": "#87CEEB"},
    }
    )

if __name__ == '__main__':
    main()
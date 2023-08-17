from datetime import date
import streamlit as st
import streamlit_book as stb

def on_click():
    from src.lib.sql_wrapper import run_query_one, ROLES
    import time
    global role, username, bday
    
    # THIS CODE IS UNSAFE! 
    # the following sql queries are susceptible to sql injections; example bday= ' or '1'='1
    # using count(*) mitigates the issue, but other types of attacks are still possible
    # birthdate is used as password, totally unsecure... 
    isEmployee = run_query_one(f'SELECT COUNT(*) FROM users WHERE username=\'{username}\' AND birthdate=\'{bday}\'')
    if (isEmployee[0]):
        if(isEmployee[1][0] > 0):
            if (role == 'Pilot'):
                res = run_query_one(f'SELECT COUNT(*) FROM pilots WHERE username=\'{username}\'')
                if (res[0] and res[1][0] > 0):
                    st.session_state['auth'] = ROLES.PILOT
                else:
                    st.warning('Invalid Pilo Role!')
                    return
            elif (role == 'Owner'): 
                res = run_query_one(f'SELECT COUNT(*) FROM restaurant_owners WHERE username=\'{username}\'')
                if (res[0] and res[1][0] > 0):
                    st.session_state['auth'] = ROLES.OWNER
                else:
                    st.warning('Invalid Owner!')
                    return
            elif (role == 'Manager'): 
                res = run_query_one(f'SELECT COUNT(*) FROM delivery_services WHERE manager=\'{username}\'');
                if (res[0] and res[1][0] > 0):
                    st.session_state['auth'] = ROLES.SERVICE
                else:
                    st.warning('Invalid Manager')
                    return
            elif (role == 'Worker'):
                res = run_query_one(f'SELECT COUNT(*) FROM workers WHERE username=\'{username}\'')
                if (res[0] and res[1][0] > 0):
                    st.session_state['auth'] = ROLES.WORKER
                else:
                    st.warning('Invalid Worker')
                    return
            else:
                st.session_state['auth'] = ROLES.PUBLIC
                st.warning('Invalid Role')
                return
            st.balloons()
            time.sleep(2)
            st.experimental_set_query_params(**{})  
        else:
            st.warning('Invalid Employee!')
            st.session_state['auth'] = ROLES.PUBLIC
            return
    else:
        st.error(isEmployee[1])
        st.session_state['auth'] = ROLES.PUBLIC
        return
        
        
_, c1, _ = st.columns(3)
c1.title('🔓 Employee Authentication')
_, c2, _ = st.columns(3)
_, c3, _ = st.columns(3)
_, c4, _ = st.columns(3)
role = c2.selectbox('Role', ['Pilot', 'Owner', 'Manager', 'Worker'], label_visibility="hidden")
username = c3.text_input("Username:", "")
bday = c4.date_input("Birthdate: ", date.today())
st.markdown("")
_, b1, _ = st.columns(3)
b1.button("Login", on_click=on_click)
    
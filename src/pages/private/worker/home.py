from datetime import date
import streamlit as st
from src.lib.sql_wrapper import addEmployee, addPilot, addWorker, fireEmployee, getEmployeeView, removePilotRole, run_query_all
import pandas as pd

st.title("👷 Worker Home Page")
st.markdown("""
    Welcome to the home page for delivery services. This will allow you to perform a few functionalities related to hiring workers, management, and adding/removing ingredients. Here
    is a list of all you can do:
    * [2]: **add_employee** - This stored procedure creates a new employee without any designated pilot or worker roles.
    * [3]: **add_pilot_role** - This stored procedure adds the pilot role to an existing employee.
    * [4]: **add_worker_role** - This stored procedure adds the worker role to an existing employee.
    * [12]: **fire_employee** - This stored procedure fires an employee who is currently working for a delivery service.
    * [23]: **remove_pilot_role** - This stored procedure removes a pilot from the system.
    * [25]: **display_employee_view** - This view displays information in the system from the perspective of an employee.
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
)

st.markdown("---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Employee")

add_employee_username = st.text_input(label="Enter a Username") # ip_username varchar(40)
col1, col2, col3 = st.columns(3)
with col1:
    add_employee_first_name = st.text_input(label="Enter First Name") # ip_first_name varchar(100)
    add_employee_birthdate = st.date_input(label="Enter Birthdate") # ip_birthdate date
    add_employee_experience = st.number_input(label="Enter Employee Experience", min_value=0, value=0) # ip_employee_experience integer
with col2:
    add_employee_last_name = st.text_input(label="Enter Last Name") # ip_last_name varchar(100)
    add_employee_taxID = st.text_input(label="Enter TaxID", value="i.e. 999-99-9999") # ip_taxID varchar(40) - must be unique
    add_employee_salary = st.number_input(label="Enter Salary", min_value=0, value=0, step=1000) # ip_salary integer
with col3:
    add_employee_address = st.text_input(label="Enter an Address") # ip_address varchar(500)
    add_employee_hired_date = st.date_input(label="Enter hired date") # ip_hired date

if st.button("Add Employee"):
    if (len(add_employee_username) == 0):
        st.error("Please enter a valid username.")
    elif (len(add_employee_first_name) == 0):
        st.error("Please enter a valid first name.")
    elif (len(add_employee_last_name) == 0):
        st.error("Please enter a valid last name.")
    elif (len(add_employee_address) == 0):
        st.error("Please enter a valid address.")
    elif (add_employee_taxID == "i.e. 999-99-9999" or len(add_employee_taxID) == 0):
        st.error("Please enter a valid taxID")
    else:
        res = addEmployee(add_employee_username, add_employee_first_name, add_employee_last_name, add_employee_address, add_employee_birthdate, 
        add_employee_taxID, add_employee_hired_date, add_employee_experience, add_employee_salary)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Employee Added 🙂")
        else:
            st.error(res[1])
    
st.markdown("---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Pilot Role")

get_add_pilot_role_usernames = run_query_all("SELECT distinct(username) FROM employees")
if (get_add_pilot_role_usernames[0]):
    add_pilot_role_username_list = ["Select a Username"]
    for username in get_add_pilot_role_usernames[1]:
        add_pilot_role_username_list.append(username[0])
    add_pilot_username = st.selectbox(label="Select a Username for Pilot Role", options=add_pilot_role_username_list) # ip_username varchar(40)
else:
    st.error(get_add_pilot_role_usernames[1])

add_pilot_license_id = st.text_input(label="Input LicenseID", value="i.e. 610623") # ip_licenseID varchar(40)
add_pilot_experience = st.number_input(label="Input Pilot Experience", min_value=0, value=0) # ip_pilot_experience integer

if st.button("Add Employee to Pilot Role"):
    if (add_pilot_username == add_pilot_role_username_list[0]):
        st.error("Please select a username!")
    elif (len(add_pilot_license_id) == 0):
        st.error("Please input a valid licenseID.")
    else:
        res = addPilot(add_pilot_username, add_pilot_license_id, add_pilot_experience)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Pilot Role Added 🙂")
        else:
            st.error(res[1])
    
st.markdown("---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Worker Role")

get_add_worker_role_usernames = run_query_all("SELECT distinct(username) FROM employees")
if (get_add_worker_role_usernames[0]):
    add_worker_role_username_list = ["Select a Username"]
    for username in get_add_worker_role_usernames[1]:
        add_worker_role_username_list.append(username[0])
    add_worker_username = st.selectbox(label="Select a Username for Worker Role", options=add_worker_role_username_list) # ip_username varchar(40)
else:
    st.error(get_add_worker_role_usernames[1])

if st.button("Add Employee to Worker Role"):
    if add_worker_username == add_worker_role_username_list[0]:
        st.error("Please select a username!")
    else:
        res = addWorker(add_worker_username)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Worker Role Added 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Fire Employee")

get_fire_employee_id = run_query_all("SELECT distinct(id) FROM work_for")
if (get_fire_employee_id[0]):
    fire_employee_id_list = ["Select a Delivery Service"]
    for employee in get_fire_employee_id[1]:
        fire_employee_id_list.append(employee[0])
    fire_employee_id = st.selectbox(label="Select a Delivery Service", options=fire_employee_id_list) # ip_id varchar(40))
else:
    st.error(get_fire_employee_id[1])

get_fire_employee_username = run_query_all(f"SELECT distinct(username) FROM work_for WHERE id=\'{fire_employee_id}\'")
if (get_fire_employee_username[0]):
    fire_employee_username_list = ["Select an Employee"]
    for employee in get_fire_employee_username[1]:
        fire_employee_username_list.append(employee[0])
    fire_employee_username = st.selectbox(label="Select an Employee", options=fire_employee_username_list) # ip_username varchar(40)
else:
    st.error(get_fire_employee_username[1])

if st.button("Fire Employee"):
    if (fire_employee_id == fire_employee_id_list[0]):
        st.error("Please select a valid delivery service.")
    elif (fire_employee_username == fire_employee_username_list[0]):
        st.error("Please select a valid employee.")
    else:
        res = fireEmployee(fire_employee_username, fire_employee_id)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Employee Fired 🙂")
        else:
            st.error(res[1])

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
st.header("Remove Pilot Role")

get_remove_pilot_role_pilots = run_query_all("SELECT username FROM pilots")
if (get_remove_pilot_role_pilots[0]):
    remove_pilot_role_list = ["Select a Pilot"]
    for pilot in get_remove_pilot_role_pilots[1]:
        remove_pilot_role_list.append(pilot[0])
    remove_pilot_role_pilot = st.selectbox(label="Select a Pilot to be Removed", options=remove_pilot_role_list) # ip_username varchar(40)
else:
    st.error(get_remove_pilot_role_pilots[1])

if st.button("Remove Pilot"):
    if (remove_pilot_role_pilot == remove_pilot_role_list[0]):
        st.error("Please select a pilot to be removed!")
    else:
        res = removePilotRole(remove_pilot_role_pilot)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Pilot Removed 🙂")
        else:
            st.error(res[1])
        

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Employee View")


display_employee_view = getEmployeeView()
if (display_employee_view[0]):
    df = pd.DataFrame(display_employee_view[1][0:], columns=['username', 'taxID', 'salary', 'hired', 'employee_experience', 'licenseID', 'piloting_experience', 'manager_status'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this employee currently.", icon="⚠")
else:
    st.error(display_employee_view[1])

import streamlit as st
from src.lib.sql_wrapper import addIngredient, addService, getServiceView, hireEmployee, manageService, removeIngredient, run_query_all
import pandas as pd

st.title("🚚 Delivery Service Home Page")
st.markdown("""
    **Welcome to the home page for delivery services. This will allow you to perform a few functionalities related to hiring workers, management, and adding/removing ingredients. Here
    is a list of all you can do:**
    * [5]: **add_ingredient** - This stored procedure creates a new ingredient.
    * [8]: **add_service** - This stored procedure creates a new delivery service.
    * [11]: **hire_employee** - This stored procedure hires an employee to work for a delivery service.
    * [13]: **manage_service** - This stored procedure appoints an employee who is currently hired by a delivery service as the new manager for that service.
    * [21]: **remove_ingredient** - This stored procedure removes an ingredient from the system.
    * [29]: **display_service_view** - This view displays information in the system from the perspective of a delivery service.
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
)

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Ingredient")

add_ingredient_barcode = st.text_input(label="Input a unique barcode", value="i.e. ap_9T25E36L") # ip_barcode varchar(40)
add_ingredient_iname = st.text_input(label="Add a New Ingredient") # ip_iname varchar(100)
add_ingredient_weight = st.number_input(label="Insert a weight", min_value=1, value=1)  # ip_weight integer

if st.button("Add New Ingredient"):
    add_ingredient_iname = add_ingredient_iname.lower()
    if (add_ingredient_barcode == "i.e. ap_9T25E36L"):
        st.error("Please enter a valid new barcode!")
    elif (len(add_ingredient_iname) == 0):
        st.error("Please enter a valid new ingredient!")
    else:
        res = addIngredient(add_ingredient_barcode, add_ingredient_iname, add_ingredient_weight)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Ingredient Added 🙂")
        else:
            st.error(res[1])

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Service")

col1, col2 = st.columns(2)
with col1:
    add_service_id = st.text_input(label="Enter a Unique Identifier (ex. rr, hf, osf)") # ip_id varchar(40)
with col2:
    add_service_long_name = st.text_input(label="Enter a Unique Long Name") # ip_long_name varchar(100)

get_add_service_locations = run_query_all("SELECT distinct(label) FROM locations")
if (get_add_service_locations[0]):
    add_service_location_list = ["Select a Location 🌎"]
    for label in get_add_service_locations[1]:
        add_service_location_list.append(label[0])
    add_service_home_base = st.selectbox("Select a Location to be Assigned", add_service_location_list, label_visibility="collapsed")
else:
    st.error(get_add_service_locations[1])

get_add_service_non_manager = run_query_all("SELECT username FROM workers WHERE username NOT IN (SELECT manager FROM delivery_services)") # ip_home_base varchar(40)
if (get_add_service_non_manager[0]):
    add_service_non_manager_list = ["Select a Username"]
    for username in get_add_service_non_manager[1]:
        add_service_non_manager_list.append(username[0])
    add_service_manager = st.selectbox("Select a Username to be Assigned", add_service_non_manager_list, label_visibility="collapsed") # ip_manager varchar(40)
else:
    st.error(get_add_service_non_manager[1])

if st.button("Add Service"):
    if (len(add_service_id) == 0):
        st.error("Please enter a unique identifier for the new service.")
    elif (len(add_service_long_name) == 0):
        st.error("Please enter a unique long name for the new service.")
    elif (add_service_home_base == add_service_location_list[0]):
        st.error("Please select a valid location for the new service.")
    elif (add_service_manager == add_service_non_manager_list[0]):
        st.error("Please select a valid manager to manage the new service.")
    else:
        res = addService(add_service_id, add_service_long_name, add_service_home_base, add_service_manager)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Service Added 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Hire Employee")

get_hire_employee_usernames = run_query_all("SELECT distinct(username) FROM employees")
if (get_hire_employee_usernames[0]):
    hire_employee_username_list = ["Select a Username"]
    for username in get_hire_employee_usernames[1]:
        hire_employee_username_list.append(username[0])
    hire_employee_username = st.selectbox(label="Select a Username to be Hired", options=hire_employee_username_list) # ip_username varchar(40)
else:
    st.error(get_hire_employee_usernames[1])

get_hire_employee_id =run_query_all("SELECT distinct(id) FROM delivery_services")
if (get_hire_employee_id[0]): 
    hire_employee_id_list = ["Select a Delivery Service ID"]
    for id in get_hire_employee_id[1]:
        hire_employee_id_list.append(id[0])
    hire_employee_id = st.selectbox(label="Select a Delivery Services", options=hire_employee_id_list) # ip_id varchar(40)
else:
    st.error(get_hire_employee_id[1])
    
if st.button("Hire Employee"):
    if (hire_employee_username == hire_employee_username_list[0]):
        st.error("Please select a username to be hired.")
    elif (hire_employee_id  == hire_employee_id_list[0]):
        st.error("Please enter a delivery service employer.")
    else:
        res = hireEmployee(hire_employee_username, hire_employee_id)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Employee Hired 🙂")
        else:
            st.error(res[1])

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Manage Service")

get_manage_service_id = run_query_all(f"SELECT distinct(id) FROM work_for")
if (get_manage_service_id[0]): 
    manage_service_id_list = ["Select a Delivery Service ID"]
    for sid in get_manage_service_id[1]:
        manage_service_id_list.append(sid[0])
    manage_service_id = st.selectbox(label="Enter a Delivery Service ID", options=manage_service_id_list) # ip_id varchar(40)
else:
    st.error(get_manage_service_id[1])

get_manage_service_username = run_query_all(f"SELECT username FROM work_for WHERE username NOT IN (SELECT manager FROM delivery_services) AND id=\'{manage_service_id}\'")
if (get_manage_service_username[0]):
    manage_service_username_list = ["Select a Username"]
    for username in get_manage_service_username[1]:
        manage_service_username_list.append(username[0])
    manage_service_username = st.selectbox("Select a Username to be Promoted", options=manage_service_username_list) # ip_username varchar(40)
else:
    st.error(get_manage_service_username[1])

if st.button("Promote Worker"):
    if (manage_service_id == manage_service_id_list[0]):
        st.error("Please select a delivery service ID.")
    elif (manage_service_username == manage_service_username_list[0]):
        st.error("Please select a worker to be promoted.")
    else:
        res = manageService(manage_service_username, manage_service_id)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Worker Promoted 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Remove Ingredient")

get_remove_ingredient_barcodes = run_query_all("SELECT distinct(barcode) FROM ingredients")
if (get_remove_ingredient_barcodes[0]):
    remove_ingredient_barcode_list = ["Select a Barcode"]
    for barcode in get_remove_ingredient_barcodes[1]:
        remove_ingredient_barcode_list.append(barcode[0])
    remove_ingredient_barcode = st.selectbox(label="Select an Ingredient to be Removed", options=remove_ingredient_barcode_list)
else:
    st.error(get_remove_ingredient_barcodes[1])

if st.button("Remove Existing Ingredient"):
    if (remove_ingredient_barcode == remove_ingredient_barcode_list[0]):
        st.error("Please select a barcode to remove.")
    else:
        res = removeIngredient(remove_ingredient_barcode)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Ingredient Removed 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Service View")

display_service_view = getServiceView()
if (display_service_view[0]):
    df = pd.DataFrame(display_service_view[1][0:], columns=['id', 'long_name', 'home_base', 'manager', 'revenue', 'ingredients_carried', 'cost_carried', 'weight_carried'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this delivery service currently.", icon="⚠")
else:
    st.error(display_service_view[1])

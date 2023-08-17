import random
import streamlit as st
import src.lib.sql_wrapper as sql
import pandas as pd

st.title("1 Delivery Services hire Employees to support their operations")
st.markdown("""
    [2] add_employee()\\
    [8] add_service()\\
    [11] hire_employee()\\
    [12] fire_employee()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[2] add_employee()")


class AddEmployee:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_username = st.text_input(label="add_employee username")
            self.ip_firstname = st.text_input(label="add_employee firstname")
            self.ip_lastname = st.text_input(label="add_employee lastname")
            self.ip_address = st.text_input(label="add_employee address")
            self.ip_birthdate = st.date_input(label="add_employee birthdate")

        with col2:
            self.ip_taxID = st.text_input(label="add_employee taxID")
            self.ip_hired = st.date_input(label="add_employee hired")
            self.ip_employee_experience = st.number_input(label="add_employee employee experience")
            self.ip_salary = st.number_input(label="add_employee salary")


add_employee = AddEmployee()

if st.button("Press to Add Employee"):
    sql.addEmployee(add_employee.ip_username, add_employee.ip_firstname, add_employee.ip_lastname, add_employee.ip_address, add_employee.ip_birthdate,
                add_employee.ip_taxID, add_employee.ip_hired, add_employee.ip_employee_experience, add_employee.ip_salary)
    st.write("Successfully Called Stored Procedure - Add Employee")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[8] add_service()")


class AddService:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="add_service id")
            self.ip_long_name = st.text_input(label="add_service long name")

        with col2:
            self.ip_home_base = st.text_input(label="add_service home base")
            self.ip_manager = st.text_input(label="add_service manager")

    def do_sql(self):
        sql.addService(self.ip_id, self.ip_long_name, self.ip_home_base, self.ip_manager)


add_service = AddService()

if st.button("Press to Add Service"):
    sql.addService(add_service.ip_id, add_service.ip_long_name, add_service.ip_home_base, add_service.ip_manager)
    st.write("Successfully Called Stored Procedure - Add Service")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[11] hire_employee()")


class HireEmployee:
    def __init__(self):
        self.ip_username = st.text_input(label="hire_employee username")
        self.ip_id = st.text_input(label="hire_employee id")

    def do_sql(self):
        sql.hireEmployee(self.ip_username, self.ip_id)


hire_employee = HireEmployee()

if st.button("Press to Hire Employee"):
    sql.hireEmployee(hire_employee.ip_username, hire_employee.ip_id)
    st.write("Successfully Called Stored Procedure - Hire Employee")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[12] fire_employee()")


class FireEmployee:
    def __init__(self):
        self.ip_username = st.text_input(label="fire_employee username")
        self.ip_id = st.text_input(label="fire_employee id")

    def do_sql(self):
        sql.fireEmployee(self.ip_username, self.ip_id)


fire_employee = FireEmployee()

if st.button("Press to Fire Employee"):
    sql.fireEmployee(fire_employee.ip_username, fire_employee.ip_id)
    st.write("Successfully Called Stored Procedure - Fire Employee")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("2 Employees support operations as (Warehouse) Workers, Pilots and/or Managers")
st.markdown("""
    [3] add_pilot_role()\\
    [4] add_worker_role()\\
    [23] remove_pilot_role()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[3] add_pilot_role()")


class AddPilotRole:
    def __init__(self):
        self.ip_username = st.text_input(label="add_pilot_role username")
        self.ip_licenceID = st.text_input(label="add_pilot_role licenceID")
        self.ip_pilot_experience = st.number_input(label="add_pilot_role pilot_experience")

    def do_sql(self):
        sql.addPilot(self.ip_username, self.ip_licenceID, self.ip_pilot_experience)


add_pilot_role = AddPilotRole()

if st.button("Press to Add Pilot Role"):
    sql.addPilot(add_pilot_role.ip_username, add_pilot_role.ip_licenceID, add_pilot_role.ip_pilot_experience)
    st.write("Successfully Called Stored Procedure - Add Pilot Role")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[4] add_worker_role()")


class AddWorkerRole:
    def __init__(self):
        self.ip_username = st.text_input(label="add_worker_role username")

    def do_sql(self):
        sql.addWorker(self.ip_username)


add_worker_role = AddWorkerRole()

if st.button("Press to Add Worker Role"):
    sql.addWorker(add_worker_role.ip_username)
    st.write("Successfully Called Stored Procedure - Add Worker Role")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[23] remove_pilot_role()")


class RemovePilotRole:
    def __init__(self):
        self.ip_username = st.text_input(label="remove_pilot_role username")

    def do_sql(self):
        sql.removePilotRole(self.ip_username)


remove_pilot_role = RemovePilotRole()

if st.button("Press to Remove Pilot Role"):
    sql.removePilotRole(remove_pilot_role.ip_username)
    st.write("Successfully Called Stored Procedure - Remove Pilot Role")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("3 Delivery Services purchase Drones to deliver Ingredients to Restaurants")
st.markdown("""
    [5] add_ingredient()\\
    [6] add_drone()\\
    [7] add_restaurant()\\
    [21] remove_ingredient()\\
    [22] remove_drone()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[5] add_ingredient()")


class AddIngredient:
    def __init__(self):
        self.ip_barcode = st.text_input(label="add_ingredient barcode")
        self.ip_iname = st.text_input(label="add_ingredient iname")
        self.ip_weight = st.number_input(label="add_ingredient weight")

    def do_sql(self):
        sql.addIngredient(self.ip_barcode, self.ip_iname, self.ip_weight)


add_ingredient = AddIngredient()

if st.button("Press to Add Ingredient"):
    sql.addIngredient(add_ingredient.ip_barcode, add_ingredient.ip_iname, add_ingredient.ip_weight)
    st.write("Successfully Called Stored Procedure - Add Ingredient")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[6] add_drone()")


class AddDrone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="add_ingredient id")
            self.ip_tag = st.number_input(label="add_ingredient tag")
            self.ip_fuel = st.number_input(label="add_ingredient fuel")
        with col2:
            self.ip_capacity = st.number_input(label="add_drone capacity")
            self.ip_sales = st.number_input(label="add_drone sales")
            self.ip_flown_by = st.text_input(label="add_drone flown_by")

    def do_sql(self):
        sql.addDrone(self.ip_id, self.ip_tag, self.ip_fuel, self.ip_capacity, self.ip_sales, self.ip_flown_by)


add_drone = AddDrone()

if st.button("Press to Add Drone"):
    sql.addDrone(add_drone.ip_id, add_drone.ip_tag, add_drone.ip_fuel, add_drone.ip_capacity, add_drone.ip_sales, add_drone.ip_flown_by)
    st.write("Successfully Called Stored Procedure - Add Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[7] add_restaurant()")


class AddRestaurant:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_long_name = st.text_input(label="add_restaurant long name")
            self.ip_rating = st.number_input(label="add_restaurant rating")
        with col2:
            self.ip_spent = st.number_input(label="add_restaurant spent")
            self.ip_location = st.text_input(label="add_restaurant location")

    def do_sql(self):
        sql.addRestaurant(self.ip_long_name, self.ip_rating, self.ip_spent, self.ip_location)


add_restaurant = AddRestaurant()

if st.button("Press to Add Restaurant"):
    sql.addRestaurant(add_restaurant.ip_long_name, add_restaurant.ip_rating, add_restaurant.ip_spent, add_restaurant.ip_location)
    st.write("Successfully Called Stored Procedure - Add Restaurant")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[21] remove_ingredient()")


class RemoveIngredient:
    def __init__(self):
        self.ip_barcode = st.text_input(label="remove_ingredient barcode")

    def do_sql(self):
        sql.removeIngredient(self.ip_barcode)


remove_ingredient = RemoveIngredient()

if st.button("Press to Remove Ingredient"):
    sql.removeIngredient(remove_ingredient.ip_barcode)
    st.write("Successfully Called Stored Procedure - Remove Ingredient")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[22] remove_drone()")


class RemoveDrone:
    def __init__(self):
        self.ip_id = st.text_input(label="remove_drone id")
        self.ip_tag = st.number_input(label="remove_drone tag")

    def do_sql(self):
        sql.removeDrone(self.ip_tag)


remove_drone = RemoveDrone()

if st.button("Press to Remove Drone"):
    sql.removeDrone(remove_drone.ip_id, remove_drone.ip_tag)
    st.write("Successfully Called Stored Procedure - Remove Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("4 Workers repair, restock and refuel the Drones to be able to deliver Ingredients")
st.markdown("""
    [17] load_drone()\\
    [18] refuel_drone()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[17] load_drone()")


class LoadDrone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="load_drone id")
            self.ip_tag = st.number_input(label="load_drone tag")
            self.ip_barcode = st.text_input(label="load_drone barcode")
        with col2:
            self.ip_more_packages = st.number_input(label="load_drone more packages")
            self.ip_price = st.number_input(label="load_drone price")

    def do_sql(self):
        sql.loadDrone(self.ip_id, self.ip_tag, self.ip_barcode, self.ip_more_packages, self.ip_price)


load_drone = LoadDrone()

if st.button("Press to Load Drone"):
    sql.loadDrone(load_drone.ip_id, load_drone.ip_tag, load_drone.ip_barcode, load_drone.ip_more_packages, load_drone.ip_price)
    st.write("Successfully Called Stored Procedure - Load Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[18] refuel_drone()")


class RefuelDrone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="refuel_drone id")
            self.ip_tag = st.number_input(label="refuel_drone tag")
        with col2:
            self.ip_more_fuel = st.number_input(label="refuel_drone more fuel")

    def do_sql(self):
        sql.refuel_drone(self.ip_id, self.ip_tag, self.ip_more_fuel)


refuel_drone = RefuelDrone()

if st.button("Press to Refuel Drone"):
    sql.refuel_drone(refuel_drone.ip_id, refuel_drone.ip_tag, refuel_drone.ip_more_fuel)
    st.write("Successfully Called Stored Procedure - Refuel Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("5 Pilots fly Drones – as “singles” or as swarms with many drones – to different Locations")
st.markdown("""
    [14] takeover_drone()\\
    [15] join_swarm()\\
    [16] leave_swarm()\\
    [19] fly_drone()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[14] takeover_drone()")


class TakeoverDrone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_username = st.text_input(label="takeover_drone barcode")
        with col2:
            self.ip_id = st.text_input(label="takeover_drone id")
            self.ip_tag = st.number_input(label="takeover_drone tag")

    def do_sql(self):
        sql.takeoverDrone(self.ip_username, self.ip_id, self.ip_tag)


takeover_drone = TakeoverDrone()

if st.button("Press to Takeover Drone"):
    sql.takeoverDrone(takeover_drone.ip_username, takeover_drone.ip_id, takeover_drone.ip_tag)
    st.write("Successfully Called Stored Procedure - Takeover Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[15] join_swarm()")


class JoinSwarm:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="join_swarm id")
            self.ip_tag = st.number_input(label="join_swarm tag")
        with col2:
            self.ip_swarm_leader_tag = st.number_input(label="join_swarm swarm leader tag")

    def do_sql(self):
        sql.joinSwarm(self.ip_id, self.ip_tag, self.ip_swarm_leader_tag)


join_swarm = JoinSwarm()

if st.button("Press to Join Swarm"):
    sql.joinSwarm(join_swarm.ip_id, join_swarm.ip_tag, join_swarm.ip_swarm_leader_tag)
    st.write("Successfully Called Stored Procedure - Join Swarm")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[16] leave_swarm()")


class LeaveSwarm:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="leave_swarm id")
        with col2:
            self.ip_swarm_tag = st.number_input(label="leave_swarm swarm tag")

    def do_sql(self):
        sql.leaveSwarm(self.ip_id, self.ip_swarm_tag)


leave_swarm = LeaveSwarm()

if st.button("Press to Leave Swarm"):
    sql.leaveSwarm(leave_swarm.ip_id, leave_swarm.ip_swarm_tag)
    st.write("Successfully Called Stored Procedure - Leave Swarm")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[19] fly_drone()")


class FlyDrone:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_id = st.text_input(label="fly_drone id")
            self.ip_tag = st.number_input(label="fly_drone tag")
        with col2:
            self.ip_destination = st.text_input(label="fly_drone destination")

    def do_sql(self):
        sql.flyDrone(self.ip_id, self.ip_tag, self.ip_destination)


fly_drone = FlyDrone()

if st.button("Press to Fly Drone"):
    sql.flyDrone(fly_drone.ip_id, fly_drone.ip_tag, fly_drone.ip_destination)
    st.write("Successfully Called Stored Procedure - Fly Drone")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("6 Owners provide funds for one or more Restaurants")
st.markdown("""
    [1] add_owner()\\
    [10] start_funding()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[1] add_owner()")


class AddOwner:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_username = st.text_input(label="add_owner username")
            self.ip_firstname = st.text_input(label="add_owner firstname")
            self.ip_lastname = st.text_input(label="add_owner lastname")
        with col2:
            self.ip_address = st.text_input(label="add_owner address")
            self.ip_birthdate = st.date_input(label="add_owner birthdate")

    def do_sql(self):
        sql.addOwner(self.ip_username, self.ip_firstname, self.ip_lastname, self.ip_address, self.ip_birthdate)


add_owner = AddOwner()

if st.button("Press to Add Owner"):
    sql.addOwner(add_owner.ip_username, add_owner.ip_firstname, add_owner.ip_lastname, add_owner.ip_address, add_owner.ip_birthdate)
    st.write("Successfully Called Stored Procedure - Add Owner")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[10] start_funding()")


class StartFunding:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_owner = st.text_input(label="start_funding owner")
        with col2:
            self.ip_long_name = st.text_input(label="start_funding long name")

    def do_sql(self):
        sql.startFunding(self.ip_owner, self.ip_long_name)


start_funding = StartFunding()

if st.button("Press to Start Funding"):
    sql.startFunding(start_funding.ip_owner, start_funding.ip_long_name)
    st.write("Successfully Called Stored Procedure - Start Funding")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("7 Managers direct Drones to Locations where Restaurants can purchase Ingredients")
st.markdown("""
    [9] add_location()\\
    [13] manage_service
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[9] add_location()")


class AddLocation:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_label = st.text_input(label="add_location label")
            self.ip_x_coord = st.number_input(label="add_location x_coord")
        with col2:
            self.ip_y_coord = st.number_input(label="add_location y_coord")
            self.ip_space = st.number_input(label="add_location space")

    def do_sql(self):
        sql.addLocation(self.ip_label, self.ip_x_coord, self.ip_y_coord, self.ip_space)


add_location = AddLocation()

if st.button("Press to Add Location"):
    sql.addLocation(add_location.ip_label, add_location.ip_x_coord, add_location.ip_y_coord, add_location.ip_space)
    st.write("Successfully Called Stored Procedure - Add Location")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[13] manage_service")


class ManageService:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_username = st.text_input(label="manage_service username")
        with col2:
            self.ip_id = st.text_input(label="manage_service id")

    def do_sql(self):
        sql.manageService(self.ip_username, self.ip_id)


manage_service = ManageService()

if st.button("Press to Manage Service"):
    sql.manageService(manage_service.ip_username, manage_service.ip_id)
    st.write("Successfully Called Stored Procedure - Manage Service")


st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("8 Restaurants purchase Ingredients from Drones at their Location")
st.markdown("""
    [20] purchase_ingredient()
""")
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1AA260;
    color: #FFFFFF;
}
</style>""", unsafe_allow_html=True
                )

st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[20] purchase_ingredient()")


class PurchaseIngredient:
    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.ip_long_name = st.text_input(label="purchase_ingredient long name")
            self.ip_id = st.text_input(label="purchase_ingredient id")
            self.ip_tag = st.number_input(label="purchase_ingredient tag")
        with col2:
            self.ip_barcode = st.text_input(label="purchase_ingredient barcode")
            self.ip_quantity = st.number_input(label="purchase_ingredient quantity")

    def do_sql(self):
        sql.purchaseIngredient(self.ip_long_name, self.ip_id, self.ip_tag, self.ip_barcode, self.ip_quantity)


purchase_ingredient = PurchaseIngredient()

if st.button("Press to Purchase Ingredient"):
    sql.purchaseIngredient(purchase_ingredient.ip_long_name, purchase_ingredient.ip_id, purchase_ingredient.ip_tag, purchase_ingredient.ip_barcode, purchase_ingredient.ip_quantity)
    st.write("Successfully Called Stored Procedure - Purchase Ingredient")










st.markdown(
    "---")  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.title("Expected Results for the “Global Views” based on the Initial Database State")
st.markdown("""
    [24] display_owner_view()\\
    [25] display_employee_view()\\
    [26] display_pilot_view()\\
    [27] display_location_view()\\
    [28] display_ingredient_view()\\
    [29] display_service_view()
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
st.header("[24] display_owner_view()")
display_owner_view = sql.getOwnerView()
if (display_owner_view[0]):
    df = pd.DataFrame(display_owner_view[1][0:], columns=['username', 'first_name', 'last_name', 'address', 'num_restaurants', 'num_places', 'highs', 'lows', 'debt'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this owner currently.", icon="⚠")


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[25] display_employee_view()")


display_employee_view = sql.getEmployeeView()
if (display_employee_view[0]):
    df = pd.DataFrame(display_employee_view[1][0:], columns=['username', 'taxID', 'salary', 'hired', 'employee_experience', 'licenseID', 'piloting_experience', 'manager_status'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this employee currently.", icon="⚠")


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[26] display_pilot_view()")


display_pilot_view = sql.getPilotView()
if (display_pilot_view[0]):
    df = pd.DataFrame(display_pilot_view[1][0:], columns=['username', 'licenseID', 'experience', 'num_drones', 'num_locations'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for pilots currently.", icon="⚠")


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[27] display_location_view()")


display_location_view = sql.getLocationView()
if (display_location_view[0]):
    df = pd.DataFrame(display_location_view[1][0:], columns=['label', 'x_coord', 'y_coord', 'num_restaurants', 'num_delivery_services', 'num_drones'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for locations currently.", icon="⚠")


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[28] display_ingredient_view()")
display_ingredient_view = sql.getIngredientView()
if (display_ingredient_view[0]):
    df = pd.DataFrame(display_ingredient_view[1][0:], columns=['ingredient_name', 'location', 'amount_available', 'low_price', 'high_price'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this ingredient currently.", icon="⚠")


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("[29] display_service_view()")

display_service_view = sql.getServiceView()
if (display_service_view[0]):
    df = pd.DataFrame(display_service_view[1][0:], columns=['id', 'long_name', 'home_base', 'manager', 'revenue', 'ingredients_carried', 'cost_carried', 'weight_carried'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this delivery service currently.", icon="⚠")

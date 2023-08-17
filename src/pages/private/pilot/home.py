import random
import streamlit as st
from src.lib.sql_wrapper import addDrone, addLocation, flyDrone, getFuelRequired, getLocationView, getPilotView, joinSwarm, leaveSwarm, loadDrone, refuel_drone, removeDrone, run_query_all, run_query_one, takeoverDrone
import pandas as pd

st.title("👨‍✈️ Pilot Home Page")
st.markdown("""
    Welcome to the home page for pilots. This will allow you to perform a few functionalities related to drones, swarms, and locations. Here
    is a list of all you can do:
    * [6]: **add_drone** - This stored procedure creates a new drone.
    * [9]: **add_location** - This stored procedure creates a new location that becomes a new valid drone destination.
    * [14]: **takeover_drone** - This stored procedure allows a valid pilot to take control of a lead drone owned by the same delivery service, whether it's a "lone drone" or the leader of a swarm.
    * [15]: **join_swarm** - This stored procedure takes a drone that is currently being directly controlled by a pilot and has it join a swarm (i.e., group of drones) led by a different directly controlled drone.
    * [16]: **leave_swarm** - This stored procedure takes a drone that is currently in a swarm and returns it to being directly controlled by the same pilot who's controlling the swarm.
    * [17]: **load_drone** - This stored procedure allows us to add some quantity of fixed-size packages of a specific ingredient to a drone's payload so that we can sell them for some specific price to other restaurants.
    * [18]: **refuel_drone** - This stored procedure allows us to add more fuel to a drone.
    * [19]: **fly_drone** - This stored procedure allows us to move a single or swarm of drones to a new location (i.e., destination).
    * [22]: **remove_drone** - This stored procedure removes a drone from the system.
    * [26]: **display_pilot_view** - This view displays information in the system from the perspective of a pilot.
    * [27]: **display_location_view** - This view displays information in the system from the perspective of a location.
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
st.header("Add Drone")


col1, col2 = st.columns(2)
with col1:
    get_add_drone_id = run_query_all("SELECT distinct(id) FROM delivery_services")
    add_drone_id_list = ["Select a Delivery Service ID"]
    if (get_add_drone_id[0]):
        for did in get_add_drone_id[1]:
            add_drone_id_list.append(did[0])
        add_drone_id = st.selectbox(label="Select an Delivery Service", options=add_drone_id_list) # ip_id varchar(40)
    add_drone_fuel = st.number_input(label="Enter Fuel", min_value=0, value=0) # ip_fuel integer
    add_drone_sales = st.number_input(label="Enter Sales", min_value=0, value=0) # ip_sales integer

with col2:
    add_drone_tag = st.text_input(label="Input a Unique Drone Tag") # ip_tag integer
    add_drone_capacity = st.number_input(label="Enter Capacity", min_value=0, value=0) # ip_capacity integer

    add_drone_pilot_list = ["Select a Pilot"]
    get_pilot_by_id = run_query_all(f"SELECT distinct(work_for.username) FROM work_for, pilots WHERE id=\'{add_drone_id}\' and work_for.username=pilots.username")
    if (get_pilot_by_id[0]):
        for pilot in get_pilot_by_id[1]:
            add_drone_pilot_list.append(pilot[0])
        add_drone_flown_by = st.selectbox(label="Select an Pilot", options=add_drone_pilot_list) # ip_flown_by varchar(40)

if st.button("Press to Add a New Drone ✅🤖"):
    if (add_drone_id == add_drone_id_list[0]):
        st.error("Please select a delivery service ID!")
    elif (add_drone_flown_by == add_drone_pilot_list[0]):
        st.error("Please select a pilot!")
    else:
        res = addDrone(add_drone_id, add_drone_tag, add_drone_fuel, add_drone_capacity, add_drone_sales, add_drone_flown_by)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - New Drone Added 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Location")


col1, col2, col3, col4 = st.columns(4)
with col1:
    add_location_label = st.text_input(label="Enter a Valid Label") # ip_label varchar(40)
with col2:
    add_location_x_coord = st.number_input(label="Enter X Coordinate ➡", value=0) # ip_x_coord integer
with col3:
    add_location_y_coord = st.number_input(label="Enter Y Coordinate ⬆", value=0) # ip_y_coord integer
with col4:
    add_location_space = st.number_input(label="Enter Space", min_value=0, value=0) # ip_space integer

if st.button("Press to Add a New Location 🌎"):
    if (len(add_location_label) == 0):
        st.error("⚠ Please enter a valid label!")
    else:
        res = addLocation(add_location_label, add_location_x_coord, add_location_y_coord, add_location_space)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - New Location Added 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Takeover Drone")


get_takeover_drone_pilots = run_query_all("SELECT username FROM pilots")
takeover_drone_pilot_list = ["Select a Pilot"]
if (get_takeover_drone_pilots[0]):
    for pilot in get_takeover_drone_pilots[1]:
        takeover_drone_pilot_list.append(pilot[0])
takeover_drone_pilot = st.selectbox(label="Select a valid pilot", options=takeover_drone_pilot_list) # ip_username varchar(40)

# Get the id, tag of the drones that belong to the same delivery service of the pilot
col1, col2 = st.columns(2)
with col1:
    get_id_drones = run_query_all(f"SELECT distinct(id) FROM drones WHERE id IN (SELECT id FROM work_for WHERE username=\'{takeover_drone_pilot}\')")
    takeover_drone_id_list = ["Select a Delivery Service ID"]
    if (get_id_drones[0]):
        for id in get_id_drones[1]:
            takeover_drone_id_list.append(id[0])
    takeover_drone_id = st.selectbox(label="Select a valid delivery service id", options=takeover_drone_id_list) # ip_id varchar(40)

with col2:
    get_takeover_drone_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{takeover_drone_id}\'")
    takeover_drone_tag_list = ["Select a Drone Tag"]
    if (get_takeover_drone_tag[0]):
        for tag in get_takeover_drone_tag[1]:
            takeover_drone_tag_list.append(tag[0])
    takeover_drone_tag = st.selectbox(label="Select a valid drone tag", options=takeover_drone_tag_list) # ip_tag integer

if st.button("Press to Takeover Drone"):
    if (takeover_drone_pilot == takeover_drone_pilot_list[0]):
        st.error("Please select a valid pilot.")
    elif (takeover_drone_id == takeover_drone_id_list[0]):
        st.error("Please select a valid id.")
    elif (takeover_drone_tag == takeover_drone_tag_list[0]):
        st.error("Please select a valid drone tag.")
    else:
        res = takeoverDrone(takeover_drone_pilot, takeover_drone_id, takeover_drone_tag)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Drone Taken Over 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Join Swarm")


col1, col2 = st.columns(2)
with col1:
    join_swarm_id_list = ["Select Drone ID"]
    get_all_existing_direct_drones = run_query_all("SELECT distinct(id) FROM drones")
    if (get_all_existing_direct_drones[0]):
        for drone_id in get_all_existing_direct_drones[1]:
            join_swarm_id_list.append(drone_id[0])
    join_swarm_id = st.selectbox(label="Select a Drone ID", options=join_swarm_id_list) # ip_id varchar(40)

with col2:
    join_swarm_tag_list = ["Select Drone Tag"]
    get_all_drones_from_id = run_query_all(f"SELECT tag FROM drones WHERE id=\'{join_swarm_id}\'")
    if (get_all_drones_from_id[0]):
        for drone_tag in get_all_drones_from_id[1]:
            join_swarm_tag_list.append(drone_tag[0])
    join_swarm_tag = st.selectbox(label="Select a Drone Tag", options=join_swarm_tag_list) # ip_tag integer

swarm_leader_tag = ["Select Swarm Leader"]
get_join_swarm_leader_tags = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{join_swarm_id}\' AND tag<>\'{join_swarm_tag}\' AND swarm_tag IS NULL")
if (get_join_swarm_leader_tags[0]):
    for tag in get_join_swarm_leader_tags[1]:
        swarm_leader_tag.append(tag[0])
new_leader_tag = st.selectbox(label="Select a Swarm Leader to Join", options=swarm_leader_tag) # ip_swarm_leader_tag integer

if st.button("Press to Join Swarm 👫"):
    if (join_swarm_id == join_swarm_id_list[0]):
        st.error("Please select a valid drone id.")
    elif (join_swarm_tag == join_swarm_tag_list[0]):
        st.error("Please select a valid drone tag.")
    elif (new_leader_tag == swarm_leader_tag[0] or new_leader_tag == None):
        st.error("Please select a valid swarm leader.")
    else:
        res = joinSwarm(join_swarm_id, join_swarm_tag, new_leader_tag)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Swarm Joined 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Leave Swarm")


col1, col2 = st.columns(2)
with col1:
    get_leave_swarm_id = run_query_all("SELECT distinct(id) FROM drones")
    leave_swarm_id_list = ["Select a Drone ID"]
    if (get_leave_swarm_id[0]):
        for id in get_leave_swarm_id[1]:
            leave_swarm_id_list.append(id[0])
    leave_swarm_id = st.selectbox(label="Select a Drone ID to be Transferred", options=leave_swarm_id_list) # ip_id varchar(40)
with col2:
    get_leave_swarm_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{leave_swarm_id}\'")
    leave_swarm_tag_list = ["Select a Drone Tag"]
    if (get_leave_swarm_tag[0]):
        for tag in get_leave_swarm_tag[1]:
            leave_swarm_tag_list.append(tag[0])
    leave_swarm_tag = st.selectbox(label="Select a Drone Tag to be Transferred", options=leave_swarm_tag_list) # ip_swarm_tag integer

if st.button("Press to Transfer Drone 🤖 ➡ 👨🏾‍✈️"):
    if (leave_swarm_id == leave_swarm_id_list[0]):
        st.error("Please select a valid drone id.")
    elif (leave_swarm_tag == leave_swarm_tag_list[0]):
        st.error("Please select a valid drone tag.")
    else:
        res = leaveSwarm(leave_swarm_id, leave_swarm_tag)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Drone Transferred 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Load Drone 📦")


col1, col2 = st.columns(2)
with col1:
    get_load_drone_id = run_query_all("SELECT distinct(id) FROM drones")
    if (get_load_drone_id[0]):
        load_drone_id_list = ["Select a Drone ID"]
        for did in get_load_drone_id[1]:
            load_drone_id_list.append(did[0])
        load_drone_id = st.selectbox(label="Select a Delivery Service ID to Load Drone", options=load_drone_id_list) # ip_id varchar(40)
    else:
        st.error(get_load_drone_id[1])

with col2:
    get_load_drone_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{load_drone_id}\'")
    if (get_load_drone_tag[0]):
        load_drone_tag_list = ["Select a Drone Tag"]
        for tag in get_load_drone_tag[1]:
            load_drone_tag_list.append(tag[0])
        load_drone_tag = st.selectbox(label="Select a Drone Tag to Load", options=load_drone_tag_list) # ip_tag integer
    else:
        st.error(get_load_drone_tag[1])

col3, col4 = st.columns(2)
with col3:
    get_load_drone_barcode = run_query_all("SELECT distinct(barcode) FROM ingredients") 
    if (get_load_drone_barcode[0]):
        load_drone_barcode_list = ["Select a Barcode"]
        for barcode in get_load_drone_barcode[1]:
            load_drone_barcode_list.append(barcode[0])
        load_drone_barcode = st.selectbox(label="Select a Barcode to Load", options=load_drone_barcode_list) # ip_barcode varchar(40)
    else:
        st.error(get_load_drone_barcode[1])
with col4:
    load_drone_more_packages = st.number_input(label="Select a Quantity of Packages to Load Drone", min_value=0, value=0) # ip_more_packages integer

load_drone_price = st.number_input(label="Select a Sale Price for Ingredient", min_value=0, value=0) # ip_price integer

if st.button("Press to Load Drone"):
    res = loadDrone(load_drone_id, load_drone_tag, load_drone_barcode, load_drone_more_packages, load_drone_price)
    if (res[0]):
        st.write("Successfully Called Stored Procedure - Drone Loaded 🙂")
    else:
        st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Refuel Drone ⛽")


col1, col2 = st.columns(2)
with col1:
    get_refuel_drone_id = run_query_all("SELECT distinct(id) FROM drones")
    if (get_refuel_drone_id[0]):
        refuel_drone_id_list = ["Select a Drone ID"]
        for did in get_refuel_drone_id[1]:
            refuel_drone_id_list.append(did[0])
        refuel_drone_id = st.selectbox("Select a Delivery Service Drone to be Refueled", refuel_drone_id_list) # ip_id varchar(40)
    else:
        st.error(get_refuel_drone_id[1])

with col2:
    get_refuel_drone_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{refuel_drone_id}\'")
    if (get_refuel_drone_tag[0]):
        refuel_drone_tag_list = ["Select a Drone Tag"]
        for tag in get_refuel_drone_tag[1]:
            refuel_drone_tag_list.append(tag[0])
        refuel_drone_tag = st.selectbox("Select a Drone Tag to be Refueled", refuel_drone_tag_list) # ip_tag integer
    else:
        st.error(get_refuel_drone_tag[1])

refuel_drone_more_fuel = st.number_input(label="Select Added Fuel", min_value=1, value=1) # ip_more_fuel integer

if st.button("Press to Refuel Drone"):
    if (refuel_drone_id == refuel_drone_id_list[0]):
        st.error("Please select a drone id for refueling.")
    elif (refuel_drone_tag == refuel_drone_tag_list[0]):
        st.error("Please select a drone tag for refueling.")
    else:
        res = refuel_drone(refuel_drone_id, refuel_drone_tag, refuel_drone_more_fuel)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Drone Fefueled 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Fly Drone ✈")


col1, col2 = st.columns(2)
with col1:
    get_fly_drone_id = run_query_all("SELECT distinct(id) FROM drones")
    if (get_fly_drone_id[0]):
        fly_drone_id_list = ["Select a Drone ID"]
        for did in get_fly_drone_id[1]:
            fly_drone_id_list.append(did[0])
        fly_drone_id = st.selectbox(label="Select a Drone ID to be Flown", options=fly_drone_id_list) # ip_id varchar(40)
    else:
        st.error(get_fly_drone_id[1])

with col2:
    get_fly_drone_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{fly_drone_id}\'")
    if (get_fly_drone_tag[0]):
        fly_drone_tag_list = ["Select a Drone Tag"]
        for tag in get_fly_drone_tag[1]:
            fly_drone_tag_list.append(tag[0])
        fly_drone_tag = st.selectbox(label="Select a Drone Tag to be Flown", options=fly_drone_tag_list) # ip_tag integer
    else:
        st.error(get_fly_drone_tag[1])

get_fly_drone_locations = run_query_all("SELECT distinct(label) FROM locations")
if (get_fly_drone_locations[0]):
    fly_drone_location_list = ["Select a Location"]
    for location in get_fly_drone_locations[1]:
        fly_drone_location_list.append(location[0])
    fly_drone_destination = st.selectbox(label="Select a Destination to Travel To", options=fly_drone_location_list) # ip_destination varchar(40)
else:
    st.error(get_fly_drone_locations[1])

if st.button("Takeoff ☁"):
    if (fly_drone_id == fly_drone_id_list[0]):
        st.error("Please enter a drone id to be flown.")
    elif (fly_drone_tag == fly_drone_tag_list[0]):
        st.error("Please enter a drone tag to be flown.")
    elif (fly_drone_destination == fly_drone_location_list[0]):
        st.error("Please enter a destination to fly to.")
    else:
        res = flyDrone(fly_drone_id, fly_drone_tag, fly_drone_destination)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Drone Flying 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Remove Drone")


col1, col2 = st.columns(2)
with col1:
    get_remove_drone_id = run_query_all("SELECT distinct(id) FROM drones")
    if (get_remove_drone_id):
        remove_drone_id_list = ["Select a Drone ID"]
        for did in get_remove_drone_id[1]:
            remove_drone_id_list.append(did[0])
        remove_drone_id = st.selectbox("Select a Delivery Service Drone to be Removed", remove_drone_id_list, label_visibility="collapsed") # ip_id varchar(40)
    else:
        st.error(get_remove_drone_id[1])

with col2:
    get_remove_drone_tag = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{remove_drone_id}\'")
    if (get_remove_drone_tag[0]):
        remove_drone_tag_list = ["Select a Drone Tag"]
        for tag in get_remove_drone_tag[1]:
            remove_drone_tag_list.append(tag[0])
        remove_drone_tag = st.selectbox("Select a Drone Tag to be Removed", remove_drone_tag_list, label_visibility="collapsed") # ip_tag integer
    else:
        st.error(get_remove_drone_tag[1])


if st.button("Press to Remove Drone ❌🤖"):
    if (remove_drone_id == remove_drone_id_list[0]):
        st.error("Please select a valid delivery service ID!")
    elif (remove_drone_tag == remove_drone_tag_list[0]):
        st.error("Please select a valid tag!")
    else:
        res = removeDrone(remove_drone_id, remove_drone_tag)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Drone Removed 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Pilot View")


display_pilot_view = getPilotView()
if (display_pilot_view[0]):
    df = pd.DataFrame(display_pilot_view[1][0:], columns=['username', 'licenseID', 'experience', 'num_drones', 'num_locations'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for pilots currently.", icon="⚠") 
else:
    st.error(display_pilot_view[1])
    

st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Location View")


display_location_view = getLocationView()
if (display_location_view[0]):
    df = pd.DataFrame(display_location_view[1][0:], columns=['label', 'x_coord', 'y_coord', 'num_restaurants', 'num_delivery_services', 'num_drones'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for locations currently.", icon="⚠")
else:
    st.error(display_location_view[1])
import datetime
import streamlit as st
from src.lib.sql_wrapper import addOwner, addRestaurant, getIngredientView, getOwnerView, purchaseIngredient, run_query_all, run_query_one, startFunding
import pandas as pd
from pandas import DataFrame

st.title("🍴 Restaurant Owner Home Page")
st.markdown("""
    Welcome to the home page for restaurant owners. This will allow you to perform a few functionalities related to restaurants, purchasing ingredients, and restaurant owners. Here
    is a list of all you can do:
    * [1]: **add_owner** - This stored procedure creates a new owner.
    * [7]: **add_restaurant** - This stored procedure creates a new restaurant.
    * [10]: **start_funding** - This stored procedure opens a channel for a restaurant owner to provide funds to a restaurant.
    * [20]: **purchase_ingredient** - This stored procedure allows a restaurant to purchase ingredients from a drone at its current location.
    * [24]: **display_owner_view** - This view displays information in the system from the perspective of an owner. 
    * [28]: **display_ingredient_view** - This view displays information in the system from the perspective of the ingredients.
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
st.header("Add Owner")
add_owner_username = st.text_input(label="Enter a Username") # ip_username varchar(40)
col1, col2, col3 = st.columns(3)
with col1:
    add_owner_first_name = st.text_input(label="Enter First Name") # ip_first_name varchar(100)
with col2:
    add_owner_last_name = st.text_input(label="Enter Last Name") # ip_last_name varchar(100)
with col3:
    add_owner_address = st.text_input(label="Enter Address 🏡") # ip_address varchar(500)

add_owner_birthdate = st.date_input("Enter Birthday 🎂", datetime.date(2000, 1, 1)) # ip_birthdate date

if st.button("Add New Owner"):
    if (len(add_owner_username) == 0):
        st.error("Please enter a valid username.")
    elif (len(add_owner_first_name) == 0):
        st.error("Please enter a valid first name.")
    elif (len(add_owner_last_name) == 0):
        st.error("Please enter a valid last name.")
    elif (len(add_owner_address) == 0):
        st.error("Please enter a valid address.")
    else :
        res = addOwner(add_owner_username, add_owner_first_name, add_owner_last_name, add_owner_address, add_owner_birthdate)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - New Owner Added! 🙂")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Add Restaurant")
add_restaurant_long_name = st.text_input(label="Enter a Name for Restaurant") # ip_long_name varchar(40)

col1, col2, col3 = st.columns(3)
with col1:
    add_restaurant_rating = st.number_input(label="Enter a Rating for the Restaurant", min_value=1, max_value=5, value=1) # ip_rating integer
with col2:
    add_restaurant_spent = st.number_input(label="Enter Spending for the Restaurant", min_value=0, value=0, step=5) # # ip_spent integer
with col3:
    get_all_existing_locations = run_query_all("SELECT distinct(label) FROM locations")
    location_list = ["Select a Location 🌎"]
    if (get_all_existing_locations[0]):
        for label in get_all_existing_locations[1]:
            location_list.append(label[0])
        add_restaurant_location = st.selectbox(label="Select a Location for New Restaurant", options=location_list) # ip_location varchar(40)
    else:
        st.error(get_all_existing_locations[1])
    

if st.button("Add New Restaurant"):
    if (len(add_restaurant_long_name) == 0):
        st.error("Please enter a valid new restaurant name.")
    elif (add_restaurant_location == location_list[0]):
        st.error("Please select a location for the new restaurant.")
    else:
        res = addRestaurant(add_restaurant_long_name, add_restaurant_rating, add_restaurant_spent, add_restaurant_location)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - New Restaurant Added! 🙂")
        else:
            st.error(res[1])
        
st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Start Funding")
get_all_existing_owners = run_query_all("SELECT distinct(username) FROM restaurant_owners")
if (get_all_existing_owners[0]):
    owner_list = ["Select an Owner"]
    for owner in get_all_existing_owners[1]:
        owner_list.append(owner[0])
    start_funding_owner = st.selectbox(label="Select a owner to provide funds", options=owner_list) # ip_owner varchar(40)
else:
    st.error(get_all_existing_owners[1])

get_all_existing_restaurants = run_query_all("SELECT distinct(long_name) FROM restaurants")
if (get_all_existing_restaurants[0]):
    restaurant_list = ["Select a Restaurant"]
    for restaurant in get_all_existing_restaurants[1]:
        restaurant_list.append(restaurant[0])
    start_funding_long_name = st.selectbox(label="Select a restaurant to be funded", options=restaurant_list) # ip_long_name varchar(40))
else:
    st.error(get_all_existing_restaurants[1])

if st.button("Open Funding Channel"):
    if (start_funding_owner == owner_list[0]):
        st.error("Please select a valid owner.")
    elif (start_funding_long_name == restaurant_list[0]):
        st.error("Please select a valid restaurant.")
    else:
        res = startFunding(start_funding_owner, start_funding_long_name)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Funding Channel Opened! 😀")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Purchase Ingredient")
# Select a name of a restaurant 
purchase_ingredient_long_name = st.selectbox(label="Select a Restaurant to Purchase Ingredient", options=restaurant_list) # ip_long_name varchar(40) - restaurants
if (purchase_ingredient_long_name != "Select a Restaurant"):
    purchase_ingredient_long_name = purchase_ingredient_long_name.lower()
    get_location_by_restaurant = run_query_one(f"SELECT distinct(hover) FROM drones WHERE hover IN (SELECT location FROM restaurants WHERE long_name=\'{purchase_ingredient_long_name}\')")
    if (get_location_by_restaurant[0] and get_location_by_restaurant[1] is not None and len(get_location_by_restaurant[1]) != 0):
        get_location_by_restaurant = get_location_by_restaurant[1][0]

        col1, col2 = st.columns(2)
        with col1:
            get_all_id_by_location = run_query_all(f"SELECT distinct(id) FROM drones WHERE hover=\'{get_location_by_restaurant}\'") 
            # Select an id (this corresponds to the delivery service that will be ordered from and the delivery service that owns the specific drone)
            id_list = []
            if (get_all_id_by_location[0]):
                for id in get_all_id_by_location[1]:
                    id_list.append(id[0])
            purchase_ingredient_id = st.selectbox("Select a Delivery Service to Order Ingredient", options=id_list) # ip_id varchar(40) - drones
        with col2:
            get_all_tags_by_id = run_query_all(f"SELECT distinct(tag) FROM drones WHERE id=\'{purchase_ingredient_id}\' and hover=\'{get_location_by_restaurant}\'")
            tag_list = []
            if (get_all_tags_by_id[0]):
                for tag in get_all_tags_by_id[1]:
                    tag_list.append(tag[0])
            # Select a tag (this corresponds to the unique identifier of the drone, which depends on the selected id)
            purchase_ingredient_tag = st.selectbox(label="Select the Drone Tag to be Ordered From", options=tag_list) # ip_tag integer - drones

        get_all_existing_ingredients = run_query_all(f"SELECT distinct(barcode) FROM payload WHERE id=\'{purchase_ingredient_id}\' and tag=\'{purchase_ingredient_tag}\'")
        ingredient_barcode_list = ["Select an Ingredient"]
        if (get_all_existing_ingredients[0]):
            for ingredient in get_all_existing_ingredients[1]:
                ingredient_barcode_list.append(ingredient[0])
        purchase_ingredient_barcode = st.selectbox(label="Select an Ingredient Barcode to be Purchased", options=ingredient_barcode_list) # ip_barcode varchar(40) - ingredients

        purchase_ingredient_quantity = st.slider("Select Quantity of Ingredient", 1, 50) # ip_quantity integer - payload
        
    else:
        st.error("Sorry, there are no drones currently at this restaurant location.")

if st.button("Purchase Ingredient"):
    if (purchase_ingredient_long_name == restaurant_list[0]):
        st.error("Please select a valid restaurant.")
    elif (purchase_ingredient_barcode == ingredient_barcode_list[0]):
        st.error("Please select a valid ingredient.")
    else:
        res = purchaseIngredient(purchase_ingredient_long_name, purchase_ingredient_id, purchase_ingredient_tag, purchase_ingredient_barcode, purchase_ingredient_quantity)
        if (res[0]):
            st.write("Successfully Called Stored Procedure - Ingredient Purchased! 😀")
        else:
            st.error(res[1])


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Owner View")
display_owner_view = getOwnerView()
if (display_owner_view[0]):
    df = pd.DataFrame(display_owner_view[1][0:], columns=['username', 'first_name', 'last_name', 'address', 'num_restaurants', 'num_places', 'highs', 'lows', 'debt'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this owner currently.", icon="⚠")  
else:
    st.error(display_owner_view[1])
   


st.markdown("---") # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
st.header("Ingredient View")
display_ingredient_view = getIngredientView()
if (display_ingredient_view[0]):
    df = pd.DataFrame(display_ingredient_view[1][0:], columns=['ingredient_name', 'location', 'amount_available', 'low_price', 'high_price'])
    if (df.empty == False):
        st.write(df)
    else:
        st.error("Error: No information for this ingredient currently.", icon="⚠")
else:
    st.error(display_ingredient_view[1])

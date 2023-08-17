import mysql.connector
import streamlit as st 
from enum import Enum

class ROLES(Enum):
    PUBLIC = 0
    OWNER = 1
    PILOT = 2
    SERVICE = 3
    WORKER = 4
    
def check_connection():
    try:
        if 'db' not in st.session_state:
            st.session_state['db'] = mysql.connector.connect(**st.secrets['mysql']) 
        return (st.session_state['db'].is_connected(), None)
    except mysql.connector.Error as err:
        print("Connection error", err)
        return (False, err)
    
def getView(name: str):
    try:
        conn: mysql.connector.MySQLConnection = st.session_state['db']
        cursor = conn.cursor()
        query = 'SELECT * FROM ' + name
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return (True, results)
    except mysql.connector.Error as err:
        print("View error", err)
        cursor.close()
        return (False, err)
        
def callProc(name: str, args):
    try: 
        conn: mysql.connector.MySQLConnection = st.session_state['db']
        cursor = conn.cursor()
        cursor.callproc(name, args)
        conn.commit()
        cursor.close()
        return (True, None)
    except mysql.connector.Error as err:
        print("Procedure error", err)
        cursor.close()
        return (False, err)

def getIngredientView():
    return getView('display_ingredient_view')

def getServiceView():
    return getView('display_service_view')

def getLocationView():
    return getView('display_location_view')

def getPilotView():
    return getView('display_pilot_view')

def getEmployeeView():
    return getView('display_employee_view')

def getOwnerView():
    return getView('display_owner_view')

def addOwner(username: str, firstname: str, lastname: str, address: str, bday: str):
    return callProc('add_owner', [username, firstname, lastname, address, bday])

def addEmployee(username: str, firstname: str, lastname: str, address: str, bday: str, taxid: str, hired: str, experience: int, salary: int):
    return callProc('add_employee', [username, firstname, lastname, address, bday, taxid, hired, experience, salary])

def addPilot(username: str, licenseid: str, experience: int):
    return callProc('add_pilot_role', [username, licenseid, experience])

def addWorker(username: str):
    return callProc('add_worker_role', [username])

def addIngredient(barcode: str, name: str, weight: int):
    return callProc('add_ingredient', [barcode, name, weight])

def addDrone(serviceid: str, tag: int, fuel: int, capacity: int, sales: int, flownby: str):
    return callProc('add_drone', [serviceid, tag, fuel, capacity, sales, flownby])
    
def addRestaurant(restaurant: str, rating: int, spent: int, location: str):
    return callProc('add_restaurant', [restaurant, rating, spent, location])

def addService(serviceid: str, restaurant: str, base: str, manager: str):
    return callProc('add_service', [serviceid, restaurant, base, manager])

def addLocation(label: str, xcord: int, ycord: int, space: int):
    return callProc('add_location', [label, xcord, ycord, space])

def startFunding(owner: str, restaurant: str):
    return callProc('start_funding', [owner, restaurant])

def hireEmployee(username: str, serviceid: str):
    return callProc('hire_employee', [username, serviceid])

def fireEmployee(username: str, serviceid: str):
    return callProc('fire_employee', [username, serviceid])

def manageService(username: str, serviceid: str):
    return callProc('manage_service', [username, serviceid])

def takeoverDrone(username: str, serviceid: str, tag: int):
    return callProc('takeover_drone', [username, serviceid, tag])

def joinSwarm(serviceid: str, tag: int, leadertag: str):
    return callProc('join_swarm', [serviceid, tag, leadertag])

def leaveSwarm(serviceid: str, swarmtag: int):
    return callProc('leave_swarm', [serviceid, swarmtag])

def loadDrone(serviceid: str, tag: int, barcode: str, packages: int, price: int):
    return callProc('load_drone', [serviceid, tag, barcode, packages, price])

def refuel_drone(serviceid: str, tag: int, fuel: int):
    return callProc('refuel_drone', [serviceid, tag, fuel])

def getFuelRequired(departure: str, arrival: str):
    return callProc('fuel_required', [departure, arrival])

def flyDrone(serviceid: str, tag: int, destination: str):
    return callProc('fly_drone', [serviceid, tag, destination])

def purchaseIngredient(restaurant: str, serviceid: str, tag: int, barcode: str, amount: int):
    return callProc('purchase_ingredient', [restaurant, serviceid, tag, barcode, amount])

def removeIngredient(barcode: str):
    return callProc('remove_ingredient', [barcode])

def removeDrone(serviceid: str, tag: int):
    return callProc('remove_drone', [serviceid, tag])

def removePilotRole(username: str):
    return callProc('remove_pilot_role', [username])

def run_query_all(query: str):
    try:
        conn: mysql.connector.MySQLConnection = st.session_state['db']
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return (True, results)
    except mysql.connector.Error as err:
        print("Database Error", err)
        cursor.close()
        return (False, err)
        
def run_query_one(query: str):
    try:
        conn: mysql.connector.MySQLConnection = st.session_state['db']
        cursor = conn.cursor(buffered=True)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return (True, result)
    except mysql.connector.Error as err:
        print("Database Error", err)
        cursor.close()
        return (False, err)

def run_query_many(query: str, count: int):
    try:
        conn: mysql.connector.MySQLConnection = st.session_state['db']
        cursor = conn.cursor(buffered=True)
        cursor.execute(query);
        results = cursor.fetchmany(count)
        cursor.close()
        return (True, results)
    except mysql.connector.Error as err:
        print("Database Error", err)
        cursor.close()
        return (False, None)
        
    

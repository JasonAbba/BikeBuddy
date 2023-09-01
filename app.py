import streamlit as st
import pyrebase 
import re
from streamlit_option_menu import option_menu

# Streamlit Imp Variables
st.set_page_config(page_title = 'ECP PROJECT', page_icon = ':zap:', layout = 'wide')

# Firebase Configuration Key
firebaseConfig = {
    'apiKey': "AIzaSyDsY0-hfeVI2roagdIlzERYUWEHHDTAPF0",
    'authDomain': "bikebuddy0118.firebaseapp.com",
    'projectId': "bikebuddy0118",
    'databaseURL': "https://bikebuddy0118-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "bikebuddy0118.appspot.com",
    'messagingSenderId': "899355751515",
    'appId': "1:899355751515:web:b9c611f8645eec9c8ebb7e",
    'measurementId': "G-2TS8BDR3S0"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# Streamlit Session State Control
# class SessionState:
#     def __init__(self):
#         self.user_status = "logged_out"

# @st.cache_data()
# def get_session_state():
#     return SessionState()

# session_state = get_session_state()
if "user_status" not in st.session_state:
    st.session_state.user_status = 'logged_out'

# Function to load local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define a regular expression pattern for a basic email validation
def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None

# Define criteria for password validation
def is_valid_password(password):
    return len(password) >= 7

# Login and Sign Up Form
def userauth():
    st.sidebar.title("BikeBuddy")
    st.sidebar.empty()

    if st.session_state.user_status == "logged_out":
        choice = st.sidebar.selectbox("Login/Sign Up", ['Login', 'Sign Up'])
        
        # Login
        if choice == "Login":
            email = st.sidebar.text_input("E-Mail")
            password = st.sidebar.text_input("Password", type="password")
            submit = st.sidebar.button("Login")
            
            if submit and is_valid_email(email) and is_valid_password(password):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    username = db.child(user['localId']).child("username").get().val()
                    st.title("Welcome, " + username)

                    # Hide the sidebar after successful login
                    st.markdown(
                        """
                        <style>
                        section[data-testid="stSidebar"][aria-expanded="true"]{
                            display: none;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )
                    return "logged_in"
                except Exception as e:
                    st.warning("Incorrect Email or Password.")
        
        # Sign Up
        elif choice == "Sign Up":
            name = st.sidebar.text_input("Full Name")
            email = st.sidebar.text_input("E-Mail")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            age = st.sidebar.number_input("Age", min_value=18, step=1)
            blood_types = ['Select', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
            blood_group = st.sidebar.selectbox("Blood Group", blood_types)
            mob_number = st.sidebar.text_input("Mobile Number")
            submit = st.sidebar.button("Sign Up")
            
            if submit:
                try:
                    user = auth.create_user_with_email_and_password(email, password)

                    db.child(user['localId']).child("name").set(name)
                    db.child(user['localId']).child("email").set(email)
                    db.child(user['localId']).child("username").set(username)
                    db.child(user['localId']).child("password").set(password)
                    db.child(user['localId']).child("age").set(age)
                    db.child(user['localId']).child("blood_group").set(blood_group)
                    db.child(user['localId']).child("mob_number").set(mob_number)
                    db.child(user['localId']).child("ID").set(user['localId'])

                    st.success("Your account has been created successfully. Go ahead and log in.")
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.info("Welcome, " + username)
                except Exception as e:
                    pass

#! ---> runapp() is calling the below modules
def check_log(widgets_list):
    for i in widgets_list:
        if i == "":
            st.warning("Fill the missing fields")
            return False
    return True
def tab1_content():
    st.session_state.user_status = "logged_in"
    col1, col2, col3 = st.columns([1.5, 1, 3])

    with col1:
        st.subheader('Log your ride details here.')
        starting_loc = st.text_input('Starting Point')
        destination_loc = st.text_input('Destination')
        fuel = st.slider('Petrol in tank', min_value=0.5, max_value = 15.0, step = 0.5)
        petrol_exp = st.number_input('Petrol Expenditure', step = 1)
        start_odo = st.number_input('Starting Odometer', step = 1)
        end_odo = st.number_input('Ending Odometer', step = 1)
        with st.expander('More...'):
            other_exp = st.number_input('Misc. Expenses', step = 1)

        widgets_list = [starting_loc, destination_loc, fuel, petrol_exp, start_odo, end_odo]
        log_btn = st.button('Log Details')
        if log_btn:
            log_status = check_log(widgets_list)
            if log_status:
                #! feed details in firebase
                #! feed details in firebase
                #! feed details in firebase
                pass

    with col2:
        st.empty()
    with col3:
        # can display some image here
        st.subheader('Log sheet preview.')
        st.divider()
        st.write("\n")
        st.write("💠 Starting Point: ", starting_loc)
        st.write("💠 Destination: ", destination_loc)
        st.write("💠 Fuel in Tank: ", fuel, "Ltrs." )
        st.write("💠 Fuel Expense: ₹", petrol_exp)
        st.write("💠 Starting Odometer Reading: ", start_odo, "Kms")
        st.write("💠 Ending Odometer Reading: ", end_odo, "Kms")
        st.write("💠 Total Distance: ", end_odo - start_odo, "Kms")
        st.write("💠 Other Expenses: ₹", other_exp)
        st.write("", )
        st.write("", )
        
def tab2_content():
    st.subheader('All your previous Rides, well documented.')

def tab3_content():
    st.subheader('Join your fellow riders from the Motorcycling Community.')
def tab4_content():
    st.subheader('All your important documents, stored away safe and secure.')


def runapp():
    # After Login and Sign Up
    # st.sidebar.title("BikeBuddy")
    if st.session_state.user_status == "logged_in": # which means user is logged in
        options = ["Ride Log", "My Rides", "Create/Join a Ride", "Your Documents"]
        icons = ["book", "person-check", "plus-circle", "files"]
        nav_item = option_menu(
            menu_title = "BikeBuddy",
            options = options,
            icons = icons,
            menu_icon = "wrench-adjustable",
            orientation = "horizontal"
        )
      
        if nav_item == "Ride Log":
            tab1_content()
        if nav_item == "My Rides":
            tab2_content()
        if nav_item == "Create/Join a Ride":
            tab3_content()
        if nav_item == "Your Documents":
            tab4_content()

# ---------> Webapp entry point
if __name__ == "__main__":
    local_css("css/style.css")
    if st.session_state.user_status == "logged_out":
        # After successful login, change the session_state to "logged_in"
        print('before userauth()', st.session_state.user_status)
        st.session_state.user_status = userauth() # should return "logged_in"
        print('after userauth()', st.session_state.user_status)
        if st.session_state.user_status == "logged_in":
            runapp()


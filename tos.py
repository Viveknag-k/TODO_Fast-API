import streamlit as st
import requests

base_url = "http://127.0.0.1:8000"


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("📝TODO List....!")

if not st.session_state.logged_in:
    
    page = st.selectbox("Choose your action:", ["🏠Sign In", "🏡Sign Up"])

    if page == "🏡Sign Up":
        new_username = st.text_input("Enter a new Username : ")
        new_password = st.text_input("Enter a Password (min. 8 characters..) : ", type="password")
        
        if st.button("🏡Sign Up"):
            if new_username and new_password:
                signup_response = requests.post(f"{base_url}/Sign_Up/", json={"username": new_username, "password": new_password})
                
                if signup_response.status_code == 200:
                    st.success("Signed up successfully. You can sign in now!")
                elif signup_response.status_code == 400:
                    st.error("Username already exists")
                else:
                    st.error("Something went wrong")
            else:
                st.error("Please fill in the details!")

    elif page == "🏠Sign In":
        username = st.text_input("Enter username:")
        password = st.text_input("Enter password:", type="password")
        
        if st.button("🏠Sign In"):
            if username and password:
                signin_response = requests.post(f"{base_url}/Sign_In/", json={"username": username, "password": password})
                
                if signin_response.status_code == 200:
                    st.success("Logged in successfully")
                    
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Please fill in the details")
else:
    
    st.write(f"Welcome, {st.session_state.username}!")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun() 

    
    tab1, tab2, tab3 = st.tabs(["Show TODO", "Add TODO", "Delete TODO"])

    with tab1:
        if st.button("Show TODO"):
            response = requests.get(f"{base_url}/Show_Tasks/", params={"username": st.session_state.username})
            if response.status_code == 200:
                todo_list = response.json()
                if len(todo_list) == 0:
                    st.info("Your TODO list is empty.")
                else:
                    st.write(todo_list, expanded=True)
            else:
                st.error("Failed to fetch the TODO list.")

    with tab2:
        item = st.text_input("Enter your task:")
        if st.button("Add TODO"):
            if item:
                response = requests.post(f"{base_url}/Add_Task/", params={"username": st.session_state.username}, json={"task": item})
                if response.status_code == 200:
                    st.success("Added to TODO list.")
                else:
                    st.error("Something went wrong.")
            else:
                st.error("Please enter a task.")

    with tab3:
        task_to_delete = st.text_input("Enter the task to delete:")
        if st.button("Delete TODO"):
            if task_to_delete:
                response = requests.delete(f"{base_url}/Delete_Task/", params={"username": st.session_state.username, "task_name": task_to_delete})
                if response.status_code == 200:
                    st.success("Task deleted successfully.")
                else:
                    st.error("Failed to delete the task.")
            else:
                st.error("Please enter a task name to delete.")

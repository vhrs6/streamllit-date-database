import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from time import strftime, gmtime, time
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


st.set_page_config(page_title='Dates', initial_sidebar_state='collapsed', page_icon='🗺')


names=['Vicky','Shravya']
username=['vicky','shravya']


with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    
)

authenticator.login()
    
if st.session_state["authentication_status"]:
    test=authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    


    st.title("Dates Management Portal 🌐")

   
    conn = st.connection("gsheets", type=GSheetsConnection)

    
    existing_data = conn.read(worksheet="Sheet1", usecols=list(range(4)), ttl=5)
    existing_data = existing_data.dropna(how="all")



 
    selected_option = st.sidebar.radio("Select an option", ("Enter Data", "Display Data"))

    if selected_option == "Enter Data":
        st.markdown("Enter the details of the date below 🖋️.")
        
        with st.form(key="dates_database"):
            place = st.text_input(label="**Place***")
            amount = st.text_input(label="**Amount***")
            
            st.markdown("**required*")

            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if not place or not amount:
                    st.warning("Ensure all mandatory fields are filled.")
                    st.stop()
                else:
                   
                    date_data = pd.DataFrame(
                        [
                            {
                                "Place": place,
                                "Amount": amount,
                                "Time": strftime("%a, %d %b %Y %H:%M:%S", gmtime(time() + 19800)),
                                "User": st.session_state["name"]
                            }
                        ]
                    )

                    
                    updated_df = pd.concat([existing_data, date_data], ignore_index=True)

                    
                    conn.update(worksheet="Sheet1", data=updated_df)

                    
                    st.success("Details successfully submitted!")


    elif selected_option == "Display Data":
        
        st.markdown("### Data 📄")
        st.dataframe(existing_data,width=4000)
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 17:15:08 2022

@author: Thisu
"""

import streamlit as st
import joblib
import pyrebase
#from pyrebase import pyrebase
from datetime import datetime

#configuration key
firebaseConfig = {
  'apiKey': "AIzaSyDRwWtwfI7dDiAUxmUDBgfA-fGyoi3jNB8",
  'authDomain': "drbigbot-36eb7.firebaseapp.com",
  'projectId': "drbigbot-36eb7",
  'databaseURL': "https://drbigbot-36eb7-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "drbigbot-36eb7.appspot.com",
  'messagingSenderId': "823848117287",
  'appId': "1:823848117287:web:e820416700ce7c24721a02",
  'measurementId': "G-JR1ZFSXQVB"
};

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database
db = firebase.database()
storage = firebase.storage()


# Authentication

choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign Up'])

email = st.sidebar.text_input('Please input your email')
password = st.sidebar.text_input('Please enter your password', type = 'password')



# Sign up Block

if choice == 'Sign Up':
    handle = st.sidebar.text_input('Please input your app handle name', value= 'Default')
    submit = st.sidebar.button('Create my account')
    
    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Your account is created sucsessfully')
        st.balloons()
        #sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('login via login drop down selection')

# Login Block
        
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        
        bio = st.radio('Jump to', ['Home', 'Recomandation', 'Settings'])
        
        

exp1 = st.expander('Input/Change Bio details')
with exp1:   

        p1 = st.slider('Enter Your Age',18,100)
        
        p2 = st.number_input("Enter your Blood Sugar Fast(mmol/L):")
    
        p3 = st.number_input("Enter your HbA1c(mmol/mol):")
         
    
        save_bio = st.button('Save')
    
        #send user static bio to DataBase
        if save_bio:
            age = db.child(user['localId']).child("p1").push(p1)
            bs_fast = db.child(user['localId']).child("p2").push(p2)
            hb1ac = db.child(user['localId']).child("p3").push(p3)
                        
                # load the model
clf = joblib.load('Diabetes_Type_model3')
                
if st.button('Predict'):
                    
                   #calling db user bio data 
                   
    db_age = db.child(user['localId']).child("p1").get().val()         
    if db_age is not None:
        val = db.child(user['localId']).child("p1").get()
        for child_val in val.each():
            p1_get = child_val.val()   
    else:
        st.info("Error!")
 
    db_bs_fast = db.child(user['localId']).child("p2").get().val()
    if db_bs_fast is not None:
           val = db.child(user['localId']).child("p2").get()
           for child_val in val.each():
               p2_get = child_val.val()
    else:
        st.info("Error!")
                
  
                   
    db_hb1ac = db.child(user['localId']).child("p3").get().val()
    if db_hb1ac is not None:
        val = db.child(user['localId']).child("p3").get()
        for child_val in val.each():
            p3_get = child_val.val()
    else:
         st.info("Error!")
                   
                   
                   
    #run Diabetes type model
    prediction = clf.predict([[p1_get,p2_get,p3_get]])
                   
    st.success('Your Diabetes Type is: {} '.format(prediction[0]))

        

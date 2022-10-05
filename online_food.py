import json
import numpy as np
import pickle
import streamlit as st
import base64

# import saved model
def load_artifacts():
    # print("loading saved artifacts...start")

    global __columns
    global __model

    with open("./columns.json", "r") as f:
        __columns = json.load(f)["data_columns"]

    with open("./order.pickle", "rb" ) as f:
        __model = pickle.load(f)
    
    # print("loading saved artifacts...done")

# order prediction functiom
def order_again(age, gender, marital, occupation, income, qualification, fam_size, pin, feedback):
    x = np.zeros(len(__columns))

    x[0] = age
    x[1] = gender
    x[2] = marital
    x[3] = occupation
    x[4] = income
    x[5] = qualification
    x[6] = fam_size
    x[7] = pin
    x[8] = feedback 

    d = __model.predict([x])[0]

    if d == 1:
        return 'Yes'
    else:
        return 'No' 

@st.experimental_memo

# background image processing

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("These ads make you think of McDonald_s.jpg")


# css code for background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]> .main {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}
[data-testid= "stHeader"]{{
background: rgba(0,0,0,0);
}}
</style>
"""
# web page code
def main():
    # background image
    st.markdown(page_bg_img, unsafe_allow_html= True)

    # Title
    st.title("Online Food Reoder Prediction")

    # user instructions
    instructions = '<p style="font-family:Sans serif; font-weight: bold; color:white; font-size: 20px;">Enter Customer Details to Predict If the Customer Will Order Again</p>'
    st.markdown(instructions, unsafe_allow_html= True)

    # user input
    age = st.text_input("Enter the Age of the Customer")
    gender = st.text_input("Enter the Gender of the Customer (1 = Male, 0 = Female):")
    marital = st.text_input("Marital Status of the Customer (1 = Single, 2 = Married, 0 = Not Revealed):")
    occupation = st.text_input("Occupation of the Customer (Student = 1, Employee = 2, Self Employeed = 3, House wife = 4):")
    income =st.text_input("Monthly Income: ('No Income': 0,'25001 to 50000': 5000, 'More than 50000': 7000, '10001 to 25000': 25000, 'Below Rs.10000': 10000")
    qualification = st.text_input("Educational Qualification (Graduate = 1, Post Graduate = 2, Ph.D = 3, School = 4, Uneducated = 5):")
    fam_size = st.text_input("Family Size")
    pin = st.text_input("Pin Code")
    feedback = st.text_input("Review of the Last Order (1 = Positive, 0 = Negative)")

    # prediction code
    food = ''

    # prediction button
    if st.button("Will the customer order again"):
        food = order_again(age, gender, marital, occupation, income, qualification, fam_size, pin, feedback)

    st.success(food)



if __name__ == '__main__':
    load_artifacts()
    main()
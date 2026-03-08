import streamlit as st

st.title("Simple Streamlit Calculator")
st.header("Simple Calculator")

#Numbers input
num1 = st.number_input("Enter first number: ")
num2 = st.number_input("Enter second number: ")

#Dropdown selection
operation = st.selectbox("Select Math Operation",["Add","Subtract","Multiply","Divide"])

#Calculate button
if st.button("Calculate"):
    try:
        if operation == "Add":
            result = num1 + num2

        elif operation == "Subtract":
            result = num1 - num2

        elif operation == "Multiply":
            result = num1 * num2

        elif operation == "Divide":
            result = num1 / num2

        st.success(f"The result is {result}")

    except:
        st.error("Error: Value cannot be divided by zero")

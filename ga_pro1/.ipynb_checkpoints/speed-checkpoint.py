import streamlit as st
import pandas as pd

with st.sidebar:
    page_chosen = st.radio(
        "MENU",
        ("Home Page", "Summary Page")
    )


if page_chosen == "Home Page":
    st.title("My Spending App")

    Item = st.text_input("What did you spend on?", "")
    st.write("I spent on:", Item)

    number = st.number_input("Insert a number", step=0.1)

    category = st.selectbox("What category did you spend on?",
    ("Food", "Clothes", "Transport", "Technology"))

    if st.button("Add Expense"):
        st.write("Done")
        new_row = pd.DataFrame({"Item": [Item], "number": [number], "category": [category]})


        original_df = pd.read_csv("test.csv")
        new_df = pd.concat([original_df, new_row], ignore_index=True)
        new_df
        new_df.to_csv('test.csv', index=False)
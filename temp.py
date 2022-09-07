# imports streamlit for gui implementation
import streamlit as st

# imports the entirety of the optimization code in one method from another file
from base import whole

# creates a title and body text for the gui
title = st.title("Summit Lineups")
body1 = st.text("This is not a guaranteed way to make money and you may lose.")
body2 = st.text("However, we haven't lost money yet.")

# adds user input boxes for username and password
username = st.text_area("Username")
password = st.text_area("Password")

# adds a button to enter in the user input for username and password
enter = st.button("Enter")

# dictionary of all valid usernames and passwords combinations
valid_logins = {"benmrosek" : "cheetah11",
                "thomas31406" : "Snoopy01",
                "willbrantley" : "allstar55",
                "bhelms" : "He10232000",
                "benreno18" : "utexas1",
                "jakerussporter" : "91899189",
                "admin" : "K4a27Bl4gj2",
                "shanny" : "shanny",
                "bsully43" : "capitals08",
                "Ctrimble01" : "Dell1213",
                "BrianAbes" : "BA1622"}

# verifies username and password for access
if (password == valid_logins.get(username) and enter == True):
    # calls the entirety of the optimization code and displays it if username
    # and password combo is valid by unpacking the multiple returns
    wait = st.text("Est Wait Time: 10s")
    thing = whole()
    dF1, dF2, dF3 = thing
    explain1 = st.text("Lineup 1")
    st.dataframe(dF1)
    explain2 = st.text("Lineup 2")
    st.dataframe(dF2)
    explain3 = st.text("Lineup 3")
    st.dataframe(dF3)
elif (enter == True):
    # shows an error message if username and password combo is no valid
    st.text("Incorrect username and/or password")
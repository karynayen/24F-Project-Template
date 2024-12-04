# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of analyst ------------------------
def AnalaystHomeNav():
    st.sidebar.page_link(
        "pages/00_Analyst_Home.py", label="Analyst Home", icon="👤"
    )


def CompanyRatingsNav():
    st.sidebar.page_link(
        "pages/01_Company_Ratings.py", label="Company Ratings", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")

def GeneralRatingsNav():
    st.sidebar.page_link("pages/05_General_Ratings_By_Major.py", label="General Ratings By Major", icon="🗺️")



#### ------------------------ Examples for Role of reviewer ------------------------
def ReviewerHomeNav():
    st.sidebar.page_link("pages/10_Reviewer_Home.py", label="Reviewer Home", icon="🏠")

def SeeUserReviewsNav():
    st.sidebar.page_link("pages/See_User_Reviews.py", label="See Your Reviews", icon="📄")

def AddReviewNav():
    st.sidebar.page_link("pages/Add_Review.py", label="Add a Review", icon="➕")

def SeeCompanyReviewsNav():
    st.sidebar.page_link("pages/See_Company_Reviews.py", label="See Company Reviews", icon="🏢")



#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")
    st.sidebar.page_link(
        "pages/21_ML_Model_Mgmt.py", label="ML Model Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show "Company Ratings" Link and "General Ratings By Major" Link if the user is a ANALYST role.
        if st.session_state["role"] == "analyst":
            AnalaystHomeNav()
            CompanyRatingsNav()
            MapDemoNav()
            GeneralRatingsNav()
            

        # If the user role is reviewer, show the Reviewer pages
        if st.session_state["role"] == "reviewer":
            ReviewerHomeNav()
            SeeUserReviewsNav()
            AddReviewNav()
            SeeCompanyReviewsNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

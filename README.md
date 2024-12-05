# GlassHusky Repository
Team members: Karyna Yen, Quangvinh Tran, Ikechukwu Ekpunobi, Patrick Rose, Astro Ohnuma

## Project Description
Imagine a Co-op review platform that goes beyond standard ratings to provide co-op seekers with actionable insights about their potential workplaces. Our app is designed to empower students by offering a comprehensive, data-driven view of internship experiences across industries. While existing platforms like Glassdoor provide general company ratings, they often overlook the unique challenges and expectations of Co-ops. Co-ops frequently face limited access to information on workplace culture, mentorship quality, and skill-building opportunities specific to early-career roles. Our platform closes this gap, giving students and young professionals the detailed guidance they need to make informed choices.
<br><br>
We’re building this app for Co-op seekers who need transparent, authentic information; Co-op reviewers who want to share their experiences; and Northeastern University administrators aiming to gain deeper insights into Co-op companies and student trends. Key features include:
Ratings, Comments, Data visualizations, Company ratings across different industries, Num of former co-ops and reviews, and q&a section for each company.
<br><br>
Our platform provides a much-needed bridge between students and co-ops, helping the next generation of talent find the right place to grow.


## Prerequisites

- A GitHub Account
- A terminal-based or GUI git client
- VSCode with the Python Plugin
- A distrobution of Python running on your laptop (Choco (for Windows), brew (for Macs), miniconda, Anaconda, etc). 

## Project Components

There are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory


### Setting up your repo
1. Once the fork has been created, clone YOUR forked version of the repo to your computer. 
1. Set up the `.env` file in the `api` folder based on the `.env.template` file. Make sure you set a password. 
1. Start the docker containers. 


## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 


## Handling User Role Access and Control

In most applications, when a user logs in, they assume a particular role.  For instance, when one logs in to a stock price prediction app, they may be a single investor, a portfolio manager, or a corporate executive (of a publicly traded company).  Each of those *roles* will likely present some similar features as well as some different features when compared to the other roles. So, how do you accomplish this in Streamlit?  This is sometimes called Role-based Access Control, or **RBAC** for short. 

The code in this project demonstrates how to implement a simple RBAC system in Streamlit but without actually using user authentication (usernames and passwords).  The Streamlit pages from the original template repo are split up among 4 roles - Analyst, Job Reviewer, Job Seeker, and a System Administrator role.

Wrapping your head around this will take a little time and exploration of this code base.  Some highlights are below. 

### Getting Started with the RBAC 
1. We need to turn off the standard panel of links on the left side of the Streamlit app. This is done through the `app/src/.streamlit/config.toml` file.  So check that out. We are turning it off so we can control directly what links are shown. 
1. Then I created a new python module in `app/src/modules/nav.py`.  When you look at the file, you will se that there are functions for basically each page of the application. The `st.sidebar.page_link(...)` adds a single link to the sidebar. We have a separate function for each page so that we can organize the links/pages by role. 
1. Next, check out the `app/src/Home.py` file. Notice that there are 3 buttons added to the page and when one is clicked, it redirects via `st.switch_page(...)` to that Roles Home page in `app/src/pages`.  But before the redirect, I set a few different variables in the Streamlit `session_state` object to track role, first name of the user, and that the user is now authenticated.  
1. Notice near the top of `app/src/Home.py` and all other pages, there is a call to `SideBarLinks(...)` from the `app/src/nav.py` module.  This is the function that will use the role set in `session_state` to determine what links to show the user in the sidebar. 
1. The pages are organized by Role.  Pages that start with a `0` are related to the *Analyst* role.  Pages that start with a `1` are related to the *Job Reviewer* role.  Pages that start with a `2` are related to The *System Admin* role. Pages that start with a `3` are related to The *Job Seeker* role.  
# HokieHunter
CS 4604 WebApp.

Made By Group 7: Alex Ryu, Gibbs Gresge, Harsha Paladugu, Jennifer Chandran, Seung Whoi Kim.

## Index
1. [About](#About)
2. [How To Run](#How-To-Run)
3. [User Guide](#User-Guide)
4. [Developer Guide](#Developer-Guide)

## About


## How To Run
### Prerequisite
1. Python
2. Node.js & npm
3. MySQL
### Guide(Step By Step)
1. Clone the Repository
2. In the terminal, move to the backend directory and install Python dependencies by
> **pip install -r requirements.txt**
3. Run app.py by
> **python app.py**
4. Run another terminal, move to the hokie-hunter directory
5. Install npm by
> **npm install**
6. Start the development server by
> **npm start**

## User Guide
### Registration
* Sign Up
    * Create an account using your email and any password that you want
    * Role must be chosen as either a student or a landlord
      * Students have more specific information required, major, and graduation year
* Login
  * Access the dashboard with your credentials
* Change Password
  * The user can change the password after logging in
* My account
  * Students can add or remove lease transfers, reviews, and favorites
  * Landlords can add or remove property information, safety features, commute information, moving services, or amenities
### Main Menu
* Browse Properties
  * Students can browse which properties are registered in our app and check location, price, or how to contact them
* Lease Transfers
  * Shows active lease requests of students 
* Reviews
  * The user can check the reviews of the properties
* Favorites
  * Users can check the properties that other students have favorited
* Roommate Search
  * Displays profiles of other students looking for roommates
    * You can message directly by the contact information
    * Can check the preferences of the roommates of other students
* Commute Info
  * Shows the distance to the closest bus station to each property
* Moving Services
  * Lists Moving Services that are available locally and their contact information
* Safety Features
  * Shows safety feature information of each property
* Amenities
  * Shows amenities that are in the properties

## Developer Guide
### Setup Guide
We have used **MySQL** to open the server. If you want to use another method, it might require other dependencies. Required Python dependencies are listed in **requirements.txt**.

By running **populatedata.py** in backend/db_test, it gives a basic sample database.
> To run correctly, MySQL must be able to be recognized by the terminal you are using.

### Project Structure
There are two folders, **backend** and **hokie-hunters**, which are each the backend and the frontend of our application.

Backend organizes API endpoints under "backend/routes/", registering them in your Flask app.

Frontend, the **hokie-hunters**, use functional React components and hooks.

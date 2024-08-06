# Django Friend Request API

This project is a Django-based API for managing friend requests. It includes features for user registration, login, searching users, and handling friend requests with rate limiting.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Project](#running-the-project)
4. [API Endpoints](#api-endpoints)


## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (recommended)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Ayush-1205/HandlingRequest.git
   cd HandlingRequest
   
2.Create a Virtual Environment

bash
python -m venv venv
Activate the Virtual Environment

On Windows:

bash
venv\Scripts\activate

3.Install the dependencies:

bash
pip install -r requirements.txt

4.Apply Migrations

bash
python manage.py makemigrations
python manage.py migrate

## Running the project
Run the Development Server

bash
python manage.py runserver

## API Endpoints
1. Sign Up
Endpoint: /api/accounts/signup/
Method: POST
Request Body:
json
{
  "email": "user@example.com",
  "password": "your_password"
}
Description: Registers a new user.
2. Login
Endpoint: /api/accounts/login/
Method: POST
Request Body:
json
{
  "email": "user@example.com",
  "password": "your_password"
}
Description: Authenticates a user and returns a JWT token.
Add this access token in header before accessing any other api
4. Search Users
Endpoint: /api/accounts/search/?keyword= name or email
Method: GET
Query Parameters: keyword
Description: Searches users by email or name with pagination (up to 10 records per page).
5. Send Friend Request
Endpoint: /api/accounts/send_friend_request/
Method: POST
Request Body:
json
{
  "receiver_email": "receiver@example.com"
}
Description: Sends a friend request to the specified email. Users cannot send more than 3 friend requests within a minute.
6. Accept Friend Request
Endpoint: /api/accounts/accept_friend_request/
Method: POST
Request Body:
json
{
  "request_id": 1
}
Description: Accepts a pending friend request.
7. Reject Friend Request
Endpoint: /api/accounts/reject_friend_request/
Method: POST
Request Body:
json
{
  "request_id": 1
}
Description: Rejects a pending friend request.
8. List Friends
Endpoint: /api/accounts/list_friends/
Method: GET
Description: Lists all users who have accepted friend requests.
9. List Pending Friend Requests
Endpoint: /api/accounts/list_pending_friend_requests/
Method: GET
Description: Lists all received pending friend requests with their id's which can be used as request_id for accepting or rejecting the request.

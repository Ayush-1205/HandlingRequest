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

1. Clone the Repository

   git clone https://github.com/Ayush-1205/HandlingRequest.git
   
   cd HandlingRequest
   
3. Create a Virtual Environment

python -m venv venv

Activate the Virtual Environment

On Windows:

venv\Scripts\activate

3. Install the dependencies

pip install -r requirements.txt

4. Apply Migrations

python manage.py makemigrations

python manage.py migrate

## Running the project
Run the Development Server

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

![image](https://github.com/user-attachments/assets/53e35069-89cd-422a-998d-23113cfb8603)


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

![image](https://github.com/user-attachments/assets/8dba5f8f-1d02-4a7d-b1d3-60ff4549c43c)


Add this access token in header before accessing any other api

![image](https://github.com/user-attachments/assets/d0d66c2e-adcd-4cce-a86c-2670ed55f698)


3. Search Users

Endpoint: /api/accounts/search/?keyword= name or email

Method: GET

Query Parameters: keyword

Description: Searches users by email or name with pagination (up to 10 records per page).

![image](https://github.com/user-attachments/assets/4b265373-cc40-478a-aa39-ff5e3c83f69e)

![image](https://github.com/user-attachments/assets/0411f33f-d28e-48d4-94c5-4ae2826da203)


4. Send Friend Request

Endpoint: /api/accounts/send_friend_request/

Method: POST

Request Body:

json

{

  "receiver_email": "receiver@example.com"
}

![image](https://github.com/user-attachments/assets/386a4b54-b428-4e01-be56-7e2a8ebe7255)


Description: Sends a friend request to the specified email. Users cannot send more than 3 friend requests within a minute.

5. Accept Friend Request

Endpoint: /api/accounts/accept_friend_request/

Method: POST

Request Body:

json

{
  "request_id": 1
}

![image](https://github.com/user-attachments/assets/57a1dd2a-c9cc-4abf-8c59-0740c675410c)


Description: Accepts a pending friend request.

6. Reject Friend Request

Endpoint: /api/accounts/reject_friend_request/

Method: POST

Request Body:

json

{

  "request_id": 1
}


Description: Rejects a pending friend request.

7. List Friends

Endpoint: /api/accounts/list_friends/

Method: GET

![image](https://github.com/user-attachments/assets/c421ba51-c29c-4006-80d9-4b955288b124)

Description: Lists all users who have accepted friend requests.

8. List Pending Friend Requests

Endpoint: /api/accounts/list_pending_friend_requests/

Method: GET

![image](https://github.com/user-attachments/assets/556510fb-de63-4164-9f5c-8c629787a24b)


Description: Lists all received pending friend requests with their id's which can be used as request_id for accepting or rejecting the request.

9. Token Refresh Endpoint

Endpoint: /api/token/refresh/

Method: POST

Request Body:

json

{
  "refresh": "your_refresh_token"
}

Description: This endpoint is used to obtain a new access token using a refresh token. The client sends a valid refresh token to this endpoint and receives a new access token.






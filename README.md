# Social Networking API

This is a social networking application API built using Django Rest Framework.

## Freatures
- User signup and login
- Search users by email or name
- Send, accept, and reject friend requests
- List friends
- List pending friend requests
- Rate limiting for friend requests (max 3 requests per minute)


## Getting Started

To get started with using this API, follow the instructions below:

## Installation

### Prerequisites

- Docker
- Docker Compose
### Steps


1. Clone this repository https://github.com/BurhanMohammad/Social-Networking-API.git to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3.   ```sh
        cd social-network-api
     ```
4. Create and activate a virtual environment (optional but recommended):

        ```sh
        python -m venv venv
        source venv/bin/activate  
        ```

5. TO run application locally with Django

        ```sh
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver
        ```

6. To Run the application using Docker Compose:
 
        ```sh
        docker-compose up --build
        ```
7. Apply migrations:

        ```sh
        docker-compose run web python manage.py migrate
        ```

The application will be available at http://localhost:8000.

## API Endpoints

- POST /signup/ - User signup
- POST /login/ - User login
- GET /search_users/ - Search users by name or email
- POST /send_friend_request/ - Send a friend request
- POST /respond_friend_request/<request_id>/ - Accept or reject a friend request
- GET /list_friends/ - List friends
- GET /list_pending_requests/ - List pending friend requests

## Rate Limiting
 Users cannot send more than 3 friend requests per minute.


### Sharing Postman Collection

   For Headers i have shared Bulk edit method and I have also shared postman Collection file please look into it.

1. **Signup**
   - URL: `http://localhost:8000/signup/`
   - Method: `POST`
   - Body: `{"email": "mail@example.com", "password": "admin", "first_name": "burhan", "last_name": "mohammad"}`

2. **Login**
   - URL: `http://localhost:8000/login/`
   - Method: `POST`
   - Body: `{"email": "mail@example.com", "password": "admin"}`

3. **Search Users**
   - URL: `http://localhost:8000/search_users/?q=am`
   - Method: `GET`
   - Headers: 
      ```
      Cookie:<CSRF_token>; sessionid=<session_token>
      X-CSRFToken:<CSRF_token>
      ````

4. **Send Friend Request**
   - URL: `http://localhost:8000/send_friend_request/`
   - Method: `POST`
   - Body: `{"to_user_id": 2}`
   - Headers: 
      ```
      Cookie:<CSRF_token>; sessionid=<session_token>
      X-CSRFToken:<CSRF_token>
      ````

5. **Respond Friend Request**
   - URL: `http://localhost:8000/respond_friend_request/<int:request_id>/`
   - Method: `POST`
   - Body: `{"action": "accept"}`
   - Headers: 
      ```
      Cookie:<CSRF_token>; sessionid=<session_token>
      X-CSRFToken:<CSRF_token>
      ````

6. **List Friends**
   - URL: `http://localhost:8000/list_friends/`
   - Method: `GET`
   - Headers: 
       ```
      Cookie:<CSRF_token>; sessionid=<session_token>
      X-CSRFToken:<CSRF_token>
      ````

7. **List Pending Requests**
   - URL: `http://localhost:8000/list_pending_requests/`
   - Method: `GET`
   - Headers: 
      ```
      Cookie:<CSRF_token>; sessionid=<session_token>
      X-CSRFToken:<CSRF_token>
      ````
---

Please contact me if you face issues while installing or running.




---
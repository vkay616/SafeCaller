# SafeCaller

An API built using Django Rest Framework that allows users to register, log in, and manage their personal contacts. The API provides endpoints for various functionalities like registering a number, logging in as a user, viewing all contacts stored in our API, searching for a contact in our database using name of the contact and reporting a number as spam. For this project, if a contact has more than 10 spam reports, his number is classified as a spam number.

### Installation

1. Install the required libraries

```bash
pip install -r requirements.txt
```

2. Change directory to head inside the safecaller folder
```bash
cd safecaller
```

3. Run migration commands just in case any last minute changes were made to the models.py file
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run the local development server
```bash
python manage.py runserver
```

5. Now you can use cURL commands, any programming language or a tool like Postman to send various requests to the API and get appropriate responses. I have provided a Postman collection to check whether all endpoints work as required or not.


### API Endpoints

##### Open Endpoints
The endpoints that don't require a user to be logged in.

| Endpoint | Detail |
| :---:        |     :---:      |  
| `POST /api/register/`   | registers a user in the db     | 
| `POST /api/login/`   | logs in a user    | 


##### Closed Endpoints
These endpoints require a user to be logged in.

| Endpoint | Detail |
| :---:        |     :---:      |  
| `POST /api/logout/`   | logs out the current logged in user   | 
| `GET /api/contacts/`   | returns all contacts registered and unregistered (personal contacts of registered users) contacts   | 
| `GET /api/contacts/?name=<input>`   | returns all contacts containing the input provided in the name field of contacts   |
| `POST /api/report/`   | reports the number  | 
# UMFlintMobileBackend
Application backend for UM-Flint Mobile App, running on Python and PostgresSQL.

# Running
### Install dependencies
```bash
pip install -r requirements.txt
```

### Add in environment variables
Move ```.env.sample``` ==> ```.env``` and configure your PostgreSQL database settings

### Run
To run the backend, enter: 
```bash
uvicorn main:app
```
and the backend will run the API with concurrency using uvicorn on port 8000.

Adding ```--reload``` will watch for changes to the code and automatically reload.

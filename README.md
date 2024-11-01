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
```bash
uvicorn main:app
```

will run the API with concurrency using uvicorn.

Adding ```--reload``` will watch for changes to the code and automatically reload.

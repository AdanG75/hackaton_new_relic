# Backend Hackaton New Relic

Backend para el hackaton de New Relic

## Correr en un entorno local

    python -m venv venv
    source .venv/bin/activate
    pip install -r requirements.txt

After, create a file .env with the next structure:
    
    MONGO_URI=Your_mongo_uri_connection
    SECRET_KEY=Your_sectret_key

Finally, run via uvicorn:

    uvicorn main:app --reload
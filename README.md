# Backend Hackaton New Relic

Backend para el hackaton de New Relic

## Consumir API

Para consumir la API se tiene como URL base a:
    
    https://hackaton-new-relic.herokuapp.com/

Mientras ls documentación se encuentra en:

    https://hackaton-new-relic.herokuapp.com/docs

## Correr en un entorno local

Genere el entorno virtual e instale las dependencias:

    python -m venv venv
    source .venv/bin/activate
    pip install -r requirements.txt

Posteriormente, ir a core/settings.py y asignar a IS_DEPLOYED como False:

    IS_DEPLOYED: bool = False

## Observabilidad

Para hacer observable la aplicación, se utilizó New Relic ejecutando los 
siguientes pasos:

    pip install newrelic   (no necesario - ya se encuentra en requirements.txt)
    newrelic-admin generate-config your_new_relic_license newrelic.ini   (no necesario - archivo ya generado)
    export NEW_RELIC_CONFIG_FILE=newrelic.ini
    export NEW_RELIC_LICENSE_KEY=your_new_relic_license

A continuación, cree un archivo .env con la siguiente estructura:
    
    MONGO_URI=Your_mongo_uri_connection
    SECRET_KEY=Your_sectret_key
    NEW_RELIC_CONFIG_FILE=newrelic.ini
    NEW_RELIC_LICENSE_KEY=your_new_relic_key

Finalmente, ejecute usando:

    newrelic-admin run-program uvicorn main:app --reload

## Despliegue mediante Heroku

Ir a core/settings.py y asignar a IS_DEPLOYED como True:

    IS_DEPLOYED: bool = True

Luego, se crea un nuevo proyecto en heroku:

    (Desde Heroku CLI)
    heroku create -a your_project_name
    git remote -v (te mostrará los respositorios remotos - uno debe de llamarse heroku-)

Para realizar el despliegue a Heroku primero establesca las variables de entorno dentro del proyecto generado:

    (Desde Heroku CLI)
    heroku config:set NEW_RELIC_APP_NAME=your_heroku_app_name
    heroku config:set NEW_RELIC_CONFIG_FILE=newrelic.ini
    heroku config:set NEW_RELIC_LICENSE_KEY=your_new_relic_key
    heroku config:set NEW_RELIC_LOG=stdout

Por último, ejecutar:

    git push heroku master:master

## Referencias

    https://docs.newrelic.com/docs/apm/agents/python-agent/hosting-services/python-agent-heroku/

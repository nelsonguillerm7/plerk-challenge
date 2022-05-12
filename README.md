# Plerk-challenge
Plerk challenge test [Live Demo](http://plesk.nelsonguillermo.com:8000)

Config pre-commit
-----------------

Pre-commit allows us to execute functions before committing.

Run ``pre-commit install``

Deploy Docker Compose
----------------------

Clone repository and create a copy of the `.env.example` file named `.env` in the directory 
and replace values. Deploy on your server using `docker-compose -f <file> up -d`:

~~~~
docker-compose up -d --build
~~~~


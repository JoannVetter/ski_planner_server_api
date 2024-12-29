# ski_planner_server_api
This repo is a project linked to the ski_planner repository. This is the API that will serve ski planner data.

# How to deploy

Everything is automated so you can run this API easily.
You have to set yourself a .env file that looks like the .env.example. Just make
sure to put strong authentication credentials for mongoDB and to have the correct URI for the API
to be able to connect.

``docker compose build``

``docker compose up -d``

The API and the MongoDB will be running on your machine.
You can check out http://localhost:8000/docs to access the API.

# Troubleshooting

If you docker compose down and do some modification on the database that you
cannot see after another docker compose up, make sure to remove the docker volume
that is persisting data through session (if you change root password for example).

If you're not familiar with docker, the way to do this is by running :


``docker volume ls``

``docker volume rm <the_mongo_db_volume>``

If you get an issue with the database authentication, make sure the format
of the MONGO_CONNECTION_URI is mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@ski-database:27017/ski_planner?authSource=admin


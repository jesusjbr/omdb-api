# omdb-api
This repository contains my solution for a coding exercise

# Prerequisites 
* Docker
* Git client

# Instructions for deployment on Google Cloud
These steps could be automated with Terraform.
You can do most of the next steps through Google cloud console (UI). I'll show the commands relevant
for the process. In a high level we need to create a PostgreSQL 17 database instance,
push a docker image to the google registry and create a container in cloud run.
### Setting the CLI
* Register an account in google cloud.
* Enable 2-Step Verification (2FA)
* Install the gcloud CLI: https://cloud.google.com/sdk/docs/install
* Use IAM roles and apply the least-privilege principle when possible.
* Initializate gcloud: `gcloud init`
* Login with Secure Credentials: `gcloud auth login`
* Set Your Project and Region:
    `gcloud config set project YOUR_PROJECT_ID` \
    `gcloud config set run/region europe-southwest1`
* Enable requires services for database instances:
```commandline
gcloud services enable run.googleapis.com sqladmin.googleapis.com
```
* Create a Cloud SQL Instance (PostgreSQL 17). Pick the smaller instance.
```commandline
gcloud sql instances create INSTANCE_ID \
  --database-version=POSTGRES_17 \
  --edition=ENTERPRISE \
  --cpu=1 --memory=4GB \
  --region=europe-southwest1
```
Where INSTANCE_ID will be the name for your instance.
Wait a moment until this message appears `Creating Cloud SQL instance for POSTGRES_17...done.`
After that take note of the params .
In the instance create a database and a user named `postgres` or create other new.
```commandline
gcloud sql databases create fastapi_db --instance=INSTANCE_ID
gcloud sql users set-password postgres --instance=INSTANCE_ID --password=YOUR_PASSWORD
```
Clone this project and switch to the develop branch \
`git clone https://github.com/jesusjbr/omdb-api.git` \
`git checkout develop`

CD to the project' root folder.
Build and Push the image to GCR (or Artifact Registry):
```commandline
sudo docker build -t gcr.io/YOUR_PROJECT_ID/fastapi-app .
sudo docker push gcr.io/YOUR_PROJECT_ID/fastapi-app
```
If you have problems for the push part use
gcloud auth configure-docker

Now connect to the database and execute the SQL script `scripts/database_creation.sql` \

Last but not least deploy to cloud run:
```commandline
gcloud run deploy app-remaster \
  --image gcr.io/YOUR_PROJECT_ID/fastapi-app \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances YOUR_PROJECT_ID:YOUR_REGION:INSTANCE_ID \
  --set-env-vars="DATABASE_USER=postgres,DATABASE_PASSWORD=YOUR_PASSWORD,DATABASE_NAME=fastapi_db,DATABASE_ENDPOINT=YOUR_PROJECT_ID:YOUR_REGION:INSTANCE_ID,DATABASE_PORT=5432,OMDB_API_KEY=YOUROMDBAPIKEY,DEPLOY_ENVIRON=GOOGLE"
```

This will provide you with a URL visit it and add /docs to use the swagger and test the app.

# Steps to execute in local
Replace the data with your own.\
Most of these steps could be automated using docker compose. \
\
Create network \
`sudo docker network create app-network`

Create a database container
```commandline
sudo docker run -d --name pg-db -p 5433:5432 --network app-network\
    -e POSTGRES_DB=mydatabase \
    -e POSTGRES_USER=myuser \
    -e POSTGRES_PASSWORD=mypassword \
    postgres:17-alpine
```

Clone this project and switch to the develop branch \
`git clone https://github.com/jesusjbr/omdb-api.git` \
`git checkout develop`

Connect to the database and execute the following SQL script:
`omdb-api/scripts/database_creation.sql`

Change directory to this project folder.
Build docker image from Dockerfile \
`sudo docker build -t omdb-api-app-image .`

Start the container
```commandline
sudo docker run -d --name app-container-uv --network app-network \
    -p 80:80 \
    -e DATABASE_ENDPOINT="pg-db" \
    -e DATABASE_PORT="5432" \
    -e DATABASE_USER="myuser" \
    -e DATABASE_PASSWORD="mypassword" \
    -e OMDB_API_KEY="XXXXXXX" \
    -e DATABASE_NAME="mydatabase" \
    omdb-api-app-image
```

If you don't have other things up and running:
Visit http://localhost:80/docs or http://127.0.0.1:80/docs and use the swagger.


# How to use
At startup the app creates a couple of dummy users to test the app. \
In this startup the initial movies are fetched and inserted. \
The users are required since I didn't implement an endpoint to register or create new users.
In case that something goes wrong you need to execute the SQL script that will clean and create
again the tables. After that restart the app container.

USERS FOR TESTING THE APP:
DEMO USER
```json
{
  "username": "demo_user",
  "password": "1234"
}
```

ADMIN USER
```json
{
  "username": "admin_user",
  "password": "12345"
}
```
Every endpoint requires authentication. The delete endpoint besides requires to have the admin role
thus only the admin user has access to it.

Go to the login endpoint in the swagger and use this data to generate a token.
Use that token value to fill the Authorize field in the top right corner. 
If you are using any http client instead add it to a `Authorization: token` header.

# Personal decisions
I decided to add the filter to get movies by title in the endpoint that retrieve multiple films
since in the reality more than one film can and have the same title.

# Improvements
* Add more metadata to prettify the autogenerated swagger/openapi in /docs.
* Add more tests.
* There is a default secret key to encode and decode jwt is hardcoded in the config but you can 
provide it as env param. 
* In a real world scenario I would have added endpoint to create and manage users and not "hardcode"
them.
* In a real world scenario I would have set up a proper CI/CD pipeline to enforce the execution of
tests and other steps. Automating fully the deployment.

# End
Thanks, leave me your comments.

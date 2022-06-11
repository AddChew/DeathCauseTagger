## Death Cause Tagger

### How to run the project via Docker

1.  Clone project branch
```sh
git clone -branch docker https://github.com/AddChew/DeathCauseTagger.git
```

2. Navigate into project folder
```sh
cd DeathCauseTagger
```

3. Build docker image
```sh
sudo docker-compose run web
```

4. Run docker container
```sh
docker-compose up
```

5. Migrate database and create super user
- Execute the following commands in a different shell
```sh
# Step 1: Get CONTAINER_ID of the web application
docker ps # i.e. 358d875f1267

# Step 2: Log in into the container for the web application
docker exec -t -i <CONTAINER_ID> bash # i.e. docker exec -t -i 358d875f1267 bash

# Step 3: Perform database migration
python3 manage.py makemigrations tagger
python3 manage.py migrate

# Step 4: Create super user
python3 manage.py createsuperuser

# Step 5: Exit container
Ctrl-D
```
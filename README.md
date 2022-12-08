# Death Cause Tagger

Web Application for the tagging of death causes to their respective ICD10 codes.

### How to run the project

1. Clone the project
```sh
git clone -branch develop https://github.com/AddChew/DeathCauseTagger.git
```

2. Navigate into project folder
```sh
cd DeathCauseTagger
```

3. Build docker image
```sh
docker-compose build

# Alternatively, can run the command below which performs both steps 3 and 4.
# docker-compose up -d --build
```

4. Spin up the docker containers
```sh
docker-compose up -d
```

### Useful Commands

1. Command to view docker logs
```sh
docker-compose logs -f
```

2. Command to enter the shell of a specific container that is up and running
```sh
# for example
# docker-compose exec web bash
docker-compose exec <service-name> bash

# Use Ctrl-D to exit the container
```

3. Command to shutdown active docker containers
```sh
docker-compose down
```
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

4. Commands to clean up resources (i.e. images, containers, volumes and networks)
```sh
# Command to clean up all dangling resources
docker system prune

# Command to clean up all resources
docker system prune -a

# Command to list all images
docker images -a

# Command to remove specific images
docker rmi <image1> <image2>

# Command to list all containers
docker ps -a

# Command to remove specific containers
docker rm <id or name of container 1> <id or name of container 2>

# Command to list all volumes
docker volume ls

# Command to remove specific volumes
docker volume rm <volume name 1> <volume name 2>

# Command to list all dangling volumes
docker volume ls -f dangling=true

# Command to remove all volumes
docker volume prune
```
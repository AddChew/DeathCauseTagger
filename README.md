## Death Cause Tagger

### Installation instructions

1.  Clone project branch
```sh
git clone -branch conda-postgres https://github.com/AddChew/DeathCauseTagger.git
```

2. Navigate into project folder
```sh
cd DeathCauseTagger
```

3. Create conda environment
```sh
conda create -y --name conda-postgres python=3.7
```

4. Activate conda environment
```sh
conda activate conda-postgres
```

5. Install the necessary dependencies
```sh
conda install -y -c conda-forge --file requirements.txt
pip install -r requirements_pip.txt
```

6. Initialise base database
```sh
initdb -D postgres
```

7. Start database server
```sh
pg_ctl -D postgres -l logfile start
```

8. Create database superuser

```sh
createuser --encrypted --pwprompt <your username>
```

10. Create project database
```sh
createdb --owner=<your username> deathcauses
```

11. Set database user username and password as environment variables
```sh
# Set username as environment variable
conda env config vars set POSTGRES_USER=<your username>
conda activate conda-postgres

# Set password as environment variable
conda env config vars set POSTGRES_PASSWORD=<your password>
conda activate conda-postgres
```

12. Migrate database
```sh
python manage.py makemigrations
python manage.py migrate
```

13. Create superuser
```sh
python manage.py createsuperuser
```

14. Start the app
```sh
python manage.py runserver
```

15. Navigate and login into the admin page to upload the fixtures for populating the database.

### Usage instructions

1. Execute the following command to stop the database server when you no longer need it
```sh
pg_ctl -D postgres -l logfile stop
```

### Postgres Exporter

1. Create env file (i.e. postgres_exporter.env) for postgres exporter where we will store our environment variables.
```sh
# postgres_exporter.env
DATA_SOURCE_NAME="postgresql://<your username>:<your password>@localhost:5432/<your db name>?sslmode=disable"
```

1. Set postgres url as environment variable
```sh
# In our case, the db name is deathcauses
# conda env config vars set PG_EXPORTER_URL="postgres://<your username>:<your password>@localhost:5432/deathcauses
conda env config vars set PG_EXPORTER_URL="postgres://<your username>:<your password>@localhost:5432/<your db name>"
```

2. Start database server
```sh
pg_ctl -D postgres -l logfile start
```

3. Start pg_exporter
```sh
./pg_exporter
```

4. Kill pg_exporter process
```sh
# Get PID
sudo netstat -nlp | grep :9630

# Kill pg_exporter process
sudo kill <PID>
```

### Postgres Extensions (this part might not be necessary)

1. List installed postgres extensions
```
psql
\dx
```

- Install postgres extension
``
psql
CREATE EXTENSION IF NOT EXISTS <extension name>
``

### How to rollback migrations
Rollback to specific migration
```sh
# python manage.py migrate tagger 0004
# python manage.py migrate tagger 0004_mapping_tagger_mapp_search__3cf9c6_gin
python manage.py migrate tagger <migration number or name>
```

Rollback all migrations
```sh
python manage.py migrate tagger zero
```

### How to connect to postgres db as another user
```sh
psql -d <database name> -U <your username>
```
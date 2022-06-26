## Death Cause Tagger

### Installation instructions

1.  Clone project branch
```sh
git clone -branch docker https://github.com/AddChew/DeathCauseTagger.git
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

8. Create project database
```sh
createdb
createdb deathcauses
```

9. Create database user
```sh
psql -c "CREATE USER <your username> with PASSWORD '<your password>';"
```

10. Set database user username and password as environment variables
```sh
# Set username as environment variable
conda env config vars set POSTGRES_USER=<your username>
conda activate conda-postgres

# Set password as environment variable
conda env config vars set POSTGRES_PASSWORD=<your password>
conda activate conda-postgres
```

11. Migrate database
```sh
python manage.py makemigrations tagger
python manage.py migrate
```

12. Create superuser
```sh
python manage.py createsuperuser
```

13. Start the app
```sh
python manage.py runserver
```

14. Navigate and login into the admin page to upload the fixtures for populating the database.

### Usage instructions

1. Execute the following command to stop the database server when you no longer need it
```sh
pg_ctl -D postgres -l logfile stop
```
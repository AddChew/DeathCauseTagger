## Death Cause Tagger

### How to run the project

1.  Clone project branch
```
git clone -branch docker https://github.com/AddChew/DeathCauseTagger.git
```

2. Navigate into project folder
```
cd DeathCauseTagger
```

3. Install the required dependencies
```
pip3 install -r requirements.txt
```

4. Migrate database
```
python3 manage.py makemigrations tagger
python3 manage.py migrate
```

5. Start web server
```
python3 manage.py runserver
```
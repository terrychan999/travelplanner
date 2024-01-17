# travelplanner

system requirement:
Python > 3.9

install deps:
```
pip install -r requirements.txt
```

init db:
```
cd backend
python -c "from app import db; db.create_all()"
```

run:
```
cd backend
python app.py
```

if wants to check the content of sqlite:
https://inloop.github.io/sqlite-viewer/
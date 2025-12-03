API RESTful (Flask + SQLAlchemy)

Endpoints:
- GET /books
- GET /books/<id>
- POST /books
- PUT /books/<id>
- DELETE /books/<id>

Run locally:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. export FLASK_APP=app.py
5. flask run --host=0.0.0.0 --port=5001

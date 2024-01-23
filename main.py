from facial_recognition.database import db

if __name__ == "__main__":
    print(db.insert({"name": "John", "age": 30}))

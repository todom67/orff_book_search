from app import app, db  
import admin
import models 
import views 

from books.blueprint import books
app.register_blueprint(books, url_prefix='/books')

if __name__ == "__main__":
    print("In main")
    app.run(port=8000)

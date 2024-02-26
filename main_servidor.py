from fastapi import FastAPI,Query,HTTPException
from pydantic import BaseModel
import uvicorn, socket,json

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

app = FastAPI()

class Book(BaseModel):
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int

with open ('books.json','r') as file:
    books = json.load(file)    
   
@app.get("/api/v1/books",status_code=200)
def get_books()->list:   
    if (len(books)>0):
        return books
    else:
        raise HTTPException(
            status_code=404,
            detail=f'There is no books'
        )

@app.get("/api/v1/books/search",status_code=200)
def search_books_author(author:str=Query(title='author',description='Looking up books by author'))->list:
    books_by_author = []
    for book in books:
        if (book["author"] == author):
            books_by_author.append(book)    
    if (len(books_by_author) > 0):
        return books_by_author
    else:
        raise HTTPException(status_code=404,detail=f'There is no book with {author} as author') 

@app.get("/api/v1/books/{title}")
def get_book_title(title:str)->dict:
    for book in books:
        if (book["title"] == title):
            return book
    raise HTTPException(status_code=404,detail=f'There is no book with {title} as title')        

@app.post("/api/v1/books",status_code=201)
def create_book(book:Book)->dict:
    new_book={
        "author": book.author,
        "country": book.country,
        "imageLink": book.imageLink,
        "language": book.language,
        "link": book.link,
        "pages": book.pages,
        "title": book.title,
        "year": book.year
    }
    books.append(new_book)
    with open("books.json",'w') as file:
        json.dump(books,file)
    return new_book

@app.put('/api/v1/books/{title}',status_code=200)
def update_book(title:str,book_updated:Book):
    for book in books:
        if (book['title'] == title):
            book["author"] = book_updated.author
            book["country"] = book_updated.country
            book["imageLink"] = book_updated.imageLink
            book["language"] = book_updated.language
            book["link"] = book_updated.link
            book["pages"] = book_updated.pages
            book["title"] = book_updated.title
            book["year"] = book_updated.year
            with open("books.json",'w') as file:
                json.dump(books,file)
            return book_updated    
    raise HTTPException(status_code=404,detail=f'There is no book with {title} as title') 

@app.delete('/api/v1/books/{title}',status_code=200)
def delete_book(title:str)->dict:
    for book in books:
        if (book['title'] == title):    
            books.remove(book)
            with open("books.json",'w') as file:
                json.dump(books,file)
            return {
                "message":"Book deleted"
            } 
    raise HTTPException(status_code=404,detail=f'There is no book with {title} as title')    

if __name__ == "__main__":
    print(f"La dirección IP de este servidor es {IPAddr}. Esta dirección va a ser solicitada por el programa del cliente")
    uvicorn.run("main_servidor:app", port=80, log_level="info",host=IPAddr)


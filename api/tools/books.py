import sqlite3
from flask import render_template,request



class Book:

    con=sqlite3.connect('Mahagony.db', check_same_thread=False)   
    cur = con.cursor()

    try:
        cur.execute('''CREATE TABLE Books (ID int,name text,author text,yearpublished int,type int,loanstatus text,unique (ID))''')
    except:
        print("table already created")
    else:
        print("table created sucessfuly")

    # def __init__(self,bookid,bookname,bookauthor,yearpublished,booktype):
    #     self.bookid=bookid
    #     self.bookname=bookname
    #     self.bookauthor=bookauthor
    #     self.yearpublished=yearpublished
    #     self.booktype=booktype   

    def showAllBooks(self):
        # if request.method=='POST':
        #     pass
        self.cur.execute("SELECT * FROM Books")
        books = self.cur.fetchall()
        return render_template("/books/showAllBooks.html", books=books)

    def addBook(self):
                msg=[]
                if request.method=='POST':
                    self.bookid=request.form.get('id')
                    self.bookname =request.form.get('name')
                    self.author = request.form.get('author')
                    self.yearpublished = request.form.get('yearpublished')
                    self.type = request.form.get('type')
                    try:
                        self.cur.execute("INSERT INTO Books (ID,name,author,yearpublished,type) VALUES (?,?,?,?,?)",((self.bookid,self.bookname,self.author,self.yearpublished,self.type)))
                        self.cur.execute(f'''UPDATE Books SET loanstatus = 'Available'  WHERE ID={self.bookid}''')
                        self.con.commit()
                    except:
                        msg="book already exists" 
                    else:
                        msg="book added"    
                return render_template("/books/addBook.html",msg=msg)

    def removeBook(self):
        msg=[]
        if request.method=='POST':
                self.bookid=request.form.get("ID")
                for row in self.cur.execute(f'''SELECT loanstatus from Books WHERE ID={self.bookid} '''):
                    loanstatus=row[0]
                    if(loanstatus == "Available"):
                        self.cur.execute(f"DELETE FROM Books where ID={self.bookid}")
                        self.con.commit()
                        msg="The book was removed from the library"
                    else:
                        msg="This book cannot be deleted! it is loaned to a customer"
                return render_template("/books/removeBook.html", msg=msg)
        return render_template("/books/removeBook.html",msg=msg)

    def findBook(self):
        if request.method=='POST':
            bookName = request.form.get('bookName')
            self.cur.execute(f'''select * from Books where name like "%{bookName}%"''')
            books = self.cur.fetchall()
            return render_template("/books/findBook.html", books=books)
        return render_template("/books/findBook.html")


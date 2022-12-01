from tkinter import *
import psycopg2
from datetime import timedelta, date

# global var: member_id1, username1, global bookName, bookIsbn, bookAuthor, bookGenre

def findBookByAuthor():
    labels = []
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set frame
    root=Toplevel(screen)
    root.geometry('500x500')
    #
    # J.R.R Tolkein
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    index = 0
    for title, isbn, author, genre in cur:
        if bookAuthor.get() == author :
            #set labels
            label1 = Label(root, text='Author: ' + author)
            label1.place(x = 100, y = 80)
            labels.append(Label(root, text='book title: ' + title))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='book isbn: ' + isbn))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='book genre: ' + genre))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='------------------------'))
            labels[index].place(x=100, y=130+index*30)
            index += 1

def findBookByGenre():
    labels = []
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set frame
    root=Toplevel(screen)
    root.geometry('500x500')
    #
    # Fantasy
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    index = 0
    for title, isbn, author, genre in cur:
        if bookGenre.get() == genre :
            #set labels
            label1 = Label(root, text='genre: ' + genre)
            label1.place(x = 100, y = 80)
            labels.append(Label(root, text='book title: ' + title))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='book isbn: ' + isbn))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='book author: ' + author))
            labels[index].place(x=100, y=130+index*30)
            index += 1
            labels.append(Label(root, text='------------------------'))
            labels[index].place(x=100, y=130+index*30)
            index += 1


def findBookByIsbn():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    def borrowBook(isbn):
        cur.execute("select * from copy where isbn = '" + isbn + "'")
        flag = 0
        for copy_number, availability, isbn in cur:
            if availability == True:
                cur.execute(f"UPDATE copy SET availability = False WHERE isbn = '{isbn}' and copy_number = {copy_number}")

                # update the borrowed table
                borrowDate = date.today()
                dueDate = borrowDate + timedelta(days=10)
                cur.execute(f"insert into borrowed(issue_date, due_date, copy_number, isbn, member_id) values ('{borrowDate}', '{dueDate}', {copy_number}, '{isbn}', {member_id1})")
                conn.commit()
                flag = 1
                lable5 = Label(root, text='Successfully borrowed')
                lable5.place(x=100, y=350)
                print(username1.get() + ' borrow ' + isbn)
                break
        if flag == 0:
            lable6 = Label(root, text='No available copy, try again next time')
            lable6.place(x=100, y=350)

    #set frame
    root=Toplevel(screen)
    root.geometry('500x500')
    #
    # 9780358380245
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    for title, isbn, author, genre in cur:
        if bookIsbn.get() == isbn :
            #set labels
            lable1 = Label(root, text='book title: ' + title)
            lable1.place(x=100, y=100)
            lable2 = Label(root, text='book isbn: ' + isbn)
            lable2.place(x=100, y=150)
            lable3 = Label(root, text='book author: ' + author)
            lable3.place(x=100, y=200)
            lable4 = Label(root, text='book genre: ' + genre)
            lable4.place(x=100, y=250)
            break
            
    #set buttons
    button1 = Button(root, text="Borrow",padx=50, command=lambda: borrowBook(isbn))
    button1.place(x=100, y=300) 

def findBookByTitle():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    def borrowBook(isbn):
        cur.execute("select * from copy where isbn = '" + isbn + "'")
        flag = 0
        for copy_number, availability, isbn in cur:
            if availability == True:
                cur.execute(f"UPDATE copy SET availability = False WHERE isbn = '{isbn}' and copy_number = {copy_number}")

                # update the borrowed table
                borrowDate = date.today()
                dueDate = borrowDate + timedelta(days=10)
                cur.execute(f"insert into borrowed(issue_date, due_date, copy_number, isbn, member_id) values ('{borrowDate}', '{dueDate}', {copy_number}, '{isbn}', {member_id1})")
                conn.commit()
                flag = 1
                lable5 = Label(root, text='Successfully borrowed')
                lable5.place(x=100, y=350)
                print(username1.get() + ' borrow ' + isbn)
                break
        if flag == 0:
            lable6 = Label(root, text='No available copy, try again next time')
            lable6.place(x=100, y=350)

    #set frame
    root=Toplevel(screen)
    root.geometry('500x500')
    #
    # The Fellowship of the Ring
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    for title, isbn, author, genre in cur:
        if bookName.get() == title :
            #set labels
            lable1 = Label(root, text='book title: ' + title)
            lable1.place(x=100, y=100)
            lable2 = Label(root, text='book isbn: ' + isbn)
            lable2.place(x=100, y=150)
            lable3 = Label(root, text='book author: ' + author)
            lable3.place(x=100, y=200)
            lable4 = Label(root, text='book genre: ' + genre)
            lable4.place(x=100, y=250)
            break
            
    #set buttons
    button1 = Button(root, text="Borrow",padx=50, command=lambda: borrowBook(isbn))
    button1.place(x=100, y=300)       
    

def memberSearch():
    global bookName
    global bookIsbn
    global bookAuthor
    global bookGenre

    #set frame
    root=Toplevel(screen)
    root.geometry('500x500')
    #set label
    lable1 = Label(root, text='enter book title')
    lable1.place(x=70, y=50)
    lable2 = Label(root, text='enter book isbn')
    lable2.place(x=70, y=100)
    lable3 = Label(root, text='enter book genre')
    lable3.place(x=70, y=150)
    lable4 = Label(root, text='enter book author')
    lable4.place(x=70, y=200)
    #set textfiled
    bookName = StringVar()
    bookIsbn = StringVar()
    bookGenre = StringVar()
    bookAuthor = StringVar()
    bookNameInput = Entry(root, textvariable=bookName, width=20)
    bookNameInput.place(x=200, y=50)
    bookIsbnInput = Entry(root, textvariable=bookIsbn, width=20)
    bookIsbnInput.place(x=200, y=100)
    bookGenreInput = Entry(root, textvariable=bookGenre, width=20)
    bookGenreInput.place(x=200, y=150)
    bookAuthorInput = Entry(root, textvariable=bookAuthor, width=20)
    bookAuthorInput.place(x=200, y=200)
    #set button
    button1 = Button(root, text="search",padx=50, command=findBookByTitle)
    button1.place(x=100, y=75)
    button1 = Button(root, text="search",padx=50, command=findBookByIsbn)
    button1.place(x=100, y=125)
    button1 = Button(root, text="search",padx=50, command=findBookByGenre)
    button1.place(x=100, y=175)
    button1 = Button(root, text="search",padx=50, command=findBookByAuthor)
    button1.place(x=100, y=225)



def selectionScreen():
    global member_id1
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute('SELECT username, password FROM admin_login')
    for username, password in cur:
        if username1.get() == username and password1.get() == password:
            root=Toplevel(screen)
            root.geometry('500x500')
            lable0 = Label(root, text='admin page')
            lable0.place(x=30, y=50)
            lable1 = Label(root, text=username1.get())
            lable1.place(x=70, y=100)
            lable2 = Label(root, text=password1.get())
            lable2.place(x=70, y=150)
            break

    cur.execute('SELECT username, password, member_id mem FROM member_login')
    for username, password, member_id in cur:
        if username1.get() == username and password1.get() == password:
            root=Toplevel(screen)
            root.geometry('500x500')
            button1 = Button(root, text="search book",padx=50, command=memberSearch)
            button1.place(x=70, y=100)
            button1 = Button(root, text="return book",padx=50)
            button1.place(x=70, y=150)
            member_id1 = member_id
            break
            

def loginScreen():
    global username1
    global password1
    global screen

    screen = Tk()
    screen.geometry('500x500')

    #label
    lable1 = Label(text='username')
    lable1.place(x=70, y=100)
    lable2 = Label(text='password')
    lable2.place(x=70, y=150)

    #textfiled
    username1=StringVar()
    password1=StringVar()
    usernameInput = Entry(textvariable=username1, width=12)
    passwordInput = Entry(textvariable=password1, width=12)
    usernameInput.place(x=150, y=100)
    passwordInput.place(x=150, y=150)

    #button
    button = Button( text="login",padx=50, command=selectionScreen)
    button.place(x=200, y=200)


    screen.mainloop()



loginScreen()
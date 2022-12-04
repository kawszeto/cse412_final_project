from tkinter import *
import psycopg2
from datetime import timedelta, date
from tkinter import ttk

# global var: member_id1, username1, global bookName, bookIsbn, bookAuthor, bookGenre
# member_id2, bookIsbn2

# 0743477103
# 1 2


# admin part
def deleteBooks():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    def deleteBook():
        cur.execute(f"select count(copy_number) as count from copy where isbn = '{deleteIsbn.get()}'")
        for count in cur:
            if count[0] == 0:
                cur.execute(f"DELETE FROM books WHERE isbn = '{deleteIsbn.get()}'")
                conn.commit()
                Label(root, text="This book has been deleted").place(x=100, y=120)
            else:
                Label(root, text="Still have copies").place(x=100, y=120)
        
    def deleteCopy():
        cur.execute(f"select * from copy where isbn = '{deleteIsbn.get()}' and copy_number = {deleteCopyNumber.get()}")
        for row in cur:
            if row[1] == True:
                cur.execute(f"DELETE FROM borrowed WHERE isbn = '{deleteIsbn.get()}' and copy_number = {deleteCopyNumber.get()}")
                cur.execute(f"DELETE FROM returned WHERE isbn = '{deleteIsbn.get()}' and copy_number = {deleteCopyNumber.get()}")
                cur.execute(f"DELETE FROM copy WHERE isbn = '{deleteIsbn.get()}' and copy_number = {deleteCopyNumber.get()}")
                conn.commit()
                Label(root, text="This copy has been deleted").place(x=100, y=230)
            else:
                Label(root, text="This copy is borrowed by the member").place(x=100, y=230)

    #set frame
    root=Toplevel(screen)
    root.geometry('400x300')
    root.title('Delete Book')

    #set delete book
    lable1 = Label(root, text='enter book isbn')
    lable1.place(x=70, y=50)
    deleteIsbn = StringVar()
    Entry(root, textvariable=deleteIsbn).place(x=200, y=50)
    Button(root, text="Delete book", command=deleteBook).place(x=100, y=100)

    #set delete copy
    deleteCopyNumber = IntVar()
    Label(root, text='enter copy number').place(x=70, y=150)
    Entry(root, textvariable=deleteCopyNumber).place(x=200, y=150)
    Button(root, text="Delete copy", command=deleteCopy).place(x=100, y=200)

def addBooks():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    def add():
        #insert book
        cur.execute(f"insert into books(title, isbn, author, publisher, genre) values('{newBookName.get()}', '{newBookIsbn.get()}', '{newBookGenre.get()}', '{newBookAuthor.get()}', '{newBookPublisher.get()}')")
        print("book added")
        conn.commit()

    def addCopies():
        for index in range(numberOfCopies.get()):
            cur.execute(f"insert into copy(copy_number, availability, isbn) values ({index+1}, true, '{newBookIsbn.get()}')")
            print(f'{index+1} add successfully')
        conn.commit()
        
    #set frame
    root=Toplevel(screen)
    root.geometry('800x600')
    root.title('Add Book')

    #set label
    lable1 = Label(root, text='enter book title')
    lable1.place(x=70, y=50)
    lable2 = Label(root, text='enter book isbn')
    lable2.place(x=70, y=100)
    lable3 = Label(root, text='enter book genre')
    lable3.place(x=70, y=150)
    lable4 = Label(root, text='enter book author')
    lable4.place(x=70, y=200)
    lable5 = Label(root, text='enter book Publisher')
    lable5.place(x=70, y=250)
    
    #set textfiled
    newBookName = StringVar()
    newBookIsbn = StringVar()
    newBookGenre = StringVar()
    newBookAuthor = StringVar()
    newBookPublisher = StringVar()
    bookNameInput = Entry(root, textvariable=newBookName, width=20)
    bookNameInput.place(x=200, y=50)
    bookIsbnInput = Entry(root, textvariable=newBookIsbn, width=20)
    bookIsbnInput.place(x=200, y=100)
    bookGenreInput = Entry(root, textvariable=newBookGenre, width=20)
    bookGenreInput.place(x=200, y=150)
    bookAuthorInput = Entry(root, textvariable=newBookAuthor, width=20)
    bookAuthorInput.place(x=200, y=200)
    bookAuthorInput = Entry(root, textvariable=newBookPublisher, width=20)
    bookAuthorInput.place(x=200, y=250)
    Button(root, text="Add Book", command=add).place(x=100, y=300)

    lable6 = Label(root, text='enter number of copies')
    lable6.place(x=70, y=350)
    numberOfCopies = IntVar()
    Entry(root, textvariable=numberOfCopies, width=20).place(x=230, y=350)
    Button(root, text="Add Copy", command=addCopies).place(x=100, y=400)

def manageBookByIsbn():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set frame
    root=Toplevel(screen)
    root.geometry('400x200')
    root.title('Manage Books')

    def returnBook(isbn, copy_number, member_id):
        print(isbn)
        print(copy_number)
        print(member_id)
        #update the borrowed table
        cur.execute(f"UPDATE copy SET availability = True WHERE isbn = '{isbn}' and copy_number = {copy_number}")
        #update the returned table
        returnDate = date.today()
        cur.execute(f"insert into returned(return_date, copy_number, isbn, member_id) values ('{returnDate}', {copy_number}, '{isbn}', {member_id})")
        conn.commit()
        print("succeesfully returned")

    rowNum = 0
    cur.execute(f"select distinct borrowed.copy_number, borrowed.member_id, borrowed.due_date from borrowed, copy where borrowed.isbn = '{bookIsbn2.get()}' and copy.availability = false and copy.isbn = borrowed.isbn")
    for copy_number, member_id, due_date in cur:
        Label(root, text=f"copy {copy_number} of {bookIsbn2.get()} borrowed by member {member_id} will due on {due_date}").grid(row=rowNum, column=0)
        rowNum +=1
        Button(root, text="mark as return", command=lambda copy_number=copy_number, member_id=member_id: returnBook(isbn=bookIsbn2.get(), copy_number=copy_number, member_id=member_id)).grid(row=rowNum, column=0)
        rowNum += 1
   
            

def findMemberById():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('600x600')
    root.title('Member info')

    def returnBook(isbn, copy_number):
        #update the borrowed table
        cur.execute(f"UPDATE copy SET availability = True WHERE isbn = '{isbn}' and copy_number = {copy_number}")
        #update the returned table
        returnDate = date.today()
        cur.execute(f"insert into returned(return_date, copy_number, isbn, member_id) values ('{returnDate}', {copy_number}, '{isbn}', {member_id2.get()})")
        conn.commit()
        print("succeesfully returned")
        

    # set labels
    rowNum = 0
    cur.execute(f"select DISTINCT copy.copy_number, copy.isbn from borrowed, copy where copy.isbn = borrowed.isbn and copy.availability = false and borrowed.member_id = {member_id2.get()}")
    for copy_number, isbn in cur:
        Label(root, text=f"copy {copy_number} of {isbn} borrowed by member {member_id2.get()} hasn't been returned").grid(row=rowNum, column=0)
        rowNum += 1
        Button(root, text="Mark as returned", command=lambda isbn=isbn, copy_number=copy_number: returnBook(isbn=isbn, copy_number=copy_number)).grid(row=rowNum, column=0)
        rowNum += 1
    
def memberInfo():
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    root=Toplevel(screen)
    root.geometry('400x600')
    root.title('Member info')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    rowNum = 0
    cur.execute('SELECT member_id, name, address, email, phone FROM Member')
    for member_id, name, address, email, phone in cur:
            Label(second_frame, text=f'Member ID: {member_id}\nName: {name}\nAddress: {address}\nEmail: {email}\nPhone: {phone}').grid(row=rowNum, column=0)
            rowNum += 1

def checkMembers():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('750x600')
    root.title('Transactions')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    # set labels
    cur.execute("select borrowed.copy_number as copy_number, borrowed.due_date as due_date, member.member_id as member_id, member.name as name, books.title as title from member, borrowed, books where member.member_id = borrowed.member_id and books.isbn = borrowed.isbn")
    rowNum = 0
    for copy_number, due_date, member_id, name, title in cur:
        Label(second_frame, text=f'{name} member id: {member_id} borrowed {title} (copy {copy_number}) which dues on {due_date}').grid(row=rowNum, column=0)
        rowNum+=1

def checkBooks():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('600x600')
    root.title('Book info')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    # set labels
    cur.execute("select books.title as title, books.isbn as isbn, copy.copy_number as copy_number, copy.availability as availability from books, copy where books.isbn = copy.isbn")
    rowNum = 0
    for title, isbn, copy_number, availability in cur:
        Label(second_frame, text=f'{title} {isbn} copy number: {copy_number} availability: {availability}').grid(row=rowNum, column=0)
        rowNum+=1

# member part
def memberReturn():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    
    def returnBook(isbn, copy_number):
        returnIsbnStr = isbn.get()
        copyNumStr = copy_number.get()
        #update the borrowed table
        cur.execute(f"UPDATE copy SET availability = True WHERE isbn = '{returnIsbnStr}' and copy_number = {copyNumStr}")
        #update the returned table
        returnDate = date.today()
        cur.execute(f"insert into returned(return_date, copy_number, isbn, member_id) values ('{returnDate}', {copyNumStr}, '{returnIsbnStr}', {member_id1})")
        conn.commit()
        print("succeesfully returned")
        

    #set frame
    root=Toplevel(screen)
    root.geometry('600x600')
    root.title('Return book')
    #
    # 9780358380245
    # 1
    #
    #set label
    lable1 = Label(root, text="Enter the book's isbn you want to return: ")
    lable1.place(x=50, y=100)
    lable2 = Label(root, text="Enter the book's borrow date you want to return: ")
    lable2.place(x=50, y=150)
    lable3 = Label(root, text="Enter the book's copy number you want to return: ")
    lable3.place(x=50, y=200)
    #set textfield
    returnIsbn = StringVar()
    borrowDate = StringVar()
    copyNum = StringVar()
    isbnInput = Entry(root, textvariable=returnIsbn, width=12)
    isbnInput.place(x=300, y=100)
    dateInput = Entry(root,textvariable=borrowDate, width=12)
    dateInput.place(x=300, y=150)
    copyInput = Entry(root,textvariable=copyNum, width=12)
    copyInput.place(x=300, y=200)
    #set button
    button = Button(root, text="return",padx=50, command= lambda: returnBook(isbn=returnIsbn, copy_number=copyNum))
    button.place(x=200, y=250)
    
def findBookByAuthor():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('300x400')
    root.title('Book search')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    #
    # J.R.R Tolkein
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    index = 0
    for title, isbn, author, genre in cur:
        if bookAuthor.get() == author :
            #set labels
            Label(second_frame, text='Author: ' + author).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book title: ' + title).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book isbn: ' + isbn).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book genre: ' + genre).grid(row=index, column=0)
            index +=1
            Button(second_frame, text="borrow").grid(row=index, column=0)
            index +=1

def findBookByGenre():
    #set query
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('300x400')
    root.title('Book search')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    def borrowBook1(isbn):
        print(isbn)
        cur.execute(f"select * from copy where isbn = '{isbn}'")
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
                Label(second_frame, text='Successfully borrowed').grid(row=0, column=0)
                print(username1.get() + ' borrow ' + isbn)
                break
        if flag == 0:
            Label(second_frame, text='No available copy, try again next time').grid(row=0, column=0)
    
    #
    # Fantasy
    #
    cur.execute('SELECT title, isbn, author, genre FROM books')
    index = 1
    for title, isbn, author, genre in cur:
        if bookGenre.get() == genre :
            #set labels
            Label(second_frame, text='Genre: ' + genre).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book title: ' + title).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book isbn: ' + isbn).grid(row=index, column=0)
            index +=1
            Label(second_frame, text='book author: ' + author).grid(row=index, column=0)
            index +=1
            
            Button(second_frame, text="borrow", command= lambda isbn=isbn: borrowBook1(isbn=isbn)).grid(row=index, column=0)
            index +=1

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
    root.title('Book search')
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
    root.title('Book search')
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
    root.title('Book search')
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

def memberViewBooks():
    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    #set the frame and scrollbar
    root=Toplevel(screen)
    root.geometry('300x600')
    root.title('All books')
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    second_frame = Frame(canvas)
    canvas.create_window((0,0), window=second_frame, anchor="nw")

    rowNum = 0
    cur.execute('SELECT title, isbn, author, publisher, genre FROM books')
    for title, isbn, author, publisher, genre in cur:
            Label(second_frame, text=f'Title: {title}\nISBN: {isbn}\nAuthor: {author}\nPublisher: {publisher}\nGenre: {genre}').grid(row=rowNum, column=0)
            rowNum += 1
    
def selectionScreen():
    global member_id1   #used for member sites
    global member_id2   #used for admin sites
    global bookIsbn2    #used for admin sites

    conn = psycopg2.connect(dbname = 'libraryManager', user="postgres", password="199814", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute('SELECT username, password FROM admin_login')
    for username, password in cur:
        if username1.get() == username and password1.get() == password:
            root=Toplevel(screen)
            root.geometry('500x500')
            root.title('Admin Page')
            label0 = Label(root, text='admin page')
            label0.place(x=30, y=20)

            button1 = Button(root, text="view member info", padx=50, command=memberInfo)
            button1.place(x=70, y=50)

            button2 = Button(root, text="check books", padx=50, command=checkBooks)
            button2.place(x=70, y=100)

            button3 = Button(root, text="check transactions", padx=50, command=checkMembers)
            button3.place(x=70, y=150)

            label1 = Label(root, text="Search member by id:")
            label1.place(x=70, y=200)
            member_id2=StringVar()
            memberIDInput = Entry(root, textvariable=member_id2, width=12)
            memberIDInput.place(x=250, y=200)
            button4 = Button(root, text="Search", padx=50, command=findMemberById)
            button4.place(x=70, y=250)
            

            label2 = Label(root, text="Search book by isbn:")
            label2.place(x=70, y=300)
            bookIsbn2=StringVar()
            ISBNInput = Entry(root, textvariable=bookIsbn2, width=12)
            ISBNInput.place(x=250, y=300)
            button5 = Button(root, text="Search", padx=50, command=manageBookByIsbn)
            button5.place(x=70, y=350)

            button6 = Button(root, text="Add books and copys", padx=50, command=addBooks)
            button6.place(x=70, y=400)

            button6 = Button(root, text="Delete books", padx=50, command=deleteBooks)
            button6.place(x=70, y=450)

            break

    cur.execute('SELECT username, password, member_id mem FROM member_login')
    for username, password, member_id in cur:
        if username1.get() == username and password1.get() == password:
            root=Toplevel(screen)
            root.geometry('500x500')
            root.title('Member Page')
            button1 = Button(root, text="View all books", padx=50, command = memberViewBooks).place(x=70, y=50)
            button1 = Button(root, text="search book",padx=50, command=memberSearch)
            button1.place(x=70, y=100)
            button1 = Button(root, text="return book",padx=50, command=memberReturn)
            button1.place(x=70, y=150)
            member_id1 = member_id
            break

def loginScreen():
    global username1
    global password1
    global screen

    screen = Tk()
    screen.geometry('500x500')
    screen.title('Library Login')

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

from tkinter import *

root = Tk()

def submit():
    message = Label(root, text = loginInput.get()).grid(row=4, column=0)
    message = Label(root, text = passwordInput.get()).grid(row=5, column=0)

loginLabel = Label(root, text="username").grid(row=0, column=0)
loginInput = Entry(root)
loginInput.grid(row=0, column=1)

passwordLabel = Label(root, text="password").grid(row=1, column=0)
passwordInput = Entry(root)
passwordInput.grid(row=1, column=1)

button = Button(root, text="login",padx=50, command=submit).grid(row=3)

# label1.pack()
# label2.pack()
# button.pack()

root.mainloop()

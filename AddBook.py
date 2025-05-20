<<<<<<< HEAD
from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

# High-Contrast Color Scheme
BG_COLOR = "#22223b"  # Very dark blue
FG_COLOR = "#f4f4f4"  # Almost white
ENTRY_BG = "#FFFFFF"  # White input fields
ENTRY_FG = "#000000"  # Black text in inputs
BUTTON_COLOR = "#4cc9f0"  # Bright blue/cyan
BUTTON_TEXT_COLOR = "#22223b"  # Dark for contrast
ERROR_COLOR = "#f72585"  # Vivid pink/red
ERROR_TEXT_COLOR = "#f4f4f4"  # White

# Fonts
TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 12, "bold")
BUTTON_FONT = ("Helvetica", 12, "bold")

def load_bg_image(window):
    pass  # No background image for non-main windows

def connect_db():
    """Connect to MySQL database"""
    try:
        return pymysql.connect(host="localhost", user="root", password="210905", database="db")
    except Exception as e:
        messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
        return None

def bookRegister():
    """Insert the new book into the database"""
    bid, title, author, price, copies = bookInfo1.get(), bookInfo2.get(), bookInfo3.get(), bookInfo4.get(), bookInfo5.get()
    status = "Available"

    if not (bid and title and author and price and copies):
        messagebox.showerror("Error", "All fields must be filled!", icon="error")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO books (bid, title, author, price, copies, status) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (bid, title, author, price, copies, status))
            con.commit()
            messagebox.showinfo("Success", "Book added successfully!", icon="info")
            root.destroy()  # Close the add book window after success
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}", icon="error")
        finally:
            con.close()

def addBook():
    """Create the Add Book window"""
    global bookInfo1, bookInfo2, bookInfo3, bookInfo4, bookInfo5, root
    root = Toplevel()
    root.title("Add Book")
    root.geometry("450x400")
    root.configure(bg=BG_COLOR)

    Label(root, text="Add New Book", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=15)

    labels = ["Book ID:", "Title:", "Author:", "Price:", "Copies:"]
    entries = []

    for text in labels:
        frame = Frame(root, bg=BG_COLOR)
        frame.pack(pady=5, padx=20, fill=X)
        Label(frame, text=text, bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT, anchor="w").pack(side=LEFT, padx=5)
        entry = Entry(frame, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, insertbackground=ENTRY_FG, width=25, relief=SOLID, borderwidth=2)
        entry.pack(side=RIGHT, padx=5)
        entries.append(entry)

    bookInfo1, bookInfo2, bookInfo3, bookInfo4, bookInfo5 = entries

    Button(root, text="Submit", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=bookRegister).pack(pady=10)
    Button(root, text="Cancel", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.destroy).pack(pady=5)
=======
from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import pymysql

def bookRegister():
    
    bid = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    status = bookInfo4.get()
    status = status.lower()
    
    insertBooks = "insert into "+bookTable+" values ('"+bid+"','"+title+"','"+author+"','"+status+"')"
    try:
        cur.execute(insertBooks)
        con.commit()
        messagebox.showinfo('Success',"Book added successfully")
    except:
        messagebox.showinfo("Error","Can't add data into Database")
    
    print(bid)
    print(title)
    print(author)
    print(status)
    root.destroy()

def addBook(): 
    
    global bookInfo1 ,bookInfo2, bookInfo3, bookInfo4, Canvas1, con, cur, bookTable, root
    
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")

    
    mypass = "210905"
    mydatabase="db"


    con = pymysql.connect( host="localhost",user="root",password=mypass,database=mydatabase)
    cur = con.cursor()
    # Table Names here
    bookTable = "books" # Book Table
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True,fill=BOTH)
        
    headingFrame1 = Frame(root,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier',15))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)

    # Book ID
    lb1 = Label(labelFrame,text="Book ID : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.2, relheight=0.08)
        
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.08)
        
    # Title
    lb2 = Label(labelFrame,text="Title : ", bg='black', fg='white')
    lb2.place(relx=0.05,rely=0.35, relheight=0.08)
        
    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.08)
        
    # Book Author
    lb3 = Label(labelFrame,text="Author : ", bg='black', fg='white')
    lb3.place(relx=0.05,rely=0.50, relheight=0.08)
        
    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3,rely=0.50, relwidth=0.62, relheight=0.08)
        
    # Book Status
    lb4 = Label(labelFrame,text="Status(Avail/issued) : ", bg='black', fg='white')
    lb4.place(relx=0.05,rely=0.65, relheight=0.08)
        
    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(root,text="SUBMIT", bg='#d1ccc0', fg='black', command=bookRegister)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    root.mainloop()
>>>>>>> 4d1ccf95b423203ce3bbf370951af86e35ea158a

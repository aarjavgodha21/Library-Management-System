from tkinter import *
from tkinter import messagebox
import pymysql
from AddBook import addBook
from DeleteBook import delete
from ViewBooks import viewBooks
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
LABEL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")

def load_bg_image(window):
    pass  # No background image for non-main windows

def connect_db():
    return pymysql.connect(host="localhost", user="root", password="210905", database="db")

def createPublisher():
    global pub_id, name, address, password_entry, signup_win
    
    signup_win = Toplevel(root)
    signup_win.title("New Publisher Registration")
    signup_win.geometry("400x400")
    signup_win.configure(bg=BG_COLOR)
    
    Label(signup_win, text="Publisher ID:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    pub_id = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    pub_id.pack(pady=5)
    
    Label(signup_win, text="Name:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    name = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    name.pack(pady=5)
    
    Label(signup_win, text="Address:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    address = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    address.pack(pady=5)
    
    Label(signup_win, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    password_entry = Entry(signup_win, show="*", bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    password_entry.pack(pady=5)
    
    Button(signup_win, text="Register", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=registerPublisher).pack(pady=10)
    Button(signup_win, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=signup_win.destroy).pack(pady=10)

def registerPublisher():
    sql = "INSERT INTO publishers (pub_id, name, address, password) VALUES (%s, %s, %s, %s)"
    values = (pub_id.get(), name.get(), address.get(), password_entry.get())
    
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute(sql, values)
        con.commit()
        messagebox.showinfo("Success", "Publisher registered successfully!", icon="info")
        signup_win.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Database issue: {str(e)}", icon="error")
    finally:
        con.close()

def openPublisherDashboard():
    dashboard = Toplevel(root)
    dashboard.title("Publisher Dashboard")
    dashboard.geometry("500x400")
    dashboard.configure(bg=BG_COLOR)
    
    Label(dashboard, text="Publisher Options", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=20)
    
    Button(dashboard, text="Add Book", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=addBook).pack(pady=5)
    Button(dashboard, text="Delete Book", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=delete).pack(pady=5)
    Button(dashboard, text="View Books", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=viewBooks).pack(pady=5)
    Button(dashboard, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=dashboard.destroy).pack(pady=20)

def publisherLogin():
    global login_id, login_password, login_win
    
    login_win = Toplevel(root)
    login_win.title("Publisher Login")
    login_win.geometry("400x300")
    login_win.configure(bg=BG_COLOR)
    
    Label(login_win, text="Publisher ID:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    login_id = Entry(login_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    login_id.pack(pady=5)
    
    Label(login_win, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    login_password = Entry(login_win, show='*', bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    login_password.pack(pady=5)
    
    Button(login_win, text="Login", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=verifyPublisher).pack(pady=10)
    Button(login_win, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=login_win.destroy).pack(pady=10)

def verifyPublisher():
    """Verify publisher credentials and open dashboard if valid"""
    sql = "SELECT * FROM publishers WHERE pub_id=%s AND password=%s"
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql, (login_id.get(), login_password.get()))
    result = cur.fetchone()
    
    if result:
        messagebox.showinfo("Success", "Login successful!", icon="info")
        login_win.destroy()
        openPublisherDashboard()  # Restored this function call
    else:
        messagebox.showerror("Error", "Invalid credentials", icon="error")

def openPublisherPortal():
    global root
    root = Tk()
    root.title("Publisher Portal")
    root.geometry("700x500")
    root.configure(bg=BG_COLOR)
    
    headingFrame1 = Frame(root, bg=BUTTON_COLOR, bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.15)
    headingLabel = Label(headingFrame1, text="Publisher Portal", bg=BUTTON_COLOR, fg=FG_COLOR, font=TITLE_FONT)
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    Button(root, text="Sign Up", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=createPublisher).place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
    Button(root, text="Sign In", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=publisherLogin).place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
    Button(root, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.destroy).place(relx=0.3, rely=0.75, relwidth=0.4, relheight=0.1)
    root.mainloop()
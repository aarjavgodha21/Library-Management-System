from tkinter import *
from tkinter import messagebox
import pymysql
from datetime import datetime, timedelta
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

logged_in_member = None  # Store logged-in member ID

def load_bg_image(window):
    pass  # No background image for non-main windows

def connect_db():
    return pymysql.connect(host="localhost", user="root", password="210905", database="db")

def createMember():
    global member_id, name, address, password_entry, signup_win
    
    signup_win = Toplevel(root)
    signup_win.title("New Member Registration")
    signup_win.geometry("400x400")
    signup_win.configure(bg=BG_COLOR)
    
    Label(signup_win, text="Member ID:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    member_id = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    member_id.pack(pady=5)
    
    Label(signup_win, text="Name:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    name = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    name.pack(pady=5)
    
    Label(signup_win, text="Address:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    address = Entry(signup_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    address.pack(pady=5)
    
    Label(signup_win, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    password_entry = Entry(signup_win, show="*", bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    password_entry.pack(pady=5)
    
    Button(signup_win, text="Register", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=registerMember).pack(pady=10)
    Button(signup_win, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=signup_win.destroy).pack(pady=10)

def registerMember():
    issue_date = datetime.today().strftime('%Y-%m-%d')
    exp_date = (datetime.today() + timedelta(days=180)).strftime('%Y-%m-%d')
    
    sql = "INSERT INTO members (member_id, name, address, issue_date, exp_date, password) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (member_id.get(), name.get(), address.get(), issue_date, exp_date, password_entry.get())
    
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute(sql, values)
        con.commit()
        messagebox.showinfo("Success", "Member registered successfully!", icon="info")
        signup_win.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Database issue: {str(e)}", icon="error")
    finally:
        con.close()

def memberLogin():
    global login_id, login_password, login_win
    
    login_win = Toplevel(root)
    login_win.title("Member Login")
    login_win.geometry("400x300")
    login_win.configure(bg=BG_COLOR)
    
    Label(login_win, text="Member ID:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    login_id = Entry(login_win, bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    login_id.pack(pady=5)
    
    Label(login_win, text="Password:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    login_password = Entry(login_win, show='*', bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    login_password.pack(pady=5)
    
    Button(login_win, text="Login", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=verifyMember).pack(pady=10)
    Button(login_win, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=login_win.destroy).pack(pady=10)

def verifyMember():
    global logged_in_member
    sql = "SELECT * FROM members WHERE member_id=%s AND password=%s"
    con = connect_db()
    cur = con.cursor()
    cur.execute(sql, (login_id.get(), login_password.get()))
    result = cur.fetchone()
    
    if result:
        logged_in_member = login_id.get()  
        messagebox.showinfo("Success", "Login successful!", icon="info")
        login_win.destroy()
        openMemberDashboard()
    else:
        messagebox.showerror("Error", "Invalid credentials", icon="error")

def openMemberDashboard():
    from IssueBook import issue  
    from ReturnBook import returnBookUI
    
    dashboard = Toplevel(root)
    dashboard.title("Member Dashboard")
    dashboard.geometry("500x400")
    dashboard.configure(bg=BG_COLOR)
    
    Label(dashboard, text=f"Welcome, Member {logged_in_member}", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=10)
    
    Button(dashboard, text="View Books", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=viewBooks).pack(pady=5)
    Button(dashboard, text="Issue Book", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=issue).pack(pady=5)
    Button(dashboard, text="Return Book", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=returnBookUI).pack(pady=5)
    Button(dashboard, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=dashboard.destroy).pack(pady=20)

def openMemberPortal():
    global root
    root = Tk()
    root.title("Member Portal")
    root.geometry("700x500")
    root.configure(bg=BG_COLOR)
    
    headingFrame1 = Frame(root, bg=BUTTON_COLOR, bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.15)
    headingLabel = Label(headingFrame1, text="Member Portal", bg=BUTTON_COLOR, fg=FG_COLOR, font=TITLE_FONT)
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    Button(root, text="Sign Up", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=createMember).place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
    Button(root, text="Sign In", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=memberLogin).place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
    Button(root, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.destroy).place(relx=0.3, rely=0.75, relwidth=0.4, relheight=0.1)
    root.mainloop()
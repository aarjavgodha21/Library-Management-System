from tkinter import *
from tkinter import messagebox
import pymysql
from Member import logged_in_member, openMemberDashboard
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

def connect_db():
    """Connect to MySQL database"""
    try:
        return pymysql.connect(host="localhost", user="root", password="210905", database="db")
    except Exception as e:
        messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
        return None

def getAvailableBooks():
    """Fetch all available books with copies > 0"""
    con = connect_db()
    books = []
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT bid, title FROM books WHERE copies > 0")
            books = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]  # Format: "101 - Harry Potter"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch book IDs: {str(e)}")
        finally:
            con.close()
    return books

def issueBook():
    """Issue a book to the logged-in member"""
    global logged_in_member
    selected_book = book_var.get()
    bid = selected_book.split(" - ")[0]  # Extract only the book ID

    if not logged_in_member:
        messagebox.showerror("Error", "No member is logged in", icon="error")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT copies FROM books WHERE bid=%s", (bid,))
            book = cur.fetchone()

            if book and book[0] > 0:
                cur.execute("INSERT INTO books_issued (bid, issuedto) VALUES (%s, %s)", (bid, logged_in_member))
                cur.execute("UPDATE books SET copies = copies - 1 WHERE bid=%s", (bid,))
                con.commit()
                messagebox.showinfo("Success", "Book Issued Successfully", icon="info")
                root.withdraw()
                openMemberDashboard()
            else:
                messagebox.showerror("Error", "Book not available", icon="error")
        except Exception as e:
            messagebox.showerror("Database Error", f"Issue failed: {str(e)}", icon="error")
        finally:
            con.close()

def load_bg_image(window):
    pass  # No background image for non-main windows

def issue():
    """Create the Issue Book window"""
    global book_var, root

    root = Toplevel()
    root.title("Issue Book")
    root.geometry("450x350")
    root.configure(bg=BG_COLOR)

    Label(root, text="Issue Book", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=15)

    available_books = getAvailableBooks()

    Label(root, text="Select Book:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    book_var = StringVar(root)
    if available_books:
        book_var.set(available_books[0])
    book_dropdown = OptionMenu(root, book_var, *available_books)
    book_dropdown.config(bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    book_dropdown.pack(pady=5)

    Button(root, text="Issue", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=issueBook).pack(pady=10)
    Button(root, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.withdraw).pack(pady=5)
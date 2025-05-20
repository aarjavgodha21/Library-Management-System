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

def load_bg_image(window):
    pass  # No background image for non-main windows

def connect_db():
    """Connect to MySQL database"""
    try:
        return pymysql.connect(host="localhost", user="root", password="210905", database="db")
    except Exception as e:
        messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
        return None

def getIssuedBooks():
    """Fetch all books issued to the logged-in member, showing both ID and title"""
    global logged_in_member
    con = connect_db()
    issued_books = []
    if con:
        try:
            cur = con.cursor()
            cur.execute("""
                SELECT books.bid, books.title FROM books_issued
                JOIN books ON books_issued.bid = books.bid
                WHERE books_issued.issuedto = %s
            """, (logged_in_member,))
            issued_books = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]  # "101 - Harry Potter"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch issued books: {str(e)}")
        finally:
            con.close()
    return issued_books

def returnBook():
    """Return a book for the logged-in member"""
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
            cur.execute("SELECT * FROM books_issued WHERE bid=%s AND issuedto=%s", (bid, logged_in_member))
            result = cur.fetchone()

            if result:
                cur.execute("DELETE FROM books_issued WHERE bid=%s AND issuedto=%s", (bid, logged_in_member))
                cur.execute("UPDATE books SET copies = copies + 1 WHERE bid=%s", (bid,))
                con.commit()
                messagebox.showinfo("Success", "Book Returned Successfully", icon="info")
                root.withdraw()
                openMemberDashboard()
            else:
                messagebox.showerror("Error", "Invalid Book ID or Member ID", icon="error")
        except Exception as e:
            messagebox.showerror("Database Error", f"Return failed: {str(e)}", icon="error")
        finally:
            con.close()

def returnBookUI():
    """Create the Return Book window"""
    global book_var, root

    root = Toplevel()
    root.title("Return Book")
    root.geometry("450x350")
    root.configure(bg=BG_COLOR)

    Label(root, text="Return Book", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=15)

    issued_books = getIssuedBooks()

    Label(root, text="Select Book:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    book_var = StringVar(root)
    if issued_books:
        book_var.set(issued_books[0])
    book_dropdown = OptionMenu(root, book_var, *issued_books)
    book_dropdown.config(bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    book_dropdown.pack(pady=5)

    Button(root, text="Return", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=returnBook).pack(pady=10)
    Button(root, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.withdraw).pack(pady=5)
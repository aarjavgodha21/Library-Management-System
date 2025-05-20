from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

# High-Contrast Color Scheme
BG_COLOR = "#22223b"  # Very dark blue
FG_COLOR = "#f4f4f4"  # Almost white
ACCENT_COLOR = "#4cc9f0"  # Bright blue/cyan
BUTTON_COLOR = "#4cc9f0"  # Bright blue/cyan
BUTTON_TEXT_COLOR = "#22223b"  # Dark for contrast
ERROR_COLOR = "#f72585"  # Vivid pink/red
ERROR_TEXT_COLOR = "#f4f4f4"  # White

# Fonts
TITLE_FONT = ("Helvetica", 18, "bold")
LABEL_FONT = ("Helvetica", 12, "bold")
DATA_FONT = ("Courier", 12)

def connect_db():
    """Connect to MySQL database"""
    try:
        return pymysql.connect(host="localhost", user="root", password="210905", database="db")
    except Exception as e:
        messagebox.showerror("Database Error", f"Connection failed: {str(e)}")
        return None

def load_bg_image(window):
    pass  # No background image for non-main windows

def viewBooks():
    """Fetch and display books in a properly formatted structure"""
    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT bid, title, author, price, copies, status FROM books")
            books = cur.fetchall()

            view_win = Toplevel()
            view_win.title("View Books")
            view_win.geometry("900x500")
            view_win.configure(bg=BG_COLOR)

            Label(view_win, text="Available Books", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=10)

            frame = Frame(view_win, bg=BG_COLOR)
            frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

            scrollbar_y = Scrollbar(frame, orient=VERTICAL)
            scrollbar_x = Scrollbar(frame, orient=HORIZONTAL)

            text_area = Text(frame, bg=BG_COLOR, fg=FG_COLOR, font=DATA_FONT, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            text_area.pack(expand=True, fill=BOTH)

            scrollbar_y.config(command=text_area.yview, bg=ACCENT_COLOR)
            scrollbar_x.config(command=text_area.xview, bg=ACCENT_COLOR)
            scrollbar_y.pack(side=RIGHT, fill=Y)
            scrollbar_x.pack(side=BOTTOM, fill=X)

            header = "{:<10} {:<30} {:<25} {:<10} {:<10} {:<15}\n".format("BID", "Title", "Author", "Price", "Copies", "Status")
            text_area.insert(END, header)
            text_area.insert(END, "=" * 105 + "\n")

            for book in books:
                row = "{:<10} {:<30} {:<25} {:<10} {:<10} {:<15}\n".format(*book)
                text_area.insert(END, row)

            text_area.config(state=DISABLED)

            Button(view_win, text="Quit", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=LABEL_FONT, relief=RAISED, borderwidth=3, command=view_win.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch books: {str(e)}", icon="error")
        finally:
            con.close()
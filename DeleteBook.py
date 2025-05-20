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

def getBookIDs():
    """Fetch all available book IDs and names"""
    con = connect_db()
    books = []
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT bid, title FROM books")
            books = [f"{row[0]} - {row[1]}" for row in cur.fetchall()]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch book IDs: {str(e)}")
        finally:
            con.close()
    return books

def getBookCopies(bid):
    """Fetch the number of copies available for the selected book"""
    con = connect_db()
    copies = 1
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT copies FROM books WHERE bid=%s", (bid,))
            result = cur.fetchone()
            if result:
                copies = result[0]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch copies: {str(e)}")
        finally:
            con.close()
    return copies

def updateCopiesSlider(*args):
    """Update the copies slider when a book is selected"""
    selected_book = book_var.get()
    selected_bid = selected_book.split(" - ")[0]  # Extract bid
    available_copies = getBookCopies(selected_bid)
    copies_slider.config(to=available_copies)
    copies_slider.set(1)

def deleteBook():
    """Delete the selected number of copies from the selected book"""
    selected_book = book_var.get()
    bid = selected_book.split(" - ")[0]  # Extract bid
    copies_to_delete = copies_slider.get()
    
    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT copies FROM books WHERE bid=%s", (bid,))
            result = cur.fetchone()
            
            if result:
                available_copies = int(result[0])
                if available_copies >= copies_to_delete:
                    cur.execute("UPDATE books SET copies = copies - %s WHERE bid=%s", (copies_to_delete, bid))
                    con.commit()
                    messagebox.showinfo("Success", f"{copies_to_delete} copies deleted successfully!", icon="info")

                    if available_copies - copies_to_delete == 0:
                        cur.execute("DELETE FROM books WHERE bid=%s", (bid,))
                        con.commit()
                        messagebox.showinfo("Info", "All copies deleted, book removed from records", icon="info")

                    delete_window.destroy()
                else:
                    messagebox.showerror("Error", "Not enough copies available to delete", icon="error")
            else:
                messagebox.showerror("Error", "Invalid Book ID", icon="error")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete book: {str(e)}", icon="error")
        finally:
            con.close()

def delete():
    """Create the Delete Book window"""
    global book_var, copies_slider, delete_window

    delete_window = Toplevel()
    delete_window.title("Delete Book")
    delete_window.geometry("450x400")
    delete_window.configure(bg=BG_COLOR)

    Label(delete_window, text="Delete Book", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT).pack(pady=15)

    Label(delete_window, text="Select Book:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    book_var = StringVar(delete_window)

    books = getBookIDs()
    if books:
        book_var.set(books[0])
    book_dropdown = OptionMenu(delete_window, book_var, *books, command=updateCopiesSlider)
    book_dropdown.config(bg=ENTRY_BG, fg=ENTRY_FG, font=LABEL_FONT, relief=SOLID, borderwidth=2)
    book_dropdown.pack(pady=5)

    Label(delete_window, text="Select Copies to Delete:", bg=BG_COLOR, fg=FG_COLOR, font=LABEL_FONT).pack(pady=5)
    copies_slider = Scale(delete_window, from_=1, to=1, orient=HORIZONTAL, length=250, bg=BG_COLOR, fg=FG_COLOR)
    copies_slider.pack(pady=5)

    Button(delete_window, text="Delete", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=deleteBook).pack(pady=10)
    Button(delete_window, text="Cancel", bg=ERROR_COLOR, fg=ERROR_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=delete_window.destroy).pack(pady=5)

    updateCopiesSlider()

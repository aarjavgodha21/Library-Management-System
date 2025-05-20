from tkinter import *
from PIL import Image, ImageTk
from Member import openMemberPortal
from Publisher import openPublisherPortal

# Updated Color Scheme (Vibrant and Bright)
BG_COLOR = "#CC4400"  # Bright Coral
FG_COLOR = "#FFFFFF"  # White text
BUTTON_COLOR = "#EA16EF"  # Dark Purple
BUTTON_TEXT_COLOR = "#F4EEFF"  # Light Lavender
ERROR_COLOR = "#D92027"  # Vibrant Red for Quit Button

# Fonts
TITLE_FONT = ("Helvetica", 20, "bold")
BUTTON_FONT = ("Helvetica", 14, "bold")

def openMain():
    global root
    root = Tk()
    root.title("Library Management System")
    root.geometry("700x500")
    
    # Load and set wallpaper
    try:
        bg_image = Image.open("lib.jpg")
        bg_image = bg_image.resize((700, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        # Store the image reference in the window object
        root.bg_image = bg_photo
        bg_label = Label(root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
    except Exception as e:
        print("Error loading wallpaper:", e)
    
    # Heading Frame with Gradient Background
    headingFrame = Frame(root, bg=BG_COLOR, bd=5)
    headingFrame.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.15)
    headingLabel = Label(headingFrame, text="Library System", bg=BG_COLOR, fg=FG_COLOR, font=TITLE_FONT)
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # Buttons with Neon Effect
    Button(root, text="Member Section", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=openMemberPortal).place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
    Button(root, text="Publisher Section", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=openPublisherPortal).place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
    Button(root, text="Quit", bg=ERROR_COLOR, fg=FG_COLOR, font=BUTTON_FONT, relief=RAISED, borderwidth=3, command=root.destroy).place(relx=0.3, rely=0.75, relwidth=0.4, relheight=0.1)
    
    root.mainloop()

openMain()
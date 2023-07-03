import re
import tkinter as tk
import subprocess
from threading import Timer
from tkinter import messagebox

# pip install pillow
from PIL import Image, ImageTk

# Log off function for macOS
def log_off():
    # TODO: Use this instead
    # "osascript -e 'tell application \"loginwindow\" to «event aevtrlgo»'"
    subprocess.call(["osascript", "-e", "tell application \"loginwindow\" to «event aevtrlgo»"])

seconds_left = 60 * 5  # 5 minutes

# Function to update the timer display
def tick_timer():
    global seconds_left
    seconds_left -= 1
    minutes = seconds_left // 60
    seconds = seconds_left % 60
    timer_label.config(text=f"{minutes:2d} minutes, {seconds:02d} seconds remaining")
    if seconds_left > 0:
        # Schedule the next update after 1 second
        timer = Timer(1, tick_timer)
        timer.daemon = True
        timer.start()
    else:
        timer_label.config(text=f"Good night!")
        log_off()

# Function to handle the button press
def continue_pressed():
    log_off()

# Function to handle window close event
def on_close():
    log_off()

# Function to handle the cheat code entry
# TODO: Fix this
def check_cheat_code():
    cheat_code = entry.get().strip()

    match = re.match(r"I really really really really really need to spend another(\d+) minutes? doing something really important", cheat_code)
    if match:
        minutes = int(match.group(1))
        entry.delete(0, tk.END)

        global seconds_left
        seconds_left = minutes * 60
        window.withdraw()  # Hide the window

        # Schedule the window to show again after (X - 5) minutes
        seconds_until_show_again = (minutes - 5) * 60
        if seconds_until_show_again < 0:
            window.deiconify()
        else:
            timer = Timer(seconds_until_show_again, window.deiconify)
            timer.daemon = True
            timer.start()
    else:
        messagebox.showinfo("Invalid Cheat Code", "The entered cheat code is invalid.")



# Create the GUI
window = tk.Tk()
window.title("")

# Make the window stay on top
window.attributes('-topmost', True)
window.resizable(False, False)

# Disable window closing using Cmd+Q shortcut (for macOS)
window.createcommand('::tk::mac::Quit', lambda: None)

# Center the window on the screen
window_width = 700
window_height = 200
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
window.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')


# Load the image
image = Image.open("./bedtime.webp")

# Create a PhotoImage object from the loaded image
image_tk = ImageTk.PhotoImage(image, width=50)

# Create a label to display the image
image_label = tk.Label(window, image=image_tk)
image_label.pack(side=tk.LEFT)


# Create a frame to hold the timer display and continue button
frame = tk.Frame(window)
frame.pack(pady=20)

# Display the text in the middle of the window
text_label = tk.Label(frame, text="I love getting good sleep. I take care of myself and my health, "
                                   "and going to bed and waking up at the same time every night "
                                   "and every morning is one of the ways I do this.",
                                   wraplength=400,
                                   justify=tk.LEFT,
                                   )
text_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

# Display the timer label on the left side
timer_label = tk.Label(frame, text="")
timer_label.grid(row=1, column=0, sticky=tk.W)

# Create the continue button on the right side
continue_button = tk.Button(frame, text="Continue", command=continue_pressed)
continue_button.grid(row=1, column=1, sticky=tk.E)

# Create a cheat code entry field
entry = tk.Entry(window, width=50)
entry.pack(pady=10)
entry.focus()

# Configure column weights for dynamic spacing
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

# Adjust column spacing
frame.grid_columnconfigure(0, minsize=1, pad=10)

# Adjust window resizing behavior
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Bind the window close event to the on_close function
window.protocol("WM_DELETE_WINDOW", on_close)

# Bind the entry field to check cheat code
entry.bind('<Return>', lambda event: check_cheat_code())

# Start the timer
tick_timer()

# Run the GUI event loop
window.mainloop()

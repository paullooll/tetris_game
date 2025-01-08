import sys
import tkinter
import mysql.connector
from tkinter import *
from tkinter import Entry
from tkinter import messagebox
from PIL import ImageTk
import database  # Assuming you have a database.py file with connection details
from mysql.connector import Error

conn = database.conn  # Assuming you have a database.py file with connection details

# --- Tkinter Login Form Code ---

form = tkinter.Tk()
bg_image = ImageTk.PhotoImage(file="bg.png")  # Replace with your actual background image
bg_label = Label(form, image=bg_image)
bg_label.grid(row=0, column=0)
form_width = 800
form_height = 600
screen_width = form.winfo_screenwidth()
screen_height = form.winfo_screenheight()
x = (screen_width / 2) - (form_width / 2)
y = (screen_height / 2) - (form_height / 2)

form.geometry("%dx%d+%d+%d" % (form_width, form_height, x, y))
form.title("Admin Login")

txt_username = Entry(form, width=25, font=("Consolas Bold", 16))
txt_username.place(x=330, y=180, height=35)

txt_password = Entry(form, width=20, font=("Consolas Bold", 16), show='*')
txt_password.place(x=390, y=230, height=35)


def check_login():
    global current_user  # Make current_user global to access it in other functions
    username = txt_username.get()
    password = txt_password.get()
    try:
        if conn.is_connected():
            pst = conn.cursor()
            sqlquery = 'SELECT * FROM admin WHERE username=%s AND password=%s'
            pst.execute(sqlquery, (username, password))
            rs = pst.fetchone()
            if (username == "" and password == ""):
                messagebox.showinfo( "Error", "Username and Password is required")
                return
            elif rs is None:
                messagebox.showinfo("", "Username and Password is Incorrect")
            else:
                messagebox.showinfo("", "Login Successfully")
                current_user = username  # Store the logged-in username
                form.destroy()  # Close the login window
                open_manage_window()  # Open the manage window
    except Error as e:
        messagebox.showinfo("", "Connection Failed")

def open_manage_window():
    manage_window = Tk()
    manage_window.title("Manage Users")
    manage_window.geometry("%dx%d+%d+%d" % (form_width, form_height, x, y))  # Same size and position

    bg_image_manage = ImageTk.PhotoImage(file="bg.png")  # Replace with your actual background image
    bg_label_manage = Label(manage_window, image=bg_image_manage)  # Use manage_window as parent
    bg_label_manage.place(x=0, y=0, relwidth=1, relheight=1)  # Place the image to cover the entire window

    # --- Keep a reference to the image to prevent garbage collection ---
    manage_window.bg_image_manage = bg_image_manage
    # --- Table ---

    # Create a frame for the table
    table_frame = Frame(manage_window)
    table_frame.pack(pady=16)

    # Create the table using a Listbox (or any other suitable widget)
    lbl_name = Label(table_frame, text="Name", font=("Consolas Bold", 16))
    lbl_name.grid(row=0, column=0, padx=5)

    lbl_score = Label(table_frame, text="Score", font=("Consolas Bold", 16))
    lbl_score.grid(row=0, column=1, padx=5)

    # --- End of adding labels ---

    user_listbox = Listbox(table_frame, width=50, height=15, font=("Consolas Bold", 16))
    user_listbox.grid(row=1, column=0, columnspan=2, pady=5)

    def populate_table():
        user_listbox.delete(0, END)  # Clear the table
        try:
            if conn.is_connected():
                cursor = conn.cursor()
                query = "SELECT username, score FROM user"
                cursor.execute(query)
                users = cursor.fetchall()
                for user in users:
                    # --- Format the string to align the score ---
                    user_listbox.insert(END, f"{user[0]:<15} {user[1]:>22}")  # Left align name, right align score
                    # --- End of formatting ---
        except Error as e:
            messagebox.showinfo("", f"Error fetching data: {e}")

    populate_table()  # Populate the table initially

    # --- CRUD Buttons ---

    def delete_user():
        try:
            selected_index = user_listbox.curselection()[0]
            selected_user = user_listbox.get(selected_index).split()[0]  # Split by space to get the username
            if conn.is_connected():
                cursor = conn.cursor()
                query = "DELETE FROM user WHERE username = %s"
                cursor.execute(query, (selected_user,))
                conn.commit()
                populate_table()  # Refresh the table
                messagebox.showinfo("", "User deleted successfully")
        except IndexError:
            messagebox.showinfo("", "Please select a user to delete")
        except Error as e:
            messagebox.showinfo("", f"Error deleting user: {e}")

    def update_user():
        try:
            selected_index = user_listbox.curselection()[0]
            selected_user = user_listbox.get(selected_index).split()[0]  # Split by space to get the username

            # --- Implementation for updating username ---

            def update_username():
                new_username = txt_new_username.get()
                if new_username == "":
                    messagebox.showinfo("Error", "New username cannot be empty")
                    return
                try:
                    if conn.is_connected():
                        cursor = conn.cursor()
                        query = "UPDATE user SET username = %s WHERE username = %s"
                        cursor.execute(query, (new_username, selected_user))
                        conn.commit()
                        populate_table()  # Refresh the table
                        messagebox.showinfo("", "Username updated successfully")
                        update_window.destroy()  # Close the update window
                except Error as e:
                    messagebox.showinfo("", f"Error updating username: {e}")

            update_window = Toplevel(manage_window)
            update_window.title("Update Username")
            update_window.geometry("200x200")  # Set size to 200x200

            # Center the window
            update_window.update_idletasks(
            )  # Required to get accurate size information before centering
            screen_width = update_window.winfo_screenwidth()
            screen_height = update_window.winfo_screenheight()
            x = (screen_width / 2) - (200 / 2)  # Calculate x-coordinate for centering
            y = (screen_height / 2) - (200 / 2)  # Calculate y-coordinate for centering
            update_window.geometry("+%d+%d" % (x, y))  # Set position

            lbl_new_username = Label(update_window, text="New Username:")
            lbl_new_username.pack(pady=5)

            txt_new_username = Entry(update_window)
            txt_new_username.pack(pady=5)

            btn_update_confirm = Button(update_window, text="Update", command=update_username)
            btn_update_confirm.pack(pady=5)

            # --- End of implementation ---

        except IndexError:
            messagebox.showinfo("", "Please select a user to update")

    def refresh_table():
        populate_table()

    def logout_user():
        # Confirm the logout action
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:  # If the user clicks "Yes"
            try:
                messagebox.showinfo("", "You have been logged out successfully")
                sys.exit()  # Terminate the entire Python application
            except Exception as e:
                messagebox.showinfo("Error", f"Error during logout: {e}")

    button_frame = Frame(manage_window, bg='black')
    button_frame.pack(pady=10)

    btn_delete = Button(button_frame, text="Delete", command=delete_user, width=20, height=3, bg="red", fg="white")  # Red button
    btn_delete.pack(side=LEFT, padx=5)

    btn_update = Button(button_frame, text="Update", command=update_user, width=20,height=3, bg="green",
                        fg="white")  # Green button
    btn_update.pack(side=LEFT, padx=5)

    btn_refresh = Button(button_frame, text="Refresh", command=refresh_table, width=20,height=3, bg="yellow")  # Yellow button
    btn_refresh.pack(side=LEFT, padx=5)

    btn_logout = Button(button_frame, text="Log Out", command=logout_user, width=20, height=3, bg="blue",
                        fg="white")  # Blue button
    btn_logout.pack(side=LEFT, padx=5)

    manage_window.mainloop()


btn_login = Button(form, width=24, font=("Consolas Bold", 16), text="Login", command=check_login)
btn_login.place(x=250, y=300, height=50)
btn_login.configure(bg='green', fg='white')

# --- Add the mainloop to start the Tkinter event loop ---
form.mainloop()
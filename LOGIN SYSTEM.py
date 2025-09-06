import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as mycon

root = tk.Tk()
root.geometry("500x400")
root.title("LOGIN SYSTEM")
root.resizable(False, False)

#login window
try:
    bg_image = Image.open(r"C:\\Users\\Lenovo\\Desktop\\bb.jpg") #bg image added to login page
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Background image not found:", e)

#mysql and python connectivity
try:
    mycon = mycon.connect(host="localhost", user="root", passwd="12345", database="d")
    cursor = mycon.cursor()
except Exception as e:
    messagebox.showerror("ERROR", f"Database Connection Failed: {e}")

# Profile window that displays user's profile information fetched from SQL.
def profile(parent_window,fullname):
    w1= tk.Toplevel(parent_window)
    w1.geometry("550x550")
    w1.title("profile")

    try:
        #bg image added to profile window which show users details
        bg_image3 = Image.open(r"C:\\Users\\Lenovo\\Desktop\\dark.jpg")
        bg_photo3= ImageTk.PhotoImage(bg_image3)
        bg_label3 = tk.Label(w1, image=bg_photo3)
        bg_label3.image = bg_photo3
        bg_label3.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image not found:", e)


    try:
        query = "SELECT fullname, fathersname, address, email FROM data4 WHERE fullname = %s"
        cursor.execute(query, (fullname,))
        data = cursor.fetchone()

        if data:
            fullname, fathersname, address, email = data

            profile_text = f"""
            ----------------------------
                    YOUR PROFILE
            ----------------------------
            Full Name     : {fullname}
            Father's Name : {fathersname}
            Address       : {address}
            Email         : {email}
            """

            profile_label = tk.Label(w1,text=profile_text,justify="left",bg="black",fg="white",font="Courier 12 bold",anchor="w",padx=20,pady=20)
            profile_label.place(x=30, y=80)
        else:
            messagebox.showerror("Error", "User details not found.")
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch profile: {e}")

    ll1 = tk.Label(w1, text="YOUR DETAILS :--", bg="white", fg="black", font="arial 18 bold")
    ll1.place(x=30,y=50)

#edit button 
    edit_btn = tk.Button(w1, text="Edit Profile", bg="white", fg="black", font="arial 12 bold", command=lambda: edit_profile(w1, fullname))
    edit_btn.place(x=30, y=350)

#login window(login only if username and password matches with stored data in sql)
def login():
    username = e1.get()
    password = e2.get()

    try:
        
        query = "SELECT * FROM data4 WHERE fullname = %s AND psswd = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
             w = tk.Toplevel(root)
             w.geometry("430x430")
             w.resizable(False, False)

             try:
                #bg image added to login page
                bg_image1 = Image.open(r"C:\Users\Lenovo\Desktop\profile.jpg")
                bg_photo1 = ImageTk.PhotoImage(bg_image1)
                bg_label1 = tk.Label(w, image=bg_photo1)
                bg_label1.image = bg_photo1 
                bg_label1.place(x=0, y=0, relwidth=1, relheight=1)
             except Exception as e:
                 print("Background image not found:", e)

            #after logged in successfully usersname will be shown
             label = tk.Label(w, text=f"Welcome {username} !!", bg="white", fg="blue", font="arial 20 bold")
             label.place(x=100, y=180)

            #button for viewing profile 
             bb1=tk.Button(w,text="Profile",bg="white",fg="black",font="arial 12 bold",command=lambda:profile(w,username))
             bb1.place(x=20,y=30)  
 
        else:
              messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

#edit window to edit the profile details
def edit_profile(parent_window, fullname):
    edit_win = tk.Toplevel(parent_window)
    edit_win.geometry("500x400")
    edit_win.title("Edit Profile")

    try:
                #bg image added to edit page
                bg_image5 = Image.open(r"C:\Users\Lenovo\Desktop\d2.jpg")
                bg_photo5 = ImageTk.PhotoImage(bg_image5)
                bg_label5 = tk.Label(edit_win, image=bg_photo5)
                bg_label5.image = bg_photo5
                bg_label5.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
                 print("Background image not found:", e)

    try:
        query = "SELECT fullname, fathersname, address, email FROM data4 WHERE fullname = %s"
        cursor.execute(query, (fullname,))
        data = cursor.fetchone()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return

    if not data:
        messagebox.showerror("Error", "User data not found.")
        return

    fullname_val, fathersname_val, address_val, email_val = data

    tk.Label(edit_win, text="Full Name",bg="black",fg="white").pack(pady=5)
    fullname_entry = tk.Entry(edit_win)
    fullname_entry.pack()
    fullname_entry.insert(0, fullname_val)

    tk.Label(edit_win, text="Father's Name",bg="black",fg="white").pack(pady=5)
    father_entry = tk.Entry(edit_win)
    father_entry.pack()
    father_entry.insert(0, fathersname_val)

    tk.Label(edit_win, text="Address",bg="black",fg="white").pack(pady=5)
    address_entry = tk.Entry(edit_win)
    address_entry.pack()
    address_entry.insert(0, address_val)

    tk.Label(edit_win, text="Email",bg="black",fg="white").pack(pady=5)
    email_entry = tk.Entry(edit_win)
    email_entry.pack()
    email_entry.insert(0, email_val)

#for saving the edit details
    def save_changes():
        new_fullname = fullname_entry.get()
        new_father = father_entry.get()
        new_address = address_entry.get()
        new_email = email_entry.get()

        try:
            query = """
                UPDATE data4
                SET fullname=%s, fathersname=%s, address=%s, email=%s
                WHERE fullname=%s
            """
            values = (new_fullname, new_father, new_address, new_email, fullname)
            cursor.execute(query, values)
            mycon.commit()
            #messagebox for profile updated after editing
            messagebox.showinfo("Success", "Profile updated successfully!")
            edit_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {e}")

    bb2=tk.Button(edit_win, text="Save Changes", command=save_changes,bg="sky blue",font="arial 15 bold",fg="blue")
    bb2.pack(pady=20)

#sign up window
def another():
    root2 = tk.Toplevel(root)
    root2.geometry("500x400")
    root2.title("Sign Up Page")

    try:
        #bg image added to sign up page where user have to fill all the details
        print("Trying to load background image...")
        bg_image2 = Image.open(r"C:\Users\Lenovo\Desktop\login.jpg").resize((500, 400))
        bg_photo2 = ImageTk.PhotoImage(bg_image2)
        bg_label2 = tk.Label(root2, image=bg_photo2)
        bg_label2.image = bg_photo2
        bg_label2.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image not found:", e)

    def next(event): #on clicking enter cursor will move to another line 
        event.widget.tk_focusNext().focus()
        return "break" 

#details required for creating profile
    label1=tk.Label(root2, text="Fullname", fg="blue", bg="white")
    label1.place(x=80, y=40)

    entry1 = tk.Entry(root2)
    entry1.place(x=180, y=40)
    entry1.bind("<Return>", next) 

    label2=tk.Label(root2, text="Father's Name", fg="blue", bg="white")
    label2.place(x=80, y=80)

    entry2 = tk.Entry(root2)
    entry2.place(x=180, y=80)
    entry2.bind("<Return>", next)

    label3=tk.Label(root2, text="Password", fg="blue", bg="white")
    label3.place(x=80, y=120)

    entry3 = tk.Entry(root2)
    entry3.place(x=180, y=120)
    entry3.bind("<Return>", next)

    label4=tk.Label(root2, text="Address", fg="blue", bg="white")
    label4.place(x=80, y=160)
 
    entry4 = tk.Entry(root2)
    entry4.place(x=180, y=160)
    entry4.bind("<Return>", next)

    label5=tk.Label(root2, text="Email", fg="blue", bg="white")
    label5.place(x=80, y=200)

    entry5 = tk.Entry(root2)
    entry5.place(x=180, y=200)
    entry5.bind("<Return>", next)

#messagebox for sign up page window 
    def mess():
        fullname = entry1.get()
        fathersname = entry2.get()
        psswd = entry3.get()
        address = entry4.get()
        email = entry5.get()

        if not (fullname and fathersname and psswd and address and email):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not psswd.isdigit() or len(psswd) != 6:
            messagebox.showerror("Error", "Password must be exactly 6 digits.")
            return
        
        #save the filled details to sql
        try:
            query = "INSERT INTO data4 (fullname, fathersname, psswd, address, email) VALUES (%s, %s, %s, %s, %s)"
            values = (fullname, fathersname, psswd, address, email)
            cursor.execute(query, values)
            mycon.commit()
            messagebox.showinfo("Success", "Data has been saved :)")
            root2.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")

#submit button for submitting the details
    tk.Button(root2, text="Submit", bg="black", fg="white", font="arial 15 bold", command=mess).place(x=180, y=240)

def movefocus(event): #on clicking enter move the cursor to another line
    event.widget.tk_focusNext().focus()
    return "break"

label=tk.Label(root, text="Sign in", bg="black", fg="white", font="arial 18 bold").place(x=200, y=80)

#required details for login
l1=tk.Label(root, text="USERNAME", fg="blue", bg="white", font="arial 15 bold", bd=6)
l1.place(x=50, y=150)

e1 = tk.Entry(root, width=25, border=0, font="arial 11 bold", fg="black")
e1.place(x=200, y=150)
e1.bind("<Return>", movefocus)

l2=tk.Label(root, text="PASSWORD", fg="blue", bg="white", font="arial 15 bold", bd=6)
l2.place(x=50, y=200)

e2 = tk.Entry(root, width=25, border=0, font="arial 11 bold", fg="black", show="*")
e2.place(x=200, y=200)
e2.bind("<Return>", movefocus)

l3=tk.Button(root, text="LOGIN", bg="white", fg="red", font="arial 15 bold", cursor="hand2", command=login)
l3.place(x=200, y=250)

l4=tk.Label(root, text="Don't have an account?", fg="black", font="arial 7 bold")
l4.place(x=160, y=300)

l5=tk.Button(root, text="Sign up", fg="blue", bg="white", font="arial 7 bold", cursor="hand2", command=another)
l5.place(x=280, y=300)

root.mainloop()
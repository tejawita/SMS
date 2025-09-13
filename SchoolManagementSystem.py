
#importing required libraries
import tkinter as tk
import sqlite3
from tkinter import messagebox
import os
from tkinter import ttk


# Tkinter theme
window = tk.Tk()
window.configure(background="#000d66")

# Set logo to application for macOS
img = tk.Image('photo', file=os.path .join(os.path.dirname(__file__), "DataFlair.png"))
window.tk.call( 'wm','iconphoto', window._w, img)

# Set icon to application for Windows
window.iconbitmap(os.path.join(os.path.dirname(__file__), "DataFlair.ico"))

# Set window size
window.geometry("1280x720")

# Set window title
window.title("DataFlair - School Management System")


# Connect to database
mydb = sqlite3.connect(os.path.join(os.path.dirname(__file__), "Student.db")) 

# Create a cursor to execute SQL commands
cursor = mydb.cursor() 

# Create a table in database if not exists
cursor.execute('''
create table if not exists student (
    Name varchar(50) NOT NULL, 
    ID varchar(20) NOT NULL PRIMARY KEY,
    Grade varchar(10) NOT NULL, 
    Sex varchar(10) NOT NULL, 
    date varchar(5) NOT NULL, 
    Month varchar(5) NOT NULL, 
    Year varchar(6) NOT NULL,
    Degree varchar(10) NOT NULL,
    Stream varchar(50) NOT NULL,
    Phone varchar(20) NOT NULL,
    Email varchar(50) NOT NULL UNIQUE,
    Address varchar(150) NOT NULL
    )
    ''')



var = 0 # Variable for radio button

sex = "none" # Variable for gender 

# If female radio button is selected then
# value of sex variable will be set to "Female"
def female_selected(): 
    global sex
    sex = "Female"
    return sex


# If male radio button is selected then
# value of sex variable will be set to "Male"
def male_selected():
    global sex
    sex = "Male"
    return sex


# Add student information to database
def add_info():
    global sex
    name = Entry_Student_Name.get()
    grade = Entry_Grade.get()
    sex = sex
    id = Entry_Student_ID.get()
    date = Entry_Date.get()
    month = Entry_Month.get()
    year = Entry_Year.get()
    degree = Entry_Degree.get()
    stream = Entry_Stream.get()
    phone = Entry_Phone_Number.get()
    email = Entry_Email.get()
    address = Entry_Address.get(1.0, "end-1c")

    #Here proceedOrNot is a variable which is used to store the return value of askyesno() method
    #askyesno() method is used to display a dialog box with yes and no button
    #If yes button is clicked then it returns 1 else it returns 0
    proceedOrNot = messagebox.askyesno("Student Adding", "Are You Sure add Student \nName = {}\nId = {}\nGrade = {}\nSex = {}\ndate = {}/{}/{}\nDegree = {}\nStream = {}\nPhone = {}\nEmail = {}\nAddress = {}".format(name, id, grade, sex, date, month, year, degree, stream, phone, email, address))

    if proceedOrNot == 1:

        # Inserting data into database
        cursor.execute("insert into student values ('"+name+"', '"+id+"', '"+grade+"', '"+sex+"', '"+date+"', '"+month+"', '"+year+"' , '"+degree+"', '"+stream+"', '"+phone+"', '"+email+"', '"+address+"')")
        
        # Displaying a message box if data is inserted successfully
        messagebox.showinfo("Student Adding", "Successfully added Student \nName = {}\nId = {}\nGrade = {}\nSex = {}\ndate = {}/{}/{}\nDegree = {}\nStream = {}\nPhone = {}\nEmail = {}\nAddress = {}".format(name, id, grade, sex, date, month, year, degree, stream, phone, email, address))
        
        # Commiting changes to database
        mydb.commit()

    else:

        # Displaying a message box if data is not inserted successfully
        messagebox.showinfo("Unsuccessfull", "Cancelled")


# Function to update student information
def delete_student():

    # Getting id of student to delete
    id = Entry_Student_ID.get()

    #Here proceedOrNot is a variable which is used to store the return value of askyesno() method
    proceedOrNot = messagebox.askyesno("Student Information", "Delete Student ?\nId = {} ".format(id))

    if proceedOrNot == 1:

        # Deleting student information from database
        cursor.execute(" delete from student where id = '"+id+"' ")

        # Commiting changes to database
        mydb.commit()

        # Displaying a message box if data is deleted successfully
        messagebox.showinfo("Deleting Student", "Successfully deleted Student \n Id = {}".format(id))
    else:

        # Displaying a message box if data is not deleted successfully
        messagebox.showinfo("Unsuccessfully", "Canceled")


# Function to reset all fields
def reset_info():
    Entry_Student_ID.delete(0, 40)
    Entry_Student_Name.delete(0,40)
    Entry_Grade.delete(0, 40)
    Entry_Student_ID.delete(0, 40)
    Entry_Date.delete(0, 40)
    Entry_Month.delete(0, 40)
    Entry_Year.delete(0, 40)
    Entry_Degree.delete(0, 40)
    Entry_Stream.delete(0, 40)
    Entry_Phone_Number.delete(0, 40)
    Entry_Email.delete(0, 40)
    Entry_Address.delete(1.0, "end-1c")


# Function to update student informations displayed in treeview
def refresh_info():
    # Deleting previous data from treeview
    tree.delete(*tree.get_children())

    # Fetching data from database
    cursor.execute("select * from student")

    for i in cursor:
        #inserting data into treeview. Start from 0
        tree.insert("", 0, text=i[0], values=(i[1], i[2], i[3], i[4]+" - "+i[5]+" - "+i[6], i[7], i[8], i[9], i[10], i[11]))


# Function to search student information from database
def search_info():
    id = Entry_Student_ID.get()
    name = Entry_Student_Name.get()
    email = Entry_Email.get()

    # Deleting previous data from treeview
    if tree2.get_children() != ():
        tree2.delete(*tree2.get_children())

    # Fetching data from database
    cursor.execute("select * from student where id = '"+id+"' or Email = '"+email+"' or name like '"+name+"%' ")

    for i in cursor:
        #inserting data into treeview. Start from 0
        tree2.insert("", 0, text=i[0], values=(i[1], i[2], i[3], i[4]+" - "+i[5]+" - "+i[6], i[7], i[8], i[9], i[10], i[11]))



#------------------------------------------------  Creating UI  ------------------------------------------------

# Creating a label for title
Label_School = tk.Label()
Label_School.place(relx=0.0, rely=0.0, height=60, width=1358)
Label_School.configure(background="#73d3ff", foreground="#0d1160", font="-family {OCR A Std} -size 30 -weight bold", text="DataFlair - Student Management System",anchor="center")

# Creating a label Frame for Student's Information
Left_Student_Information = tk.LabelFrame()
Left_Student_Information.place(relx=0.004, rely=0.099, relheight=0.800, relwidth=0.377)
Left_Student_Information.configure(relief='groove', text='''Student's Information''', font="-family {Segoe UI} -size 18 -weight bold -slant italic ", foreground="black", background="#7bffa7")

# Creating label for Student's ID
Student_ID = tk.Label(Left_Student_Information)
Student_ID.place(relx=0.077, rely=0.080, height=31, width=160, bordermode='ignore')
Student_ID.configure(background="#613b84", font="-family {Segoe UI} -size 17", foreground="white", text="Student's ID", anchor="center" )

# Creating label for Student's Name
Student_Name = tk.Label(Left_Student_Information)
Student_Name.place(relx=0.077, rely=0.165, height=31, width=160, bordermode='ignore')
Student_Name.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Student Name", anchor="center")

# Creating label for Student's Grade
Grade = tk.Label(Left_Student_Information)
Grade.place(relx=0.077, rely=0.250, height=31, width=160, bordermode='ignore')
Grade.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Grades", anchor="center")

# Creating label for Student's gender
Sex = tk.Label(Left_Student_Information)
Sex.place(relx=0.077, rely=0.335, height=31, width=160, bordermode='ignore')
Sex.configure(background="#613b84", font="-family {Segoe UI} -size 17", foreground="white", text="Gender", anchor="center")

# Creating label for Student's Date of Birth
Date_of_Birth = tk.Label(Left_Student_Information)
Date_of_Birth.place(relx=0.077, rely=0.420, height=31, width=160, bordermode='ignore')
Date_of_Birth.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Date of Birth", anchor="center" )

# Creating label for Student's Degree
Degree = tk.Label(Left_Student_Information)
Degree.place(relx=0.077, rely=0.505, height=31, width=160, bordermode='ignore')
Degree.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Degree", anchor="center" )

# Creating label for Student's Stream
Stream = tk.Label(Left_Student_Information)
Stream.place(relx=0.077, rely=0.590, height=31, width=160, bordermode='ignore')
Stream.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Stream", anchor="center" )

# Creating label for Student's Phone Number
Phone_Number = tk.Label(Left_Student_Information)
Phone_Number.place(relx=0.077, rely=0.675, height=31, width=160, bordermode='ignore')
Phone_Number.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Phone Number", anchor="center" )

# Creating label for Student's Email
Email = tk.Label(Left_Student_Information)
Email.place(relx=0.077, rely=0.760, height=31, width=160, bordermode='ignore')
Email.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Email", anchor="center" )

# Creating label for Student's Address
Address = tk.Label(Left_Student_Information)
Address.place(relx=0.077, rely=0.845, height=31, width=160, bordermode='ignore')
Address.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Address", anchor="center" )


# Creating input field for Student's ID
Entry_Student_ID = tk.Entry(Left_Student_Information)
Entry_Student_ID.place(relx=0.442, rely=0.080, height=30, relwidth=0.488, bordermode='ignore')
Entry_Student_ID.configure(background="black",font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Student_ID.insert(0, "Enter Student ID")
Entry_Student_ID.bind("<FocusIn>", lambda args: Entry_Student_ID.delete('0', 'end'))

# Creating input field for Student's Name
Entry_Student_Name = tk.Entry(Left_Student_Information)
Entry_Student_Name.place(relx=0.442, rely=0.165, height=29, relwidth=0.488, bordermode='ignore')
Entry_Student_Name.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Student_Name.insert(0, "Enter Student Name")
Entry_Student_Name.bind("<FocusIn>", lambda args: Entry_Student_Name.delete('0', 'end'))

# Creating input field for Student's Grade
Entry_Grade = tk.Entry(Left_Student_Information)
Entry_Grade.place(relx=0.442, rely=0.250, height=29, relwidth=0.488, bordermode='ignore')
Entry_Grade.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Grade.insert(0, "Enter Student Grade")
Entry_Grade.bind("<FocusIn>", lambda args: Entry_Grade.delete('0', 'end'))


# Creating radio button for selecting Student's gender
Radiobutton_Sex_Male = tk.Radiobutton(Left_Student_Information)
Radiobutton_Sex_Male.place(relx=0.442, rely=0.33, relheight=0.059, relwidth=0.217, bordermode='ignore')
Radiobutton_Sex_Male.configure(text="Male", variable=var, value=1, command=male_selected, state="active", background="#7bffa7", foreground="black")

Radiobutton_Sex_Female = tk.Radiobutton(Left_Student_Information)  
Radiobutton_Sex_Female.place(relx=0.673, rely=0.335, relheight=0.059, relwidth=0.252, bordermode='ignore')
Radiobutton_Sex_Female.configure(text="Female", variable=var, value=2, command=female_selected,state= "normal", background="#7bffa7", foreground="black")


# Creating input fields for Student's Date of Birth
#--------------------------------------------------
Entry_Date = tk.Entry(Left_Student_Information)
Entry_Date.place(relx=0.442, rely=0.420, relheight=0.059, relwidth=0.106, bordermode='ignore')
Entry_Date.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Date.insert(0, "DD")
Entry_Date.bind("<FocusIn>", lambda args: Entry_Date.delete('0', 'end'))

Entry_Month = tk.Entry(Left_Student_Information)
Entry_Month.place(relx=0.577, rely=0.420, relheight=0.059, relwidth=0.125, bordermode='ignore')
Entry_Month.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Month.insert(0, "MM")
Entry_Month.bind("<FocusIn>", lambda args: Entry_Month.delete('0', 'end'))

Entry_Year = tk.Entry(Left_Student_Information)
Entry_Year.place(relx=0.731, rely=0.420, relheight=0.059, relwidth=0.183, bordermode='ignore')
Entry_Year.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Year.insert(0, "YYYY")
Entry_Year.bind("<FocusIn>", lambda args: Entry_Year.delete('0', 'end'))
#-----------------------------------------------------


# Creating input field for Student's Degree
Entry_Degree = tk.Entry(Left_Student_Information)
Entry_Degree.place(relx=0.442, rely=0.505, height=29, relwidth=0.488, bordermode='ignore')
Entry_Degree.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Degree.insert(0, "Enter Student Degree")
Entry_Degree.bind("<FocusIn>", lambda args: Entry_Degree.delete('0', 'end'))

# Creating input field for Student's Stream
Entry_Stream = tk.Entry(Left_Student_Information)
Entry_Stream.place(relx=0.442, rely=0.590, height=29, relwidth=0.488, bordermode='ignore')
Entry_Stream.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Stream.insert(0, "Enter Student Stream")
Entry_Stream.bind("<FocusIn>", lambda args: Entry_Stream.delete('0', 'end'))

# Creating input field for Student's Phone Number
Entry_Phone_Number = tk.Entry(Left_Student_Information)
Entry_Phone_Number.place(relx=0.442, rely=0.675, height=29, relwidth=0.488, bordermode='ignore')
Entry_Phone_Number.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Phone_Number.insert(0, "Enter Student Phone Number")
Entry_Phone_Number.bind("<FocusIn>", lambda args: Entry_Phone_Number.delete('0', 'end'))

# Creating input field for Student's Email
Entry_Email = tk.Entry(Left_Student_Information)
Entry_Email.place(relx=0.442, rely=0.760, height=29, relwidth=0.488, bordermode='ignore')
Entry_Email.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")
Entry_Email.insert(0, "Enter Student Email")
Entry_Email.bind("<FocusIn>", lambda args: Entry_Email.delete('0', 'end'))

# Creating input field for Student's Address
Entry_Address = tk.Text(Left_Student_Information)
Entry_Address.place(relx=0.442, rely=0.845, relheight=0.1, relwidth=0.488, bordermode='ignore')
Entry_Address.configure(background="black",  font="-family {Segoe UI} -size 14 -weight bold", foreground="white")


# Creating frame for the right side of the window
Frame_right = tk.Frame()
Frame_right.place(relx=0.388, rely=0.099, relheight=0.890, relwidth=0.607)
Frame_right.configure(relief='groove', borderwidth="2", background="#Fd7c45")

# Creating a listbox inside the frame
upper_box = tk.Listbox(Frame_right)
upper_box.place(relx=0.020, rely=0.100, relheight=0.300, relwidth=0.960)

# Creating a label for the listbox
label = tk.Label(Frame_right)
label.place(relx=0.020, rely=0.050, relheight=0.050, relwidth=0.960)
label.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Student Database Information", anchor="center")

# Creating column tree inside the listbox
tree = ttk.Treeview(upper_box, columns=('ID', ' Name', 'Grade', 'Gender', 'Date of Birth', 'Degree', 'Stream', 'Phone Number', 'Email', 'Address'))
tree.place(relx=0.020, rely=0.100, relheight=0.300, relwidth=0.960)
tree.heading('#0', text='Name')
tree.heading('#1', text='ID')
tree.heading('#2', text='Grade')
tree.heading('#3', text='Gender')
tree.heading('#4', text='Date of Birth')
tree.heading('#5', text='Degree')
tree.heading('#6', text='Stream')
tree.heading('#7', text='Phone Number')
tree.heading('#8', text='Email')
tree.heading('#9', text='Address')
tree.column('#0', width=150, anchor='center')
tree.column('#1', width=50, anchor='center')
tree.column('#2', width=60, anchor='center')
tree.column('#3', width=60, anchor='center')
tree.column('#4', width=100, anchor='center')
tree.column('#5', width=70, anchor='center')
tree.column('#6', width=60, anchor='center')
tree.column('#7', width=90, anchor='center')
tree.column('#8', width=120, anchor='center')
tree.column('#9', width=120, anchor='center')
tree.pack()


# Creating second listbox inside the frame
lower_box = tk.Listbox(Frame_right)
lower_box.place(relx=0.020, rely=0.600, relheight=0.300, relwidth=0.960)
lower_box.configure(background="black", font="-family {Segoe UI} -size 14", foreground="white", highlightbackground="white", highlightcolor="black")

#create a label for the listbox
label2 = tk.Label(Frame_right)
label2.place(relx=0.020, rely=0.550, relheight=0.050, relwidth=0.960)
label2.configure(background="#613b84",  font="-family {Segoe UI} -size 17", foreground="white", text="Student Search Information", anchor="center")

# Creating column tree inside the listbox
tree2 = ttk.Treeview(lower_box, columns=('ID', ' Name', 'Grade', 'Gender', 'Date of Birth', 'Degree', 'Stream', 'Phone Number', 'Email', 'Address'))
tree2.place(relx=0.020, rely=0.600, relheight=0.300, relwidth=0.960)
tree2.heading('#0', text='Name')
tree2.heading('#1', text='ID')
tree2.heading('#2', text='Grade')
tree2.heading('#3', text='Gender')
tree2.heading('#4', text='Date of Birth')
tree2.heading('#5', text='Degree')
tree2.heading('#6', text='Stream')
tree2.heading('#7', text='Phone Number')
tree2.heading('#8', text='Email')
tree2.heading('#9', text='Address')
tree2.column('#0', width=150, anchor='center')
tree2.column('#1', width=50, anchor='center')
tree2.column('#2', width=60, anchor='center')
tree2.column('#3', width=60, anchor='center')
tree2.column('#4', width=100, anchor='center')
tree2.column('#5', width=70, anchor='center')
tree2.column('#6', width=60, anchor='center')
tree2.column('#7', width=90, anchor='center')
tree2.column('#8', width=120, anchor='center')
tree2.column('#9', width=120, anchor='center')
tree2.pack()


# Creating a frame for the action buttons
Button_Frame = tk.Frame()
Button_Frame.place(relx=0.004, rely=0.890, relheight=0.10, relwidth=0.377)
Button_Frame.configure(relief='groove', borderwidth="2", background="#E4a400")

# Creating add buttons to add student information into the database
Button_ADD = tk.Button(Button_Frame)
Button_ADD.place(relx=0.020, rely=0.200, height=40, width=70)
Button_ADD.configure(background="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''ADD''', command=add_info)

# Creating search buttons to search student information in the database
Button_SEARCH = tk.Button(Button_Frame)
Button_SEARCH.place(relx=0.200, rely=0.200, height=40, width=85)
Button_SEARCH.configure(background="#b423d8", borderwidth="5",  font="-family {Segoe UI} -size 14", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''SEARCH''', command=search_info)

# Creating update buttons to update student information in the database view
Button_REFRESH = tk.Button(Button_Frame)
Button_REFRESH.place(relx=0.410, rely=0.200, height=40, width=85)
Button_REFRESH.configure(background="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''REFRESH''', command=refresh_info)

# Creating update buttons to update student information in the database
Button_DELETE = tk.Button(Button_Frame)
Button_DELETE.place(relx=0.610, rely=0.200, height=40, width=80)
Button_DELETE.configure(background="#b423d8", borderwidth="5",  font="-family {Segoe UI} -size 14", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''DELETE''', command=delete_student)

# Creating update buttons to update student information in the database
Button_RESET = tk.Button(Button_Frame)
Button_RESET.place(relx=0.815, rely=0.200, height=40, width=80)
Button_RESET.configure(background="#b423d8", borderwidth="5",  font="-family {Segoe UI} -size 14", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''RESET''', command=reset_info)




# This function call will refresh the database view when we open the application
refresh_info()

# This will run the mainloop of the application
window.mainloop()

from tkinter import *
from tkinter import messagebox
import sqlite3


class Root(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.root = root
        self.photo = PhotoImage(file="Images/tagicon.png")
        self.root.iconphoto(False,self.photo)
        self.root.title("Employee Tracker")
        self.root.resizable(0,0)
        self.root_width = 450
        self.root_height = 400
        self.root.geometry(f"{self.root_width}x{self.root_height}")
        self.create_buttons()
        self.create_entries()

        # creating the table

        try:
            conn = sqlite3.connect("employees.db")

            c = conn.cursor()
            c.execute("""CREATE TABLE employees (fname text, lname text, pay integer)""")
            conn.commit()
            conn.close()
        except:
            pass

    def create_buttons(self):
        self.my_frame = Frame(self.root,bg="black",width=100,height=100)
        self.my_frame.place(x=0,y=self.root_height-80,height=80,width=450)

        self.save_btn = Button(self.my_frame,bg="#FFAE01",text="SAVE",width=12,fg='black',command=self.save_record)
        self.save_btn.pack(side=LEFT,padx=10)

        self.show_btn = Button(self.my_frame,bg="#FFAE01",text="SHOW",width=12,fg='black',command=self.show_records)
        self.show_btn.pack(side=LEFT,padx=10)

        self.delete_btn = Button(self.my_frame,bg="#FFAE01",text="DELETE",width=12,fg='black',command=self.delete_record)
        self.delete_btn.pack(side=LEFT,padx=10)
        try:
            self.update_btn = Button(self.my_frame,bg='#FFAE01',text="UPDATE",width=12,fg='black',relief=FLAT,command=self.update_records)
            self.update_btn.pack(side=LEFT,padx=10)
        except:
            messagebox.showwarning(title="Not enough entry",message="You have to enter both the name and the surname in order to update the pay")

    def create_entries(self):
        self.my_title = Label(self.root,bg="#FFAE01",fg='black',text="Employee Tracker",font=("arial",17,"bold"))
        self.my_title.place(x=0,y=0,width=self.root_width,height=30)

        self.container = LabelFrame(self.root,text="Entries",fg="orange",bg="black")
        self.container.place(x=10,y=40,width=self.root_width-20,height=270)

        self.pay_label = Label(self.container,text="Enter the name of Employee:",fg="orange",bg="black")
        self.pay_label.place(x=0,y=30,width=190,height=50)

        self.pay_label = Label(self.container,text="Enter the surname of Employee:",fg="orange",bg="black")
        self.pay_label.place(x=0,y=90,width=190,height=50)

        self.pay_label = Label(self.container,text="Enter the payment of Employee:",fg="orange",bg="black")
        self.pay_label.place(x=0,y=150,width=190,height=50)

        self.fname_entry = Entry(self.container, bg="orange", fg="black", font=("arial", 14))
        self.fname_entry.place(x=230, y=40, width=140, height=30)

        self.lname_entry = Entry(self.container, bg="orange", fg="black", font=("arial", 14))
        self.lname_entry.place(x=230, y=100, width=140, height=30)

        self.pay_entry = Entry(self.container,bg="orange",fg="black",font=("arial",14))
        self.pay_entry.place(x=230,y=160,width=140,height=30)

    def save_record(self):
        conn = sqlite3.connect("employees.db")
        c = conn.cursor()
        if self.fname_entry.get() == "" or self.lname_entry.get() == "" or self.pay_entry.get() == "":
            messagebox.showerror(message="All the entries should be given",title="Entry Error")
        else:
            c.execute("INSERT INTO employees VALUES(:fname,:lname,:pay)",
                      {"fname":self.fname_entry.get(),"lname":self.lname_entry.get(),"pay":self.pay_entry.get()})
            conn.commit()
        conn.close()
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.pay_entry.delete(0, END)


    def show_records(self):
        show = Tk()
        show.title("Records")
        show_width = 300
        show_height = 230
        show.iconbitmap("Images/paintlogo.ico")
        show.geometry(f"{show_width}x{show_height}")
        conn = sqlite3.connect("employees.db")
        c = conn.cursor()
        c.execute("""SELECT * FROM employees""")

        record_frame = LabelFrame(show,text="Records",bg="black",fg="orange")
        record_frame.place(x=15,y=15,width=show_width-30,height=show_height-30)

        employee_records = c.fetchall()
        for record in employee_records:
            employee = str(employee_records.index(record)+1) + ". | " + record[0] + " | " + record[1] + " | " + str(record[2])
            employee_label = Label(record_frame,text=employee,bg="black",fg="orange")
            employee_label.pack()

        show.mainloop()

    def delete_record(self):
        conn = sqlite3.connect("employees.db")
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE fname=:fname AND lname=:lname AND pay=:pay",{"fname": self.fname_entry.get(),"lname": self.lname_entry.get(),"pay":self.pay_entry.get()})
        conn.commit()
        conn.close()
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.pay_entry.delete(0, END)

    def update_records(self):
        update = Tk()
        update.iconbitmap("Images/paintlogo.ico")
        update.title("Update Employee")
        update.resizable(0,0)
        update_width = 450
        update_height = 400
        update.geometry(f"{update_width}x{update_height}")

        def savenew():
            conn = sqlite3.connect("employees.db")
            c = conn.cursor()

            c.execute("UPDATE employees SET pay=:pay WHERE lname=:lname AND fname=:fname",{"fname":self.fname_entry.get(),"pay":pay_entry.get(),"lname":self.lname_entry.get()})

            conn.commit()
            conn.close()

            self.fname_entry.delete(0, END)
            self.lname_entry.delete(0, END)
            self.pay_entry.delete(0, END)

            update.destroy()

        conn = sqlite3.connect("employees.db")
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE lname=:lname AND fname = :fname",{"lname": self.lname_entry.get(),"fname":self.fname_entry.get()})
        conn.commit()
        record = c.fetchone()
        conn.commit()


        my_frame = Frame(update, bg="black", width=100, height=100)
        my_frame.place(x=0, y=self.root_height - 80, height=80, width=450)

        submit_btn = Button(my_frame, bg='#FFAE01', text="SUBMIT", width=90, fg='black', relief=FLAT,command=savenew)
        submit_btn.pack(side=LEFT, padx=10)

        my_title = Label(update, bg="#FFAE01", fg='black', text="Update Employee", font=("arial", 17, "bold"))
        my_title.place(x=0, y=0, width=update_width, height=30)

        container = LabelFrame(update, text="Entries", fg="orange", bg="black")
        container.place(x=10, y=40, width=update_width - 20, height=270)

        pay_label = Label(container, text="Enter the name of Employee:", fg="orange", bg="black")
        pay_label.place(x=0, y=30, width=190, height=50)

        pay_label = Label(container, text="Enter the surname of Employee:", fg="orange", bg="black")
        pay_label.place(x=0, y=90, width=190, height=50)

        pay_label = Label(container, text="Enter the payment of Employee:", fg="orange", bg="black")
        pay_label.place(x=0, y=150, width=190, height=50)

        fname_entry = Entry(container, bg="orange", fg="black", font=("arial", 14))
        fname_entry.insert(0,record[0])
        fname_entry.place(x=230, y=40, width=140, height=30)

        lname_entry = Entry(container, bg="orange", fg="black", font=("arial", 14))
        lname_entry.insert(0,record[1])
        lname_entry.place(x=230, y=100, width=140, height=30)

        pay_entry = Entry(container, bg="orange", fg="black", font=("arial", 14))
        pay_entry.insert(0,record[2])
        pay_entry.place(x=230, y=160, width=140, height=30)

        conn.close()
        update.mainloop()


if __name__ == '__main__':
    root = Tk()
    Root(root)
    root.mainloop()
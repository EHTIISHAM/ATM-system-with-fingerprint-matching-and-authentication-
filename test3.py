import os
import cv2
import time
import random
import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox

#DB connection
conn = sqlite3.connect('atm_database.db')
cursor = conn.cursor()


def loginid():
    global user_id
    user_id = id_entry.get()
    if user_id.isdigit():
        id_frame.pack_forget()
        sp_frame.pack(expand=True)
        result_label.config(text="")
        sresult_label.config(text=f"")
        id_entry.delete(0, tk.END)

    else:
        id_entry.delete(0, tk.END)
        sresult_label.config(text=f"")
        messagebox.showerror("Input Error","PLS Enter a numeric value")
        id_frame.pack()

def login():
    global user_id
    global password
    password = pass_entry.get()
    
    cursor.execute("SELECT password_hash, salt FROM security WHERE account_number = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        stored_password_hash, salt = result
        entered_password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
        
        if entered_password_hash == stored_password_hash:
            cursor.execute("SELECT account_holder, balance FROM accounts WHERE account_number = ?", (user_id,))
            account_info = cursor.fetchone()
            name, balance = account_info[0], account_info[1]
            pass_entry.delete(0,tk.END)
            sresult_label.config(text="")
            balance_label.config(text=f"Welcome Back {name}")
            sp_frame.pack_forget()
            balance_frame.pack(expand=True)
        else:
            pass_entry.delete(0,tk.END)
            result_label.config(text=f"")
            sresult_label.config(text=f"User not fount")
            sp_frame.pack_forget()
            id_frame.pack(expand=True)
            id_entry.delete(0,tk.END)

    else:
        pass_entry.delete(0,tk.END)
        sresult_label.config(text=f"User not fount")
        sp_frame.pack_forget()
        id_frame.pack(expand=True)
        id_entry.delete(0,tk.END)

def fp():
    cursor.execute("SELECT password_hash, salt FROM security WHERE account_number = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        fpid = str(user_id)
        rn = random.randrange(1,3)
        rn_str = str(rn)
        in_loc = ("INPUT/"+fpid+"_"+rn_str+".bmp")
        db_loc = ("FP_DB/"+fpid+".bmp")

        global load_img 
        load_img = cv2.imread(in_loc)

        bstscr = 0
        filen = None
        img = None
        kp1, kp2, mp = None, None, None

        fpimg = cv2.imread(db_loc)
        sift = cv2.SIFT_create()

        keyp1, desp1 = sift.detectAndCompute(load_img, None   )
        keyp2, desp2 = sift.detectAndCompute(fpimg, None   )

        matchs = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {}).knnMatch(desp1, desp2, k=2)

        matchp = []

        for p, q in matchs:
            if p.distance < 0.2* q.distance:
                matchp.append(p)

        keyp = 0
        if len(keyp1)<len(keyp2):
            keyp = len(keyp1)
        else:
            keyp = len(keyp2)

        if len(matchp) / keyp *100 > bstscr:
            bstscr = len(matchp) / keyp *100
            filen = db_loc
            img = fpimg
            kp1,kp2,mp = keyp1, keyp2 , matchp
            print("Best Match: " + filen)
            print("Score: " + str(bstscr))
        
            sp_frame.pack_forget()
            cursor.execute("SELECT account_holder, balance FROM accounts WHERE account_number = ?", (user_id,))
            account_info = cursor.fetchone()
            name, balance = account_info[0], account_info[1]
            balance_label.config(text=f"Welcome Back {name}")
            balance_frame.pack(expand=True)
            flabel.config(text="Matched")
            time.sleep(1)
            def res_show():

                res = cv2.drawMatches(load_img, kp1, img, kp2, mp, None)
                res = cv2.resize(res,None, fx=4, fy=4)
                cv2.imshow("result", res)
                cv2.waitKey(0)
                cv2.destroyAllWindows

            #res_show()

        else:
            flabel.config(text="Try again")
    else:
        pass_entry.delete(0,tk.END)
        sresult_label.config(text=f"User not fount")
        sp_frame.pack_forget()
        id_frame.pack(expand=True)
        id_entry.delete(0,tk.END)

def withdraw_money():
    amount = withdraw_entry.get()
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (user_id,))
    current_balance = cursor.fetchone()[0]
    if  amount.isdigit():
        amount = int(amount)
        if amount > current_balance and amount < 25001 and amount > 99:
            messagebox.showerror("Error", "Not enough balance")
        elif amount <= 25000 and amount >= 100:
            new_balance = current_balance - amount
            cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user_id))
            conn.commit()
            messagebox.showinfo("Withdrawal Successful", f"Withdrawal successful! New balance: Rs {new_balance}")
            withdraw_frame.pack_forget()
            end_frame.pack()
        else:
            messagebox.showinfo("Error","Input amount out of range")
            withdraw_entry.delete(0,tk.END)
    else:
        messagebox.showerror("Input Error","PLS Enter a numeric value")
        withdraw_entry.delete(0,tk.END)


def q1():
    qwithdraw(1000)
def q2():
    qwithdraw(5000)
def q3():
    qwithdraw(10000)
def q4():
    qwithdraw(20000)
def q5():
    qwithdraw(25000)

def qwithdraw(money):
    global user_id
    amount = int(money)
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (user_id,))
    current_balance = cursor.fetchone()[0]
    new_balance = current_balance - amount
    cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, user_id))
    conn.commit()
    messagebox.showinfo("Withdrawal Successful", f"Withdrawal successful! New balance: Rs {new_balance}")
    qwithdraw_frame.pack_forget()
    end_frame.pack()

def balancechk():
    global user_id
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (user_id))
    balance = cursor.fetchone()
    messagebox.showinfo("balance",f"Your Balance is: Rs {balance}")

def withdraw():
    balance_frame.pack_forget()
    withdraw_frame.pack(expand=True)

def qwithdrawf():
    balance_frame.pack_forget()
    qwithdraw_frame.pack(expand=True)

def backqw():
    balance_frame.pack(expand=True)
    qwithdraw_frame.pack_forget()

def backw():
    balance_frame.pack(expand=True)
    withdraw_frame.pack_forget()


def exit_program():
    root.destroy()



#frame 1 ((((

# Create the main window
root = tk.Tk()
root.title("Welcome Screen")
root.configure(background="black")
root.geometry("800x500")

# Create a frame for centering
id_frame = tk.Frame(root)
id_frame.configure(background="black")
id_frame.pack(expand=True)

# Create and center the "Welcome" label
welcome_label = tk.Label(id_frame, text="Welcome Back", font=("Helvetica", 70), fg="white", bg="black", pady= 10)
welcome_label.pack()

# Create and center the label for entering a number
text_label = tk.Label(id_frame, text="Enter a number:", font=("Helvetica", 25), fg="white", bg="black", pady=10)
text_label.pack()

# Create and center the entry box
id_entry = tk.Entry(id_frame,width=30,font=20)
id_entry.pack(ipady=8,ipadx=20,pady=(10,15))

# Create a frame for the buttons and center it
button_frame = tk.Frame(id_frame, pady=20)
button_frame.configure(background="black")
button_frame.pack()

# Create and center the "Enter" button
enter_button = tk.Button(button_frame, text="Enter", font=("Helvetica", 14), fg="white", bg="green", command=loginid )
enter_button.pack(side=tk.LEFT)

just_some_space = tk.Label(button_frame, text="             " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

# Create and center the "Exit" button
exit_button = tk.Button(button_frame,padx=10, text="Exit", font=("Helvetica", 14), fg="white", bg="red" ,command=exit_program)
exit_button.pack(side=tk.LEFT)

result_label = tk.Label(id_frame, text="", font=("Helvetica", 14), fg="white", bg="black" )
result_label.pack()

sresult_label = tk.Label(id_frame, text="", font=("Helvetica", 14), fg="white", bg="black" )
sresult_label.pack()

#))))frame 1 end  done


#frame 2 ((((
sp_frame = tk.Frame(root)
sp_frame.configure(background="black")
sp_frame.config(bg="black")

pass_label = tk.Label(sp_frame, text="Enter your password/PIN:", font=("Helvetica", 25), fg="white", bg="black",pady=25)
pass_label.pack()

pass_entry = tk.Entry(sp_frame,width=30,font=20,show='*')
pass_entry.pack(ipady=8,ipadx=20,pady=(10,15))

pass_button_frame = tk.Frame(sp_frame, pady=20)
pass_button_frame.configure(background="black")
pass_button_frame.pack()

pass_enter_button = tk.Button(pass_button_frame, text="Login", font=("Helvetica", 14), fg="white", bg="blue", command=login )
pass_enter_button.pack(side=tk.LEFT)

or_label = tk.Label(pass_button_frame, text="or use finger print", font=("Helvetica", 20), fg="white", bg="black", padx=10, pady=3)
or_label.pack(side=tk.LEFT)

finger_button = tk.Button(pass_button_frame, text="Fingerprint", font=("Helvetica", 14), fg="white", bg="green", command=fp)
finger_button.pack(side=tk.LEFT)

flabel = tk.Label(sp_frame, text="", font=("Helvetica", 25), fg="white", bg="black",pady=25)
flabel.pack()

#frame 2 end done  ))))


#frame 3 ((((

balance_frame = tk.Frame(root)
balance_frame.configure(background="black")
balance_frame.config(bg="black")

balance_label = tk.Label(balance_frame, text="", font=("Helvetica", 40), fg="white", bg="black", pady=20)
balance_label.pack()

balance_button_frame = tk.Frame(balance_frame , pady=20)
balance_button_frame.configure(background="black")
balance_button_frame.pack()

balance_check_button = tk.Button(balance_button_frame, text="Check balance", font=("Helvetica", 20), fg="black", bg="light green", command=balancechk,padx=10,pady=10)
balance_check_button.pack(side=tk.LEFT)

just_some_space = tk.Label(balance_button_frame, text="          " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

withdraw_button = tk.Button(balance_button_frame, text="Withdraw", font=("Helvetica", 20), fg="black", bg="light green", command=withdraw,padx=10,pady=10)
withdraw_button.pack(side=tk.LEFT)

just_some_space = tk.Label(balance_button_frame, text="          " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

quick_withdraw_button = tk.Button(balance_button_frame, text="Quick Withdraw", font=("Helvetica", 20), fg="black", bg="light green", command=qwithdrawf,padx=10,pady=10)
quick_withdraw_button.pack(side=tk.LEFT)

#frame 3 end ))))



#frame 4  ((((

withdraw_frame = tk.Frame(root)
withdraw_frame.configure(background="black")
withdraw_frame.config(bg="black")


withdraw_label = tk.Label(withdraw_frame, text="Enter the ammount", font=("Helvetica", 30), fg="white", bg="black", pady= 20)
withdraw_label.pack()

withdraw_entry = tk.Entry(withdraw_frame,width=30,font=20)
withdraw_entry.pack(ipady=8,ipadx=20,pady=(10,15))

just_some_space = tk.Label(withdraw_frame, text="          " , background= "black",pady= 11)
just_some_space.pack()

withdraw_button_frame = tk.Frame(withdraw_frame , pady=20)
withdraw_button_frame.configure(background="black")
withdraw_button_frame.pack()

withdraw_button = tk.Button(withdraw_button_frame, text="Enter", font=("Helvetica", 14), fg="white", bg="blue", command=withdraw_money, )
withdraw_button.pack(side=tk.LEFT)

just_some_space = tk.Label(withdraw_button_frame, text="          " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

backw_button = tk.Button(withdraw_button_frame, text="Back", font=("Helvetica", 14), fg="black", bg="light blue", command=backw)
backw_button.pack(side=tk.LEFT)

end_frame = tk.Frame(root)
end_frame.config(background='black')

thank_label = tk.Label(end_frame, text="Thanks For Visiting Our ATM",fg='white',bg='black')
thank_label.pack()
thank_label.config(font=('Arial' , 25, 'bold' ),pady=(50))

def retrun():
    end_frame.pack_forget()
    id_frame.pack(expand=True)
    id_entry.delete(0,tk.END)
Thanks_btn = tk.Button(end_frame,text='exit' ,bg='white',fg='black',width=20,command=retrun)
Thanks_btn.pack(ipady=8,pady=(20,20))
Thanks_btn.config(font=('Arial', 15 ))

#frame 4 end ))))


#frame 5 ((((

qwithdraw_frame = tk.Frame(root)
qwithdraw_frame.configure(background="black")
qwithdraw_frame.config(bg="black")

just_some_space = tk.Label(qwithdraw_frame, text="Select one" , fg="white" , font= ("Helvetica", 30), background= "black",pady= 11)
just_some_space.pack()

qwithdraw_button_frame = tk.Frame(qwithdraw_frame , pady=20)
qwithdraw_button_frame.configure(background="black")
qwithdraw_button_frame.pack()


q1_button = tk.Button(qwithdraw_button_frame, text="1000", font=("Helvetica", 14), fg="white", bg="blue", command=q1,padx=7)
q1_button.pack(side=tk.LEFT)

just_some_space = tk.Label(qwithdraw_button_frame, text="       " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

q2_button = tk.Button(qwithdraw_button_frame, text="5000", font=("Helvetica", 14), fg="white", bg="blue", command=q2,padx=7)
q2_button.pack(side=tk.LEFT)

just_some_space = tk.Label(qwithdraw_button_frame, text="       " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

q3_button = tk.Button(qwithdraw_button_frame, text="10000", font=("Helvetica", 14), fg="white", bg="blue", command=q3)
q3_button.pack(side=tk.LEFT)

just_some_space = tk.Label(qwithdraw_button_frame, text="       " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

q4_button = tk.Button(qwithdraw_button_frame, text="20000", font=("Helvetica", 14), fg="white", bg="blue", command=q4)
q4_button.pack(side=tk.LEFT)

just_some_space = tk.Label(qwithdraw_button_frame, text="       " , background= "black",pady= 11)
just_some_space.pack(side=tk.LEFT)

q5_button = tk.Button(qwithdraw_button_frame, text="25000", font=("Helvetica", 14), fg="white", bg="blue", command=q5)
q5_button.pack(side=tk.LEFT)

backw_button = tk.Button(qwithdraw_frame, text="Back", font=("Helvetica", 14), fg="black", bg="light blue", command=backqw)
backw_button.pack()

#frame 5 end))))

root.mainloop()

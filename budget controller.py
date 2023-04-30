# this Budget Controller is developed by Ebrahim Ramadan - ID:320220029
from packages import *


c = sqlite3.connect('aya_budget.sqlite3')
conn = c.cursor()
# create initial table
conn.execute('''CREATE TABLE IF NOT EXISTS Budget
                   (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT,
                    name TEXT,
                    income REAL)''')
c.commit()
# c (the real connection) => for commits, while
# conn (the cursor object) => for executes


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("Budget Controller for Students")
        self.photo = None
        self.BGessentials()

    def BGessentials(self):
        img = Image.open("Picture1-removebg-preview.png")
        img = img.resize((200, 200))
        self.photo = ImageTk.PhotoImage(img)
        # i had to save the bg pic as class instance var
        # ceated a label with the PhotoImage obj and placed it behind all other widgets (as a bg) I preferred that way instead of using canvas bg implementation option but still valid ok
        background_label = tk.Label(self, image=self.photo)
        background_label.place(x=-135, y=-70, relwidth=1, relheight=1)

        BIG_font = font.Font(family="Hero", size=20, weight="bold")
        self.smoll_font = font.Font(family="Hero", size=10, weight="bold")
        self.median_font = font.Font(family="Hero", size=12, weight="bold")

        monthlyLABEL = ttk.Label(
            self, text='MONTHLY \n BUDGET', font=BIG_font)
        monthlyLABEL.place(x=100, y=50)

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
        # I don't knwo I used optionsArea before & didn't like bc it couldn't easily retrive the selected val (I don't like implementing StringVar())
        # SO I used combobox (3a4ra / 3a4ra)
        style = ttk.Style()
        style.configure("TCombobox", padding=7, width=25)
        # month_var = tk.StringVar()
        # month_var.set("Choose a month...")

        self.month_combo = ttk.Combobox(self, values=months)
        self.month_combo.place(x=350, y=130)
        self.month_combo.set("Choose a month...")
        self.month_combo.config(state="readonly")

        # the name label & input
        nameLabel = ttk.Label(
            self, text=f'Enter Your Full Name:', font=self.smoll_font)
        nameLabel.place(x=350, y=180)
        self.nameInput = ttk.Entry(self)
        self.nameInput.place(x=350, y=200)

        # the income label & input
        incomeLabel = ttk.Label(
            self, text=f'Enter Your Total Income:', font=self.smoll_font)
        incomeLabel.place(x=350, y=230)
        self.incomeInput = ttk.Entry(self)
        self.incomeInput.place(x=350, y=250)
        self.income = None
        # submit btn
        self.submitbtn = ttk.Button(self, text='Submit',
                                    command=self.saving_data_sqlite3)
        self.submitbtn.place(x=350, y=290)
        # reset btn
        resetbtn = ttk.Button(self, text='Reset',
                              command=self.clear_func)
        resetbtn.place(x=435, y=290)

        # the dash
        line = tk.Label(self, text="______________________"*3)
        line.config(fg=('#7B87BB'))
        line.place(x=130, y=340)

        # label.config(fg=("#00000080"))
        self.savingsTOTAL = []
        link_label = tk.Label(
            self, text="For Financial Education Resources", fg="blue", cursor="hand2", font=self.smoll_font)
        link_label.place(x=200, y=332)
        link_label.bind("<Button-1>", lambda event: self.open_link())
        link_label.bind("<Enter>", lambda e: link_label.config(fg='red'))
        link_label.bind("<Leave>", lambda e: link_label.config(fg='blue'))

    def saving_data_sqlite3(self):
        self.income = self.incomeInput.get()
        try:
            income_value = float(self.income)
        except ValueError:
            income_value = None

        if income_value is not None:
            # saving data to sqLite db
            self.name = self.nameInput.get()

            conn.execute(
                "INSERT INTO Budget (month, name, income) VALUES (?, ?, ?)",
                (self.month_combo.get(), self.name, income_value)
            )
            c.commit()

        pygame.mixer.init()
        coin_sound = pygame.mixer.Sound(
            'scale-f6-106128.wav')
        coin_sound.play()
        # istill doun   no how it works but i did ut like thi (first time)
        pygame.time.wait(1500)

        # calculating the nbeeds, wants, and savings values
        global needs_value, wants_value, savings_value
        needs_value = 0.5 * income_value
        wants_value = round(0.3 * income_value, 2)
        savings_value = round(0.2 * income_value, 2)

        self.confirmo_label = ttk.Label(self)
        self.confirmo_label.config(
            text=f'Hello {self.nameInput.get()}, your {self.month_combo.get()} income is {income_value}', font=self.median_font)
        self.confirmo_label.place(x=90, y=400)

        self.needs_label = ttk.Label(self)
        self.needs_label.place(x=90, y=440)
        self.needs_label.config(
            text=f'Your Needs (50%) count {needs_value}', font=self.median_font)
        needsbtn = ttk.Button(
            self, text="EXPAND NEEDS", command=self.OPEN_Needs_win)
        needsbtn.place(x=400, y=440)

        self.wants_label = ttk.Label(self)
        self.wants_label.config(
            text=f'Your Wants (30%) count {wants_value}', font=self.median_font)
        self.wants_label.place(x=90, y=470)
        wantsbtn = ttk.Button(
            self, text="EXPAND WANTS", command=self.OPEN_Wants_win)
        wantsbtn.place(x=400, y=470)
        self.savingsTOTAL.append(savings_value)
        self.savings_label = ttk.Label(self)
        self.savings_label.config(
            text=f'Your Savings (20%) count {savings_value}', font=self.median_font)
        self.savings_label.place(x=90, y=500)

        target_savings = ttk.Button(
            self, text="SET SAVINGS TARGET", command=self.TargetSavings)
        target_savings.place(x=370, y=500)
        print(self.savingsTOTAL)
        # global target
        if target is not None and float(sum(self.savingsTOTAL)) >= float(target):
            # notification settings
            title = 'Budget Tracker'
            message = f'You have reached your target of savings({target} that was set at {self.savingsave()})!'
            notification.notify(title=title, message=message)
            self.savingset.destroy()
            self.savingsTarget.destroy()

        # def visualization():
        vis = ttk.Button(self, text='Show Savings Tracker', command=self.vis)
        vis.place(x=90, y=525)

        bill = ttk.Button(self, text="Remind Me Of A Bill ",
                          command=self.Bill_Reminder)
        bill.place(x=215, y=525)

    def savingsave(self):
        current_time = datetime.datetime.now()
        year = current_time.year
        month = current_time.month
        day = current_time.day
        hour = current_time.hour
        minute = current_time.minute
        AFTERTIME = "{}-{}-{} ({}:{}).".format(
            year, month, day, hour, minute)
        global target
        target = self.savingsTarget.get()
        target = float(target)
        if target:
            notification.notify(app_name="Budget Controller ", title='Target Setting',
                                message=f"Savings Targetted to {target} at {AFTERTIME} you will be notified when reached to")
        return AFTERTIME

    def TargetSavings(self):
        self.savingsTarget = ttk.Entry(self)
        self.savingsTarget.place(x=370, y=500)
        self.savingset = ttk.Button(self, text="SET", command=self.savingsave)
        self.savingset.place(x=470, y=500)

    def vis(self):
        x = self.savingsTOTAL
        y = range(len(self.savingsTOTAL))
        plt.scatter(x, y, marker='o', s=50, c='blue')
        plt.plot(x, y, linestyle='--', linewidth=2, color='green')
        plt.xlabel('Index')
        plt.ylabel('Savings')
        plt.title('Savings Tracker')
        plt.show()

    def open_link(self):
        webbrowser.open(
            "https://www.cnbc.com/select/how-to-create-a-budget-guide/")

    def Bill_Reminder(self):
        self.rtt = tk.Toplevel(self)
        self.rtt.title("Bills Reminder")
        cal = Calendar(self.rtt, selectmode="day", year=2023, month=4, day=30)
        cal.pack(padx=10, pady=10)

        billo1 = ttk.Label(self.rtt, text='The Bill')
        billo1.pack(padx=5, pady=10)
        BillName = ttk.Entry(self.rtt)
        BillName.pack()

        billo2 = ttk.Label(self.rtt, text='The Bill Amount')
        billo2.pack(padx=10, pady=10)
        BillAmount = ttk.Entry(self.rtt)
        BillAmount.pack()

        def select_date():
            selected_date = cal.get_date()
            TheBillName = BillName.get()
            TheBillAmount = BillAmount.get()
            print("You selected:", selected_date)
            notification.notify(
                app_name="Budget Controller ", title='Target Setting', message=f"the Bill {TheBillName} of {TheBillAmount} is set to be remind you at {selected_date} \n have a nice day<3")
            # k.destroy()
            cal.selection_clear()
            BillName.delete(0, 'end')
            BillAmount.delete(0, 'end')
        billybtn = ttk.Button(self.rtt, text="Remind",
                              command=select_date)
        billybtn.pack(pady=10)

    def OPEN_Needs_win(self):
        NeedsWIN = tk.Toplevel(self)
        NeedsWIN.title('Needs customizations')
        NeedsWIN.geometry("270x250")

        needaddlbl = ttk.Label(NeedsWIN, text='Enter A Need Cost')
        needaddlbl.pack()
        needbutinNEED = ttk.Label(
            NeedsWIN, text=f"max needs: {needs_value}", font=('Arial', 8))
        needbutinNEED.pack()
        needaddentry = ttk.Entry(NeedsWIN)
        needaddentry.pack()

        my_needs = []

        def Adding_Needs():
            global needs_value
            a_need = needaddentry.get()
            if a_need.isdigit() or (a_need.startswith('-') and a_need[1:].isdigit()):
                # Checking if the totla of needs exceeds the max.value
                if sum(my_needs) + float(a_need) > needs_value:
                    messagebox.showerror(
                        title='Max Needs Exceeded',
                        message=f"The running total of needs exceeds the maximum of {needs_value}."
                    )
                else:
                    my_needs.append(float(a_need))
                    with open("needs.csv", 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(my_needs)
                    needaddentry.delete(0, 'end')
                    totalneedsfornow = ttk.Label(
                        NeedsWIN, text=f'{sum(my_needs)}')
                    totalneedsfornow.pack()
            else:
                messagebox.showerror(
                    title='Invalid Input',
                    message='Please enter a valid numeric value for the need cost.'
                )

        button = ttk.Button(NeedsWIN, text="Add Need", command=Adding_Needs)
        button.pack()
        # global needs_value

    def OPEN_Wants_win(self):
        WantsWIN = tk.Toplevel(self)
        WantsWIN.title('Wants customizations')
        WantsWIN.geometry("270x250")

        wantaddlbl = ttk.Label(WantsWIN, text='Enter A Want Cost')
        wantaddlbl.pack()
        wantbutinWANT = ttk.Label(
            WantsWIN, text=f"max wants: {wants_value}", font=('Arial', 8))
        wantbutinWANT.pack()
        wantaddentry = ttk.Entry(WantsWIN)
        wantaddentry.pack()

        my_wants = []

        def Adding_Wants():
            global wants_value
            a_want = wantaddentry.get()
            if a_want.isdigit() or (a_want.startswith('-') and a_want[1:].isdigit()):
                if sum(my_wants) + float(a_want) > wants_value:
                    messagebox.showerror(
                        title='Max Wants Exceeded',
                        message=f"The running total of wants exceeds the maximum of {wants_value}."
                    )
                else:
                    my_wants.append(float(a_want))
                    with open("wants.csv", 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(my_wants)
                    wantaddentry.delete(0, 'end')
                    totalwantsfornow = ttk.Label(
                        WantsWIN, text=f'{sum(my_wants)}')
                    totalwantsfornow.pack()
            else:
                messagebox.showerror(
                    title='Invalid Input',
                    message='Please enter a valid numeric value for the want cost.'
                )

        button = ttk.Button(WantsWIN, text="Add Want", command=Adding_Wants)
        button.pack()

    def clear_func(self):
        self.month_combo.set('Choose a month...')
        self.nameInput.delete(0, 'end')
        self.incomeInput.delete(0, 'end')

    # def listing_details(self):

    def save(self):
        self.mainloop()


target = None

if __name__ == "__main__":
    app = App()
    app.save()

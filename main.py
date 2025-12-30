import tkinter as tk
import requests
import re
from tkinter import ttk
from tkinter import *
from time import strftime

class CurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']
        
    def convert(self, from_currency, to_currency, amount):
        initial_amt = amount
        if from_currency!='USD':
            amount = amount/self.currencies[from_currency]
            
        amount = round(amount * self.currencies[to_currency], 4)
        return amount
        
class Window(tk.Tk):
    def __init__(self, convert_amount):
        tk.Tk.__init__(self)
        self.convert_amt = convert_amount

        self.title('Real Time Currency Converter')
        self.configure(background='black')
        self.geometry('578x170')

        self.date_label = Label(self, text=f"Entry Date: {self.convert_amt.data['date']}", borderwidth=3, bg='black', fg="white")
        self.date_label.config(font=('Arial', 14, 'bold'))
        self.date_label.place(x=209, y=5)

        timer = strftime('%H:%M:%S')
        self.time_label = Label(self, text=f"Entry Time: {timer}", borderwidth=3, bg='black', fg="white")
        self.time_label.config(font=('Arial', 14, 'bold'))
        self.time_label.place(x=216, y=30)

        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_entry=Entry(self, validate='key', validatecommand=valid, justify = tk.CENTER)
        
        self.converted_amt_field = Label(self, text='', bg='white', justify=tk.CENTER, width=18, fg="black")
        
        self.to_currency_var = StringVar(self)
        self.from_currency_var = StringVar(self)
        self.to_currency_var.set("IRR")       
        self.from_currency_var.set("USD")
        
        font = ('Arial', 14, 'bold')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_var, values=list(self.convert_amt.currencies.keys()), justify=tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_var, values=list(self.convert_amt.currencies.keys()), justify=tk.CENTER)
        
        self.amount_entry.place(x=36, y=110)
        self.converted_amt_field.place(x=360, y=113)
        self.from_currency_dropdown.place(x=30, y=80)
        self.to_currency_dropdown.place(x=340, y=80)
        
        self.convert_button = Button(self, text='Convert', fg='black', command=self.perform)
        self.convert_button.config(font=('Arial', 12, 'bold'))
        self.convert_button.place(x=248, y=95)
        
    def perform(self):
        amount=float(self.amount_entry.get())
        from_curr = self.from_currency_var.get()
        to_curr = self.to_currency_var.get()
        
        converted_amt = round(self.convert_amt.convert(from_curr, to_curr, amount), 2)
        self.converted_amt_field.config(text = str(converted_amt))
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string=="" or (string.count('.')<=1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)
    Window(converter)
    mainloop()
 

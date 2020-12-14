from tkinter import Tk, RIGHT, LEFT, BOTH, X, RAISED, TOP
from tkinter.ttk import Frame, Button, Style, Entry, Label
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

class base(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initInputs()

    def initUI(self):
        self.master.title("Arbitragé")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=True)

    def initInputs(self):

        graphFrame = Frame(self)
        graphFrame.pack(fill=BOTH, expand=True)
        fig = Figure(figsize=(1, 1), dpi=100)
        t = np.arange(0, 12 * 1, 0.1) # Multiply by term.
        # Loan Graph - Currently working with static values.
        fig.add_subplot(111).plot(t, 5000 * np.power((1 + (0.2 / 1)), t))
        # Investment Graph - Currently working with static values.
        fig.add_subplot(111).plot(t, 5000 * (1 + t/12))

        canvas = FigureCanvasTkAgg(fig, master=graphFrame)  # A tk.DrawingArea.
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, graphFrame)
        toolbar.update()

        inputsFrame = Frame(self)
        inputsFrame.grid_columnconfigure(1, weight=1)
        inputsFrame.grid_columnconfigure(3, weight=1)
        inputsFrame.pack(fill=X, padx=5, pady=5)

        # Loan Amount
        Label(inputsFrame, text="Loan Amount", width=14).grid(row=0, column=0)
        e_loan = Entry(inputsFrame)
        e_loan.grid(row=0, column=1, stick="we", padx=(0, 5))
        # Loan Interest
        Label(inputsFrame, text="Yearly Interest", width=14).grid(row=1, column=0)
        e_interest = Entry(inputsFrame)
        e_interest.grid(row=1, column=1, stick="we", padx=(0, 5))
        # Loan Term
        Label(inputsFrame, text="Term (Months)", width=14).grid(row=2, column=0)
        e_term = Entry(inputsFrame)
        e_term.grid(row=2, column=1, stick="we", padx=(0, 5))
        # Exchange Price
        Label(inputsFrame, text="Exchange Price", width=14).grid(row=0, column=2)
        e_exchange = Entry(inputsFrame)
        e_exchange.grid(row=0, column=3, stick="we")
        # Increase Forsee
        Label(inputsFrame, text="Monthly Increase", width=14).grid(row=1, column=2)
        e_increase = Entry(inputsFrame)
        e_increase.grid(row=1, column=3, stick="we")

        def calculate():
            print("Loan:\t\t", e_loan.get())
            print("Interest:\t", e_interest.get())
            print("Term:\t\t", e_term.get())
            print("Exchange:\t", e_exchange.get())
            print("Increase:\t", e_increase.get())
            canvas.draw()



        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=X, padx=5, pady=(0, 5))
        b_calculate = Button(buttonsFrame, text="Calculate", command=calculate)
        b_calculate.pack(side=RIGHT)
        b_reset = Button(buttonsFrame, text="Reset")
        b_reset.pack(side=RIGHT)
        
def main():
    root = Tk()
    root.geometry("720x540+300+300")
    base()
    root.mainloop()

if __name__ == '__main__':
    main()
from tkinter import Tk, RIGHT, LEFT, BOTH, X, RAISED, TOP, StringVar
from tkinter.ttk import Frame, Button, Style, Entry, Label, OptionMenu
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import yfinance as yf
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

        canvas = FigureCanvasTkAgg(fig, master=graphFrame)  # A tk.DrawingArea.
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas.draw()
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
        # Increase Forsee
        Label(inputsFrame, text="Commodity Type", width=14).grid(row=2, column=2)
        e_commodity_options = ["", "MSFT", "AAPL", "IBM", "TSLA", "USDTRY=X", "EURTRY=X"]
        e_commodity_var = StringVar(inputsFrame)
        e_commodity_var.set(e_commodity_options[0])
        e_commodity = OptionMenu(inputsFrame, e_commodity_var, *e_commodity_options)
        e_commodity.grid(row=2, column=3, stick="we")

        # Currently just printing values.
        def calculate():
            print("Loan:\t\t", e_loan.get())
            print("Interest:\t", e_interest.get())
            print("Term:\t\t", e_term.get())
            print("Exchange:\t", e_exchange.get())
            print("Increase:\t", e_increase.get())
            print("Commodity:\t", e_commodity_var.get())
            # Uncomment to log data.
            # print(yf.Ticker(e_commodity_var.get()).history(period="1y", interval = "1d"))
            # Get ticker name from e_commodity_var 1 year period, daily data. # Remove ['Close'] for all data.
            comm_data = list(yf.download(e_commodity_var.get(), period="1y", interval = "1d")['Close'])
            # Remove nan datas from list
            comm_data = [comm for comm in comm_data if str(comm) != 'nan']
            # Plot n items to graph
            fig.add_subplot(111).plot(comm_data)

            # GOAL
            # Get "max" data from yfinance ticker
            # Process data by term (month)
            # Dump prediction data to list (remove nan's)
            # Create a list of predictions like (1.32, 1.56, 15.531, 53.01) etc.

            ######################################
            # DEFAULT GRAPHS, IMPLEMENT LATER
            # t = np.arange(0, 12 * 1, 0.1) # Multiply by term.
            # fig.add_subplot(111).plot(t, 5000 * (1 + t/12))
            # fig.add_subplot(111).plot(t, 5000 * np.power((1 + (0.2 / 1)), t))
            ######################################

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

# Required for MacOS 11, idk why.
if __name__ == '__main__': main()
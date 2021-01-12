from tkinter import Tk, RIGHT, LEFT, BOTH, X, RAISED, TOP, StringVar
from tkinter.ttk import Frame, Button, Style, Entry, Label, OptionMenu
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from matplotlib.figure import Figure
import yfinance as yf
import numpy as np
import math, datetime


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
        Label(inputsFrame, text="Loan Amount $", width=14).grid(row=0, column=0)
        e_loan = Entry(inputsFrame)
        e_loan.grid(row=0, column=1, stick="we", padx=(0, 5))

        # Loan Term
        Label(inputsFrame, text="Term (Months)", width=14).grid(row=1, column=0)
        e_term = Entry(inputsFrame)
        e_term.grid(row=1, column=1, stick="we", padx=(0, 5))

        # Loan Interest
        Label(inputsFrame, text="Monhtly Interest", width=14).grid(row=0, column=2)
        e_interest = Entry(inputsFrame)
        e_interest.grid(row=0, column=3, stick="we", padx=(0, 5))

        # Increase Foresee
        Label(inputsFrame, text="Commodity Type", width=14).grid(row=1, column=2)
        e_commodity_options = ["", "MSFT", "AAPL", "IBM", "USDTRY=X", "EURTRY=X", "BTC-USD"]
        e_commodity_var = StringVar(inputsFrame)
        e_commodity_var.set(e_commodity_options[0])
        e_commodity = OptionMenu(inputsFrame, e_commodity_var, *e_commodity_options)
        e_commodity.grid(row=1, column=3, stick="we", padx=(0, 5))

        # Currently just printing values.
        predict_plot = fig.add_subplot(111)

        def calculate():

            # Input variables.
            loan = int(e_loan.get())
            interest = float(e_interest.get())
            times = int(e_term.get())
            commodity = e_commodity_var.get()

            debt = loan * interest * times / 100 + loan

            # YahooFinance historical data
            df = yf.download(commodity, period="10y", interval="1d") #---> Data Size

            dfreg = df.loc[:, ['Open', 'Close', 'Adj Close', 'Volume']]
            dfreg['HILO_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
            dfreg['DELT_PCT'] = (df['Close'] - df['Open']) / df['Open'] * 100.0
            dfreg.fillna(value=-99999, inplace=True)

            #Forecastout = Calculation of the time
            forecast_out = times * 30

            dfreg['label'] = dfreg['Close'].shift(-forecast_out)

            # Calculation of the lot
            liste2 = list(dfreg['Close'][-1:])# YF'den alınan son close datası alım olarak kabul edilir
            lot = loan / int(liste2[0])

            # Separation
            x = dfreg.drop(columns='label')
            x = scale(x) # label dışındaki bütün verileri belli parametereye yerleştiriyor.

            y = dfreg.iloc[:, -1]  # labeldaki tüm satırları al,en son sütunu al
            x_to_predict = x[-forecast_out:]  # the last day we will guess

            # baştan al en son da ki tahmin ediceğimiz günü alma
            x = x[:-forecast_out]
            y = y[:-forecast_out]

            x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=0)

            regressor = LinearRegression()
            regressor.fit(x_train, y_train) # Training

            # Percentage of Accuracy
            accuracy = regressor.score(x_test, y_test) * 100

            prediction_set = regressor.predict(x_to_predict)
            dfreg['Prediction'] = np.nan

            # Last date detection
            last_date = dfreg.iloc[-1].name
            lastDatetime = last_date.timestamp()
            one_day = 86400
            # New date detection
            nexDatetime = lastDatetime + one_day

            for i in prediction_set:
                # Calculate elapsed time
                next_date = datetime.datetime.fromtimestamp(nexDatetime)
                nexDatetime += one_day
                dfreg.loc[next_date] = [np.nan for q in range(len(dfreg.columns) - 1)] + [i]

            # Last and First Predict detection
            firstPredict = list(dfreg['Prediction'][-forecast_out:-forecast_out + 1]) #----> ilk predict değerini listeden bulmka için -forecast:-forecast+1 yaparak predict forecastin ilk değerini buluruz.
            lastPredict = list(dfreg['Prediction'][-1:])

            # Calculation of increase amount
            liste = lastPredict + firstPredict
            a = liste[0]
            b = liste[1]
            result = b - a
            increase = result / a * -1 * 100

            # Calculation of new list = lot X predict
            liste3 = list(dfreg['Prediction'][-forecast_out:])
            liste3 = [i * lot for i in liste3]

            # Output labels
            Label(inputsFrame, text="Accuracy: {:.2f}%".format(accuracy), width=14).grid(row=2, column=0)
            Label(inputsFrame, text="Debt: ${:.2f}".format(debt), width=14).grid(row=2, column=1)
            Label(inputsFrame, text="Change: {:.2f}%".format(increase), width=14).grid(row=2, column=2)

            # Plot Stuff
            predict_plot.clear()
            predict_plot.plot(liste3)
            predict_plot.plot([0, forecast_out], [loan, debt])

            canvas.draw()

        # Button
        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=X, padx=5, pady=(0, 5))
        b_calculate = Button(buttonsFrame, text="Calculate", command=calculate)
        b_calculate.pack(side=RIGHT)


def main():
    root = Tk()
    root.geometry("720x540+300+300")
    base()
    root.mainloop()


# Required for MacOS 11, idk why.
if __name__ == '__main__': main()
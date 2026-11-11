import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import add_stock, get_stock, get_stocks, remove_stock, update_stock

def validate_stock_entry(ticker, shares, date_purchased) -> str | None:
    cleaned_ticker = ticker.strip()
    cleaned_shares = shares.strip()
    cleaned_date_purchased = date_purchased.strip()

    try:
        float(cleaned_shares)
    except ValueError:
        return "Enter a valid amount of Shares"

    try:
        date = datetime.strptime(cleaned_date_purchased, "%m/%d/%Y")
    except ValueError:
        return "Enter a valid date"

    if len(cleaned_ticker) == 0 or not cleaned_ticker.isalpha():
        return "Enter a valid ticker"
    elif len(cleaned_shares) == 0:
        return "Shares are required"
    elif date.date() > datetime.today().date():
        return "Enter a valid date"
    else:
        return None

class Application:
    def __init__(self, root):
        self.root = root
        root.title("Stock Portfolio Tracker")
        root.geometry("700x500")
        root.update_idletasks()
        root.geometry(
            f"+{(root.winfo_screenwidth() - 700) // 2}"
            f"+{(root.winfo_screenheight() - 500) // 2}"
        )

        self.op_dataselecter_var = tk.StringVar()
        self.op_dataselecter_var.set("1D")

        self.lb_portolio_value = tk.Label(root, text="Portfolio Value", font=("Helvetica", 8, "underline"))
        self.lb_portolio_value.place(x=117, y=25, width=80, height=20)

        self.lb_annualized_volatility = tk.Label(root, text="Annualized Volatility", font=("Helvetica", 8, "underline"))
        self.lb_annualized_volatility.place(x=510, y=25, width=100, height=20)

        self.lb_total_return = tk.Label(root, text="Total Return", font=("Helvetica", 8, "underline"))
        self.lb_total_return.place(x=339, y=25, width=60, height=20)

        self.lb_value = tk.Label(root, text="$0.00")
        self.lb_value.place(x=120, y=45, width=50, height=20)

        self.lb_return = tk.Label(root, text="$0.00")
        self.lb_return.place(x=339, y=45, width=40, height=20)

        self.lb_volatility = tk.Label(root, text="0.00%")
        self.lb_volatility.place(x=506, y=45, width=50, height=20)

        self.ch_portfolio = FigureCanvasTkAgg(Figure(figsize=(4.90, 1.60), dpi=100, layout="constrained"), master=root)
        self.ch_portfolio_axes = self.ch_portfolio.figure.add_subplot(111)
        self.ch_portfolio_axes.set_title("Portfolio Value Over Time")
        self.ch_portfolio.draw()
        self.ch_portfolio.get_tk_widget().place(x=120, y=80, width=490, height=160)

        self.bt_add = tk.Button(root, text="Add Stock", command=self.on_bt_add)
        self.bt_add.place(x=129, y=249, width=68, height=30)

        self.bt_risk = tk.Button(root, text="Analyze Risk", command=self.on_bt_risk)
        self.bt_risk.place(x=310, y=450, width=110, height=30)

        self.tr_Holdings = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show="headings")
        self.tr_Holdings.column("col1", width=5, minwidth=5, stretch=True)
        self.tr_Holdings.column("col2", width=5, minwidth=5, stretch=True)
        self.tr_Holdings.column("col3", width=5, minwidth=5, stretch=True)
        self.tr_Holdings.column("col4", width=5, minwidth=5, stretch=True)
        self.tr_Holdings.heading("col1", text="Stock")
        self.tr_Holdings.heading("col2", text="Shares")
        self.tr_Holdings.heading("col3", text="Value")
        self.tr_Holdings.heading("col4", text="Return")
        self.tr_Holdings.place(x=129, y=290, width=460, height=150)

        self.sb_holdings = tk.Scrollbar(root, orient="vertical")
        self.sb_holdings.place(x=589, y=290, width=20, height=150)

        self.bt_remove = tk.Button(root, text="Remove Stock", command=self.on_bt_remove)
        self.bt_remove.place(x=210, y=249, width=100, height=30)

        self.op_dataselecter = tk.OptionMenu(root, self.op_dataselecter_var, "1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "Max")
        self.op_dataselecter.place(x=534, y=250, width=70, height=30)

        self.sb_holdings.config(command=self.tr_Holdings.yview)
        self.tr_Holdings.config(yscrollcommand=self.sb_holdings.set)
        self.load_stocks()

    def load_stocks(self):
        stocks = get_stocks()
        for stock in stocks:
            self.tr_Holdings.insert("", "end", values=stock)

    def on_bt_add(self):
        new_window = tk.Tk()
        new_window.title("Stock Entry")
        new_window.geometry("300x241")

        lb_ticker = tk.Label(new_window, text="Ticker:")
        lb_ticker.place(x=60, y=16, width=90, height=26)

        lb_shares = tk.Label(new_window, text="Shares:")
        lb_shares.place(x=60, y=68, width=90, height=26)

        lb_purchase_price = tk.Label(new_window, text="Purchase Price:")
        lb_purchase_price.place(x=20, y=117, width=110, height=30)

        lb_date_purchased = tk.Label(new_window, text="Date Purchased:")
        lb_date_purchased.place(x=20, y=167, width=110, height=30)


        en_ticker = tk.Entry(new_window)
        en_ticker.place(x=130, y=14, width=150, height=28)

        en_shares = tk.Entry(new_window)
        en_shares.place(x=130, y=67, width=150, height=28)

        en_purchase_price = tk.Entry(new_window)
        en_purchase_price.place(x=130, y=117, width=150, height=28)

        en_date_purchased = tk.Entry(new_window)
        en_date_purchased.place(x=130, y=167, width=150, height=28)

        def on_bt_enter():
            ticker = en_ticker.get()
            shares = en_shares.get()
            purchase_price = en_purchase_price.get()
            date_purchased = en_date_purchased.get()
            if validate_stock_entry(ticker, shares, date_purchased) is not None:
                return messagebox.showerror("Invalid Ticket", validate_stock_entry(ticker, shares, date_purchased))
            add_stock(ticker, shares, purchase_price, date_purchased)

            value = 0
            calc_return = 0
            self.tr_Holdings.insert("", "end", text=ticker, values=(ticker, shares, value, calc_return))

            new_window.destroy()

        bt_enter = tk.Button(new_window, text="Enter", command=on_bt_enter)
        bt_enter.place(x=102, y=200, width=95, height=32)



    def on_bt_risk(self):
        pass

    def on_bt_remove(self):
        selected_stock = self.tr_Holdings.selection()
        values = self.tr_Holdings.item(selected_stock[0], "values")
        for values in selected_stock:
            self.tr_Holdings.delete(values)
        remove_stock(values[0])

    def plot_ch_portfolio(self, x, y):
        """Redraw the chart from two equal-length sequences."""
        self.ch_portfolio_axes.clear()
        self.ch_portfolio_axes.plot(x, y)
        self.ch_portfolio_axes.set_title("Portfolio Value Over Time")
        self.ch_portfolio.draw()

    def load_tr_Holdings(self, rows):
        """Populate the table — pass any iterable of row tuples/lists."""
        self.tr_Holdings.delete(*self.tr_Holdings.get_children())
        for values in rows:
            self.tr_Holdings.insert("", "end", values=values)
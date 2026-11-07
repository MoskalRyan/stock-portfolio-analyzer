import tkinter as tk
from tkinter import ttk
# Requires matplotlib:  pip install matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application:
    def __init__(self, root):
        self.root = root
        root.title("Stock Portfolio Tracker")
        root.geometry("520x380")

        self.lb_portolio_value = tk.Label(root, text="Portfolio Value", font=("Helvetica", 8, "underline"))
        self.lb_portolio_value.place(x=20, y=0, width=80, height=30)

        self.lb_annualized_volatility = tk.Label(root, text="Annualized Volatility", font=("Helvetica", 8, "underline"))
        self.lb_annualized_volatility.place(x=395, y=0, width=100, height=30)

        self.lb_total_return = tk.Label(root, text="Total Return", font=("Helvetica", 8, "underline"))
        self.lb_total_return.place(x=225, y=0, width=60, height=30)

        self.lb_value = tk.Label(root, text="$0.00")
        self.lb_value.place(x=20, y=20, width=50, height=30)

        self.lb_return = tk.Label(root, text="$0.00")
        self.lb_return.place(x=225, y=20, width=40, height=30)

        self.lb_volatility = tk.Label(root, text="0.00%")
        self.lb_volatility.place(x=395, y=20, width=50, height=30)

        self.ch_portfolio = FigureCanvasTkAgg(Figure(figsize=(4.80, 1.50), dpi=100, layout="constrained"), master=root)
        self.ch_portfolio_axes = self.ch_portfolio.figure.add_subplot(111)
        self.ch_portfolio_axes.set_title("Portfolio Value Over Time")
        self.ch_portfolio.draw()
        self.ch_portfolio.get_tk_widget().place(x=20, y=60, width=480, height=150)

        self.button1 = tk.Button(root, text="Add Stock", command=self.on_button1)
        self.button1.place(x=60, y=219, width=68, height=16)

        self.button2 = tk.Button(root, text="Analyze Risk", command=self.on_button2)
        self.button2.place(x=220, y=350, width=90, height=20)

        self.tr_Holdings = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show="headings")
        self.tr_Holdings.heading("col1", text="Stock")
        self.tr_Holdings.heading("col2", text="Shares")
        self.tr_Holdings.heading("col3", text="Value")
        self.tr_Holdings.heading("col4", text="Return")
        self.tr_Holdings.place(x=60, y=240, width=390, height=100)

        self.sb_holdings = tk.Scrollbar(root, orient="vertical")
        self.sb_holdings.place(x=450, y=240, width=20, height=100)

        self.button3 = tk.Button(root, text="Remove Stock", command=self.on_button3)
        self.button3.place(x=133, y=219, width=100, height=16)

        self.combobox1 = ttk.Combobox(root, values=["1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "Max"])
        self.combobox1.place(x=430, y=210, width=70, height=24)

        self.sb_holdings.config(command=self.tr_Holdings.yview)
        self.tr_Holdings.config(yscrollcommand=self.sb_holdings.set)

    def on_button1(self):
        pass

    def on_button2(self):
        pass

    def on_button3(self):
        pass

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
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        self.optionmenu1_var = tk.StringVar()
        self.optionmenu1_var.set("1D")

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

        self.button1 = tk.Button(root, text="Add Stock", command=self.on_button1)
        self.button1.place(x=129, y=249, width=68, height=30)

        self.button2 = tk.Button(root, text="Analyze Risk", command=self.on_button2)
        self.button2.place(x=310, y=450, width=110, height=30)

        self.tr_Holdings = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show="headings")
        self.tr_Holdings.heading("col1", text="Stock")
        self.tr_Holdings.heading("col2", text="Shares")
        self.tr_Holdings.heading("col3", text="Value")
        self.tr_Holdings.heading("col4", text="Return")
        self.tr_Holdings.place(x=129, y=290, width=460, height=150)

        self.sb_holdings = tk.Scrollbar(root, orient="vertical")
        self.sb_holdings.place(x=589, y=290, width=20, height=150)

        self.button3 = tk.Button(root, text="Remove Stock", command=self.on_button3)
        self.button3.place(x=210, y=249, width=100, height=30)

        self.optionmenu1 = tk.OptionMenu(root, self.optionmenu1_var, "1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "Max")
        self.optionmenu1.place(x=534, y=250, width=70, height=30)

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

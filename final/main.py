import tkinter as tk
from gui import Application
from database import init_db

def main():
    init_db()
    
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
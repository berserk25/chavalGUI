import tkinter as tk
import gui_product
import sqlite_product

if __name__ == '__main__':
	sqlite_product.database_existence_check()
	window = tk.Tk()
	app = gui_product.Product(window)
	app.mainloop()
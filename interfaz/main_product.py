import tkinter as tk
import gui_product

if __name__ == '__main__':
	window = tk.Tk()
	app = gui_product.Product(window)
	app.mainloop()
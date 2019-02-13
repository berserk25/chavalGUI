import tkinter as tk
import tkinter.ttk
import sqlite_product
class Product(tk.Frame):

	def __init__(self, window):
		super().__init__(window)
		self.wind = window
		self.wind.title('Products Application')

		#Creating a frame container
		frame = tk.LabelFrame(self.wind, text = 'Register a new product')
		frame.grid(row = 0, column = 0, columnspan = 3, pady = 50, padx = 50)
		
		#Name input
		tk.Label(frame, text = 'Name: ').grid(row = 1, column = 0)
		self.name = tk.Entry(frame)
		self.name.focus()
		self.name.grid(row = 1, column = 1)

		#Price input
		tk.Label(frame, text = 'Price: ').grid(row = 2, column = 0)
		self.price = tk.Entry(frame)
		self.price.grid(row = 2, column = 1)

		#Button add product
		tk.Button(frame, text = 'Save product', command = self.add_product).grid(row = 3, columnspan = 2, sticky = tk.W + tk.E)

		#Output messages
		self.message = tk.Label(text = '', fg = 'red')
		self.message.grid(row = 3, column = 0, columnspan = 2, sticky = tk.W + tk.E)

		#Table
		self.tree = tk.ttk.Treeview(height = 10, columns = 2)
		self.tree.grid(row = 4, column = 0, columnspan = 2)
		self.tree.heading('#0', text = 'Name', anchor = tk.CENTER)
		self.tree.heading('#1', text = 'Price', anchor = tk.CENTER)

		#Buttons
		tk.Button(text = 'Delete', command = self.delete_product).grid(row = 5, column = 0, sticky = tk.W + tk.E)
		tk.Button(text = 'Edit', command = self.edit_product).grid(row = 5, column = 1, sticky = tk.W + tk.E)

		#Filling table
		self.get_products()

	def get_products(self):
		#Cleaning table
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)

		db_rows = sqlite_product.get_products()

		#Filling data
		for row in db_rows:
			self.tree.insert('', 0, text = row[1], values = row[2])

	def not_null_entry_val(self):
		return len(self.name.get()) != 0 and len(self.price.get()) != 0

	def add_product(self):
		self.message['text'] = ''
		if self.not_null_entry_val():
			sqlite_product.add_product(self.name.get(), self.price.get())
			self.message['fg'] = 'green'
			self.message['text'] = 'Product {} added successfully'.format(self.name.get())
			self.name.delete(0, tk.END)
			self.price.delete(0, tk.END)
		else:
			self.message['fg'] = 'red'
			self.message['text'] = 'Name and price are required'
		self.get_products()

	def delete_product(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['fg'] = 'red'
			self.message['text'] = 'Please select a record'
			return
		name = self.tree.item(self.tree.selection())['text']

		sqlite_product.delete_product(name)

		self.message['fg'] = 'green'
		self.message['text'] = 'Record {} deleted successfully'.format(name)
		self.get_products()

	def edit_product(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.message['fg'] = 'red'
			self.message['text'] = 'Please select a record'
			return
		name = self.tree.item(self.tree.selection())['text']
		oldPrice = self.tree.item(self.tree.selection())['values'][0]
		self.edit_wind = tk.Toplevel()
		self.edit_wind.title('Edit product')

		#Old name
		tk.Label(self.edit_wind, text = 'Old name').grid(row = 0, column = 1)
		tk.Entry(self.edit_wind, textvariable = tk.StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)

		#New name
		tk.Label(self.edit_wind, text = 'New name').grid(row = 1, column = 1)
		newName = tk.Entry(self.edit_wind)
		newName.grid(row = 1, column = 2)

		#Old price
		tk.Label(self.edit_wind, text = 'Old price').grid(row = 0, column = 3)
		tk.Entry(self.edit_wind, textvariable = tk.StringVar(self.edit_wind, value = oldPrice), state = 'readonly').grid(row = 0, column = 4)

		#New price
		tk.Label(self.edit_wind, text = 'New price').grid(row = 1, column = 3)
		newPrice = tk.Entry(self.edit_wind)
		newPrice.grid(row = 1, column = 4)

		#Button
		tk.Button(self.edit_wind, text = 'Update', command = lambda: self.edit_record(newName.get(), name, newPrice.get(), oldPrice)).grid(row = 2, column = 2, sticky = tk.W + tk.E)

	def edit_record(self, newName, name, newPrice, oldPrice):
		
		sqlite_product.edit_record(newName, name, newPrice, oldPrice)

		self.edit_wind.destroy()
		self.message['fg'] = 'green'
		self.message['text'] = 'Record {} updated successfully'.format(name)
		self.get_products()
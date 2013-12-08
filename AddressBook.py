
from Tkinter import * # Import tkinter
import tkMessageBox   
import re
import sqlite3
class AddressBook(object):

	def Display(self, output):
		self.DisplayArea.insert(END, output)
		self.DisplayArea.see(END) 

	def __init__(self, DB_path):
		# create the database if it does not exist
		self.dbfilename = DB_path
		db=sqlite3.connect(self.dbfilename)
		db.text_factory = str
		cu=db.cursor()
		cu.execute(
				"CREATE TABLE IF NOT EXISTS AddressList\
					( id	INTEGER PRIMARY KEY, \
					  name	TEXT, \
					  sex	TEXT, \
					  phone	TEXT, \
					  address	TEXT, \
					  email	TEXT \
					  )" \
					)
		db.commit()
		cu.close()
		# create the main window
		window = Tk()
		window.geometry("475x270")
		window.title("Contact Book")
		# create the query display area
		self.DisplayArea = Listbox(master=window)
		self.DisplayArea.pack(side=BOTTOM, fill=X)


		# variables that we can set
		self.nameVar = StringVar()
		self.sexVar = StringVar()
		self.phoneVar = StringVar()
		self.addressVar = StringVar()
		self.emailVar = StringVar()

		# frames and buttons
		frame1 = Frame(window)
		frame1.pack(fill=X)
		Label(frame1, text = "Name:").grid(row = 1, column = 1, sticky = W)
		Entry(frame1, textvariable = self.nameVar,width = 15).grid(row = 1, column = 2)

		Label(frame1, text = "Phone:").grid(row = 1, column = 3, sticky = W)
		Entry(frame1, textvariable = self.phoneVar, width = 15).grid(row = 1, column = 4)

		Label(frame1, text = "Gender:").grid(row = 1, column = 5, sticky = W)
		Entry(frame1, textvariable = self.sexVar, width = 5).grid(row = 1, column = 6)
			
		frame2 = Frame(window)
		frame2.pack(fill=X)
		Label(frame2, text = "Address:").grid(row = 1, column = 1, sticky = W)
		Entry(frame2, textvariable = self.addressVar, width = 20).grid(row = 1, column = 2)

		Label(frame2, text = "Email:").grid(row = 1, column = 3, sticky = W)
		Entry(frame2, textvariable = self.emailVar, width = 22).grid(row = 1, column = 4)

		frame3 = Frame(window)
		frame3.pack(fill=X)
		Button(frame3, text = "Add", command = self.Add).grid(row = 1, column = 1)
		Button(frame3, text = "Query", command = self.Query).grid(row = 1, column = 2)
		Button(frame3, text = "Update", command = self.Update).grid(row = 1, column = 3)
		Button(frame3, text = "Delete", command = self.Delete).grid(row = 1, column = 4)
		Button(frame3, text = "ShowAll", command = self.ShowAll).grid(row = 1, column = 5)  

		# Create an event loop
		window.mainloop()

	def Add(self):
		db = sqlite3.connect(self.dbfilename)
        	cu = db.cursor()
		###################### handling name ############################
		name = self.nameVar.get()
		if name == "":
			tkMessageBox.showinfo("Error", "Name can't be NULL!")
			cu.close()
			
		cu.execute('select name from AddressList')# testify name
		for namelist in cu.fetchall():
			if name in namelist:
				tkMessageBox.showinfo("Error", "Name already exists!")
				cu.close()
				return
		##################################################################
		###################### handling gender ###########################
		sex = self.sexVar.get()
		if sex != 'male' and sex != 'female':
			tkMessageBox.showinfo("Error", "Invalid Gender! Are you crazy?!")
			cu.close()
			return
		##################################################################
		################## handling telephone number #####################
		phone = self.phoneVar.get()
		pattern = re.compile('^[1][3-8]+\\d{9}')
		correct = pattern.match(phone)
		if correct == None:
			tkMessageBox.showinfo("Error", "Invalid Phone Number!")
			cu.close()
			return
		##################################################################
		####################### handling address #########################
		address = self.addressVar.get()
		##################################################################
		####################### handling email ###########################
		email = self.emailVar.get()
		pattern = re.compile('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
		correct = pattern.match(email)
		if correct == None:
			tkMessageBox.showinfo("Error", "Invalid Email Address!")
			cu.close()
			return
		##################################################################
		######################### add a new contact ######################
		values = (name,sex,phone,address,email)
		cu.execute('insert into AddressList(name,sex,phone,address,email) \
		values(?, ?, ?, ?, ?)',values)
		db.commit()
		cu.close()
		tkMessageBox.showinfo("New Contact", "A new Contact has been successfully added!")
		##################################################################
	def Query(self):
		name = self.nameVar.get()
		# invalid name
		if name == "":
			tkMessageBox.showinfo("Error", "Name cannot be NULL!")
			cu.close()
			return
		# db opreations
		db = sqlite3.connect(self.dbfilename)
        	cu = db.cursor()
		cu.execute("select * from AddressList where name  = ?", (name, ))
		Output = ""
		row = cu.fetchone()
		# no such person
		if row == None:
			tkMessageBox.showinfo("Error", "No such person!")
			cu.close()
			return
		# delete the older output first
		ListSize = self.DisplayArea.size()
		self.DisplayArea.delete(0, ListSize - 1)
		# display the specific contact info in the ListBox
		# for multiple items, use a for loop, easy to implement
		Output = str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t\t' + str(row[4]) + '\t\t' + str(row[5]) + '\n'
		title = 'No.\tName\tGender\tTelephone\t\tAddress\t\tEmail\n'
		self.Display(title)
		self.Display(Output)
		db.commit()
		cu.close()

	def Update(self):
		new = []
		name = self.nameVar.get()
		if name == "":
			tkMessageBox.showinfo("Error", "Name cannot be NULL!")
			return
		new.append(name)
		###################### handling gender ###########################
		sex = self.sexVar.get()
		if sex != 'male' and sex != 'female' and sex != '':
			tkMessageBox.showinfo("Error", "Invalid Gender! Are you crazy?!")
			return
		new.append(sex)
		##################################################################
		################## handling telephone number #####################
		phone = self.phoneVar.get()
		pattern = re.compile('^[1][3-8]+\\d{9}')
		correct = pattern.match(phone)
		if correct == None and phone != '':
			tkMessageBox.showinfo("Error", "Invalid Phone Number!")
			return
		new.append(phone)
		##################################################################
		####################### handling address #########################
		address = self.addressVar.get()
		new.append(address)
		##################################################################
		####################### handling email ###########################
		email = self.emailVar.get()
		pattern = re.compile('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
		correct = pattern.match(email)
		if correct == None and email != '':
			tkMessageBox.showinfo("Error", "Invalid Email Address!")
			return
		new.append(email)

		db = sqlite3.connect(self.dbfilename)
        	cu = db.cursor()
		cu.execute("select * from AddressList where name  = ?", (name, ))
		old = []
		row = cu.fetchone()
		if row == None:
			tkMessageBox.showinfo("Error", "No such person!")
			cu.close()
			return
		# name exists in db
		for i in range(1, len(row)): 
			old.append(str(row[i]))
		# if user updates partial information, get the untouched from the old item
		for i in range(1, 5):
			if new[i] == '':
				new[i] = old[i]
		
		cu.execute('UPDATE AddressList set sex=?, phone=?, address=?, email=? WHERE name=?', (new[1], new[2], new[3], new[4], new[0]))
		db.commit()
		cu.close()
		tkMessageBox.showinfo("Update Successfully", "The contact information has been updated successfully!")

	"""
	implement the two functions below
	"""
	def Delete(self):
		# delete a specific contact item
		name = self.nameVar.get()
		# invalid name
		if name == "":
			tkMessageBox.showinfo("Error", "Name cannot be NULL!")
			return
		# db opreations
		db = sqlite3.connect(self.dbfilename)
        	cu = db.cursor()
		cu.execute("select * from AddressList where name  = ?", (name, ))
		row = cu.fetchone()
		if row == None:
			tkMessageBox.showinfo("Error", "No such person!")
			cu.close()
			return
		cu.execute('DELETE FROM AddressList where name=?', (name,))
		db.commit()
		cu.close()
		tkMessageBox.showinfo("Delete Successfully", name+" has been removed from the contact book permenantly!")
	def ShowAll(self):
		# show all the contact info stored in the db
		db = sqlite3.connect(self.dbfilename)
        	cu = db.cursor()
		cu.execute("select * from AddressList")
		AllItems = cu.fetchall()
		cu.close()
		if AllItems == []:
			tkMessageBox.showinfo("Error", "Empty contact book!")
			return
			
		# delete the older output first
		ListSize = self.DisplayArea.size()
		self.DisplayArea.delete(0, ListSize - 1)
		title = 'No.\tName\tGender\tTelephone\t\tAddress\t\tEmail\n'
		self.Display(title)
		# display the specific contact info in the ListBox
		for i in range(0, len(AllItems)):
			row = AllItems[i]	
			Output = str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t\t' + str(row[4]) + '\t\t' + str(row[5]) + '\n'
			self.Display(Output)

if __name__=="__main__":
	addrbook = AddressBook("address-book.db")

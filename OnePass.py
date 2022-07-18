# ----- OnePass ---------------------------------------------------------------------------------------------------- #

# OnePass is an encrypted password manager that stores your passwords locally on your computer
# Created by Steven Pereira aka Cursed Cancer
# Github: https://github.com/CursedCancer

# ----- Import Section --------------------------------------------------------------------------------------------- #

import os
import time
import sqlite3
import random
import string
import keyring
import pwinput
import base64
# from rich import print
from rich import box
from rich.console import Console
from rich.table import Table
from rich.table import Column
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ----- Global Declaration ----------------------------------------------------------------------------------------- #

console = Console()

# ----- Database --------------------------------------------------------------------------------------------------- #

class database():

	def connect():
		connect = sqlite3.connect(r"Database/OnePass.db")
		cursor = connect.cursor
		connect.commit()
		return connect

	def create():
		if os.path.exists(r"Database/"):
			if os.path.exists(r"Database/OnePass.db"):
				database.connect()
				pass
			else:
				database.connect()
		else:
			os.mkdir(r"Database/")
			database.connect()

# ----- Tables ----------------------------------------------------------------------------------------------------- #

def tables():
	database.create()
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	cursor.execute('''
					CREATE TABLE IF NOT EXISTS 'Passwords'
					(
						ID						INTEGER 			Primary Key,
						Name					TEXT(100),
						Username				TEXT(100),
						Password				TEXT(100),
						'Email Address'			TEXT(100),
						URL						TEXT(100),
						Description				TEXT(1000),
						Folder					CHAR(100))''')

# ----- Values ----------------------------------------------------------------------------------------------------- #

def values():
	console.print("[#5bd2f0]──────[#ffaf68] Adding a Password [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
	name = console.input("[#ffaf68]Enter the name of the account: ")
	username = console.input("[#ffaf68]Enter the username of the account: ")
	password = console.input("[#ffaf68]Enter the password of the account: ")
	email = console.input("[#ffaf68]Enter the email address associated with this account: ")
	url = console.input("[#ffaf68]Enter the URL of this account: ")
	while True:
		check = ["Y", "y", "N", "n"]
		description_check = console.input("[#ffaf68][?] Do you want to add any notes to this account? [Y/n]: ")
		if description_check in check:
			if description_check == "y" or description_check == "Y":
				description = console.input("[#ffaf68]Enter a note for the account: ")
				break
			else:
				description = ""
				break
		else:
			print("[#FF756D][!] You've entered the wrong input. Please try again...")
	while True:
		check = ["Y", "y", "N", "n"]
		folder_check = console.input("[#ffaf68][?] Do you want to add this account to a folder? [Y/n]: ")
		if folder_check in check:
			if folder_check == "y" or folder_check == "Y":
				folder = console.input("[#ffaf68]Enter the name of the folder: ")
				break
			else:
				folder = ""
				break
		else:
			print("[#FF756D][!] You've entered the wrong input. Please try again...")
	store(name, username, password, email, url, description, folder)
	console.print("[#79d45e][+] Successfully added an account into OnePass")
	console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
	display_passwords()

# ----- Store ------------------------------------------------------------------------------------------------------ #

def store(name, username, password, email, url, description, folder):
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	sqlQuery = "INSERT INTO 'Passwords' (Name, Username, Password, 'Email Address', URL, Description, Folder) VALUES (?, ?, ?, ?, ?, ?, ?)"
	values = (name, username, password, email, url, description, folder)
	cursor.execute(sqlQuery, values)
	connect.commit()

# ----- Display ---------------------------------------------------------------------------------------------------- #

def display_passwords():
	console.print("[#5bd2f0]──────[#ffaf68] Displaying all Passwords [#5bd2f0]──────────────────────────────────────────────────────────────────────────\n")
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	sqlQuery = "SELECT * FROM 'Passwords'"
	cursor.execute(sqlQuery)
	rows = cursor.fetchall()
	table = Table(
			Column(header="ID", style="#B9EAED", header_style="#7CB5D2"),
			Column(header="Name", style="#D9C4EC", header_style="#B19CD8"),
			Column(header="Username", style="#B9EAED", header_style="#7CB5D2"),
			Column(header="Password", style="#D9C4EC", header_style="#B19CD8"),
			Column(header="Email Address", style="#B9EAED", header_style="#7CB5D2"),
			Column(header="URL", style="#B9EAED", header_style="#7CB5D2"),
			Column(header="Description", style="#D9C4EC", header_style="#B19CD8"),
			Column(header="Folder", style="#B9EAED", header_style="#7CB5D2"),
			box=box.ROUNDED, 
			safe_box=False)
	for row in rows:
		table.add_row(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]))
	console.print(table)

def display_folders():
	console.print("[#5bd2f0]──────[#ffaf68] Displaying all Folders [#5bd2f0]──────────────────────────────────────────────────────────────────────────\n")
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	sqlQuery = "SELECT DISTINCT Folder FROM 'Passwords'"
	cursor.execute(sqlQuery)
	rows = cursor.fetchall()
	table = Table(
			Column(header="Folders", style="#D9C4EC", header_style="#B19CD8"),
			box=box.ROUNDED, 
			safe_box=False)
	for row in rows:
		table.add_row(str(row[0]))
	console.print(table)

# ----- Update ----------------------------------------------------------------------------------------------------- #

def update():
	console.print("[#5bd2f0]──────[#ffaf68] Updating a Password [#5bd2f0]─────────────────────────────────────────────────────────────────────────────\n")
	display_passwords()
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	id_no = console.input("[#ffaf68]Enter the ID number of the account that you want to update: ")
	console.print(f"[#79d45e][+] Updating password with ID - {id_no}: ")
	column_name = str.title(console.input("[#ffaf68]Enter the column name that you want to update: "))
	column_value = console.input("[#ffaf68]Enter the value of " + column_name + ": ")
	if column_name == "Name":
		sqlQuery = "UPDATE 'Passwords' SET Name = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "Username":
		sqlQuery = "UPDATE 'Passwords' SET Username = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "Password":
		sqlQuery = "UPDATE 'Passwords' SET Password = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "Email Address":
		sqlQuery = "UPDATE 'Passwords' SET 'Email Address' = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "URL":
		sqlQuery = "UPDATE 'Passwords' SET URL = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "Description":
		sqlQuery = "UPDATE 'Passwords' SET Description = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	elif column_name == "Folder":
		sqlQuery = "UPDATE 'Passwords' SET Folder = ? WHERE ID = ?"
		cursor.execute(sqlQuery, ([column_value, id_no]))
		console.print("[#79d45e][+] Successfully updated a password")
		connect.commit()
	else:
		console.print("[#FF756D][!] Column does not exist")
		connect.commit()
		menu.clear()
		console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
		display_passwords()

# ----- Delete ----------------------------------------------------------------------------------------------------- #

def delete():
	console.print("[#5bd2f0]──────[#ffaf68] Deleting a Password [#5bd2f0]─────────────────────────────────────────────────────────────────────────────\n")
	display_passwords()
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	multi_delete = console.input("[#ffaf68][?] Do you want to delete multiple accounts? [Y/n]: ")
	if multi_delete == "y" or multi_delete == "Y":
		id_1 = console.input("[#ffaf68]Enter the first ID of the account range that you want to delete: ")
		id_2 = console.input("[#ffaf68]Enter the last ID of the account range that you want to delete: ")
		sqlQuery = "DELETE FROM 'Passwords' WHERE ID BETWEEN ? AND ?"
		cursor.execute(sqlQuery, [id_1, id_2])
		console.print("[#79d45e][+] Successfully deleted multiple accounts from OnePass")
		connect.commit()
		console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
		display_passwords()
	elif multi_delete == "n" or multi_delete == "N":
		id_no = console.input("[#ffaf68]Enter the ID of the account that you want to delete: ")
		sqlQuery = "DELETE FROM 'Passwords' WHERE ID = ?"
		cursor.execute(sqlQuery, [id_no])
		console.print("[#79d45e][+] Successfully deleted an account from OnePass")
		connect.commit()
		console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
		display_passwords()

# ----- Search ----------------------------------------------------------------------------------------------------- #

def search():
	console.print("[#5bd2f0]──────[#ffaf68] Searching a Password [#5bd2f0]────────────────────────────────────────────────────────────────────────────\n")
	connect = sqlite3.connect(r"Database/OnePass.db")
	cursor = connect.cursor()
	name = console.input("[#ffaf68]Enter the name of the account that you want to search for: ")
	sqlQuery = "SELECT * FROM 'Passwords' WHERE Name = ?"
	cursor.execute(sqlQuery, [name])
	console.print("[#79d45e][+] Successfully searched an account")
	rows = cursor.fetchall()
	table = Table(
					Column(header="ID", style="#B9EAED", header_style="#7CB5D2"),
					Column(header="Name", style="#D9C4EC", header_style="#B19CD8"),
					Column(header="Username", style="#B9EAED", header_style="#7CB5D2"),
					Column(header="Password", style="#D9C4EC", header_style="#B19CD8"),
					Column(header="Email Address", style="#B9EAED", header_style="#7CB5D2"),
					Column(header="Phone Number", style="#D9C4EC", header_style="#B19CD8"),
					Column(header="URL", style="#B9EAED", header_style="#7CB5D2"),
					Column(header="Description", style="#D9C4EC", header_style="#B19CD8"),
					Column(header="Folder", style="#B9EAED", header_style="#7CB5D2"),
					box=box.ROUNDED, 
					safe_box=False)
	for row in rows:
		table.add_row(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]),str(row[5]),str(row[6]),str(row[7]))
	console.print("[#5bd2f0]──────[#ffaf68] Output [#5bd2f0]───────────────────────────────────────────────────────────────────────────────\n")
	console.print(table)

# ----- Generate --------------------------------------------------------------------------------------------------- #

def generate():
	try:
		console.print("[#5bd2f0]────── [#ffaf68]Password Generator[#5bd2f0] ──────────────────────────────────────────────────────────────────────────\n")
		length = int(console.input("[#ffaf68][?] Enter the length of the password: "))
		lower = string.ascii_lowercase
		upper = string.ascii_uppercase
		number = string.digits
		symbols = string.punctuation
		data = lower + upper + number + symbols
		raw = random.sample(data, length)
		password = "".join(raw)
		print(password)
	except ValueError:
		console.print("[#FF756D][!] Please enter a numerical value as the length")
		generate()

# ----- Settings --------------------------------------------------------------------------------------------------- #

class settings():

	def create_master_password():
		user_input = console.input("[#ffaf68][?] Set a new master password for OnePass")
		keyring.set_password("Master", "OnePass", user_input)

	def update_master_password():
		console.print("[#5bd2f0]──────[#ffaf68] Updating Master Password [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────\n")
		keyring.delete_password("Master", "OnePass")
		user_input = console.input("[#ffaf68][?] Set a new master password for OnePass: ")
		keyring.set_password("Master", "OnePass", user_input)
		console.print("[#79d45e][+] Master password successfully updated")

	def delete_master_password():
		console.print("[#5bd2f0]──────[#ffaf68] Deleting Master Password [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────\n")
		check = console.input("[#FF756D][!] Are you sure that you want to delete your Master Password? [Y/n]: ")
		if check == "y" or check == "Y":
			valid = console.input("[#ffaf68]Please enter your master password: ")
			password = keyring.get_password("Master", "OnePass")
			if valid == password:
				keyring.delete_password("Master", "OnePass")
				console.print("[#79d45e][+] Master password successfully deleted")
			else:
				console.print("[[#FF756D]!]You've entered the wrong password. Terminating OnePass...")
				exit()
		else: 
			console.print("[#ffaf68][~] Going back to the main menu...")
			pass

	def panic():
		console.print("[#5bd2f0]──────[#ffaf68] Panic [#5bd2f0]───────────────────────────────────────────────────────────────────────────────────────────\n")
		check = keyring.get_password("Master", "OnePass")
		master_password = console.input("[#ffaf68]Enter your master password to delete all accounts in OnePass: ")
		if master_password == check:
			warn = console.input("[#FF756D][?] Do you want to delete all the accounts in OnePass? (Y/N) ")
			if warn == "y" or warn == "Y":
				os.remove(r"Database/OnePass.db")
				database.create()
				tables()
				console.print("[#79d45e][+] Successfully deleted all accounts from OnePass")
				time.sleep(3)
			elif warn == "n" or warn == "N":
				console.print("[#FF756D][-] Panic mode aborted")
				time.sleep(3)
				menu.main()
			else:
				pass
		else:
			console.print("[#FF756D][!] Incorrect master password. Terminating OnePass...")
			encryption.encrypt()
			exit()

# ----- Banner Function -------------------------------------------------------------------------------------------- #

class banner():

	def ascii():
		console.print(r"""[#79d45e]
        ┌──────────────────────────────────────────────────────────────────────────────────────┐
        │      [#a484e9]________  ________   _______   ________  ________  ________   ________ [#79d45e]         │
        │     [#a484e9]|\   __  \|\   ___  \|\  ___ \ |\   __  \|\   __  \|\   ____\ |\   ____\ [#79d45e]        │ 
        │     [#a484e9]\ \  \|\  \ \  \\ \  \ \   __/|\ \  \|\  \ \  \|\  \ \  \___|_\ \  \___|_ [#79d45e]       │
        │      [#a484e9]\ \  \\\  \ \  \\ \  \ \  \_|/_\ \   ____\ \   __  \ \_____  \\ \_____  \ [#79d45e]      │
        │       [#a484e9]\ \  \\\  \ \  \\ \  \ \  \_|\ \ \  \___|\ \  \ \  \|____|\  \\|____|\  \ [#79d45e]     │
        │        [#a484e9]\ \_______\ \__\\ \__\ \_______\ \__\    \ \__\ \__\____\_\  \ ____\_\  \ [#79d45e]    │
        │         [#a484e9]\|_______|\|__| \|__|\|_______|\|__|     \|__|\|__|\_________\\_________\ [#79d45e]   │
        │                                                           [#a484e9]\|_________\|_________| [#79d45e]   │
        │                                                                                      │
        │                              [#31bff3]- WELCOME TO ONEPASS -[#79d45e]                                  │
        │  Onepass is a Encrypted Password Manager that stores all your sensitive credentials  │
        │                                                                                      │
        │                                      +-+-+                                           │
        │                                 [red] Cursed Cancer[#79d45e]                                       │
        │                                      +-+-+                                           │
        └──────────────────────────────────────────────────────────────────────────────────────┘     
        """)

# ----- Main Menu -------------------------------------------------------------------------------------------------- #

class menu():

	def clear():
		time.sleep(1)
		if os.name == "nt":
			os.system("cls")
		else:
			os.system("clear")

	def main():
		banner.ascii()
		console.print("[#5bd2f0]────── [#ffaf68]Main Menu [#5bd2f0]────────────────────────────────────────────────────────────────────────────────────────\n")
		console.print("[#f6e683]\t1. Add a new account to OnePass")
		console.print("[#f6e683]\t2. Generate a strong password")
		console.print("[#f6e683]\t3. Search OnePass for an account")
		console.print("[#f6e683]\t4. Update accounts")
		console.print("[#f6e683]\t5. Delete accounts")
		console.print("[#f6e683]\t6. Display accounts")
		console.print("[#f6e683]\t7. Settings")
		console.print("[#f6e683]\tQ. Quit")

	def display():
		banner.ascii()
		console.print("[#5bd2f0]────── [#ffaf68]Settings [#5bd2f0]────────────────────────────────────────────────────────────────────────────────────────\n")
		console.print("[#f6e683]\t1. Display all passwords")
		console.print("[#f6e683]\t2. Display all folders")
		console.print("[#f6e683]\tQ. Quit")

	def settings():
		banner.ascii()
		console.print("[#5bd2f0]────── [#ffaf68]Settings [#5bd2f0]────────────────────────────────────────────────────────────────────────────────────────\n")
		console.print("[#f6e683]\t1. Update master password")
		console.print("[#f6e683]\t2. Delete master password")
		console.print("[#f6e683]\t3. Activate panic mode")
		console.print("[#f6e683]\t4. Go back to the main menu")
		console.print("[#f6e683]\tQ. Quit")

# ----- Conditions ------------------------------------------------------------------------------------------------- #

class conditions():

	def main():
		while True:
			user_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
			if user_input == "1":
				menu.clear()
				banner.ascii()
				values()
				quit.store()
				break
			elif user_input == "2":
				menu.clear()
				banner.ascii()
				generate()
				quit.generate()
				break
			elif user_input == "3":
				menu.clear()
				banner.ascii()
				search()
				quit.search()
				break
			elif user_input == "4":
				menu.clear()
				banner.ascii()
				update()
				quit.update()
				break
			elif user_input == "5":
				menu.clear()
				banner.ascii()
				delete()
				quit.delete()
				break
			elif user_input == "6":
				menu.clear()
				menu.display()
				conditions.display()
				break
			elif user_input == "7":
				menu.clear()
				menu.settings()
				conditions.settings()
				break
			elif user_input == "Q" or user_input == "q":
				console.print("[#FF756D][!] Terminating OnePass")
				time.sleep(1)
				encryption.encrypt()
				exit()
				break
			else:
				console.print("[#FF756D][!] Please enter a valid option...")

	def display():
		while True:
			user_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
			if user_input == "1":
				menu.clear()
				banner.ascii()
				display_passwords()
				quit.display()
				break
			elif user_input == "2":
				menu.clear()
				banner.ascii()
				display_folders()
				quit.display()
				break
			elif user_input == "Q" or user_input == "q":
				console.print("[#FF756D][!] Terminating OnePass")
				time.sleep(1)
				encryption.encrypt()
				exit()
				break
			else:
				console.print("[#FF756D][!] Please enter a valid option...")

	def settings():
		while True:
			user_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
			if user_input == "1":
				menu.clear()
				banner.ascii()
				settings.update_master_password()
				quit.settings()
				break
			elif user_input == "2":
				menu.clear()
				banner.ascii()
				settings.delete_master_password()
				quit.settings()
				break
			elif user_input == "3":
				menu.clear()
				banner.ascii()
				settings.panic()
				quit.settings()
				break
			elif user_input == "Q" or user_input == "q":
				console.print("[#FF756D][!] Terminating OnePass")
				time.sleep(1)
				encryption.encrypt()
				exit()
				break
			else:
				console.print("[#FF756D][!] Please enter a valid option...")

# ----- Quit Menu -------------------------------------------------------------------------------------------------- #

class quit():

	def store():
		console.print("[#f6e683]\n1. Add another account")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			values()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def generate():
		console.print("[#f6e683]\n1. Generate another password")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			generate()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def search():
		console.print("[#f6e683]\n1. Search another account")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			search()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def update():
		console.print("[#f6e683]\n1. Update another account")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			update()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def delete():
		console.print("[#f6e683]\n1. Delete another account")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			delete()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def display():
		console.print("[#f6e683]1. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

	def settings():
		console.print("[#f6e683]\n1. Go back to the settings menu")
		console.print("[#f6e683]2. Go back to the main menu")
		console.print("[#f6e683]Q. Quit")
		quit_input = console.input("\n[#5bd2f0]────── [#ffaf68]Choose an Option [#5bd2f0]─────────────────────────────────────────────────────────────────────────────────[#ffaf68]\n>> ")
		if quit_input == "1":
			menu.clear()
			banner.ascii()
			menu.settings()
			conditions.settings()
		elif quit_input == "2":
			menu.clear()
			banner.ascii()
			menu.main()
			conditions.main()
		elif quit_input == "q" or quit_input == "Q":
			console.print("[#FF756D][!] Terminating OnePass")
			time.sleep(1)
			encryption.encrypt()
			exit()
		else:
			pass

# ----- Encryption ------------------------------------------------------------------------------------------------- #

class encryption():

	def encrypt():
	    key = keyring.get_password("Master", "OnePass")
	    password = key.encode()
	    pass_salt = b'\x82\x06\xbf6u^\x12\xc1a\x92\xff\x89d(\xa3\x97'
	    kdf = PBKDF2HMAC(
	            algorithm = hashes.SHA256,
	            length = 32,
	            salt = pass_salt,
	            iterations = 10000,
	            backend = default_backend()
	        )
	    key = base64.urlsafe_b64encode(kdf.derive(password))
	    cipher = Fernet(key)
	    with open(r"Database/OnePass.db", 'rb') as ogfile:
	            og = ogfile.read()
	    encrypted_file = cipher.encrypt(og)
	    with open(r"Database/OnePass.db", "wb") as enfile:
	        enfile.write(encrypted_file)

	def decrypt():
	    key = keyring.get_password("Master", "OnePass")
	    password = key.encode()
	    pass_salt = b'\x82\x06\xbf6u^\x12\xc1a\x92\xff\x89d(\xa3\x97'
	    kdf = PBKDF2HMAC(
	            algorithm = hashes.SHA256,
	            length = 32,
	            salt = pass_salt,
	            iterations = 10000,
	            backend = default_backend()
	        )
	    key = base64.urlsafe_b64encode(kdf.derive(password))
	    cipher = Fernet(key)
	    with open(r"Database/OnePass.db", "rb") as df:
	        encrypted_data = df.read()
	    decrypted_file = cipher.decrypt(encrypted_data)
	    with open(r"Database/OnePass.db", "wb") as df:
	        df.write(decrypted_file)

# ----- Main Function ---------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
	menu.clear()
	check = keyring.get_password("Master", "OnePass")
	if check == None:
		newpassword = pwinput.pwinput("Enter the new Master Password for OnePass: ")
		#encryption.decrypt()
		keyring.set_password("Master", "OnePass", newpassword)
		database.create()
		while True:
			menu.clear()
			tables()
			menu.main()
			conditions.main()
	else:
		master_password = pwinput.pwinput("Enter your Master Password to enter OnePass: ")
		encryption.decrypt()
		if master_password == check:
			database.create()
			while True:
				menu.clear()
				tables()
				menu.main()
				conditions.main()
		else:
			console.print("[#FF756D][!] Incorrect Master Password")
			encryption.encrypt()
			exit()

# ----- End -------------------------------------------------------------------------------------------------------- #
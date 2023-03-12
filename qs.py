import getpass
from tqdm import tqdm
import sqlite3
import pyzbar.pyzbar as pyzbar
import pyqrcode
import cv2
import os
import colorama
from colorama import Back
import getpass
import os
import sqlite3
import colorama
import cv2
import pyqrcode
import pyzbar.pyzbar as pyzbar
from colorama import Back
from tqdm import tqdm

colorama.init(autoreset=True)

# ©|Anupa_Dinuranga
#--------ScanningFromWebCamera----------
def scan():
	i = 0
	cap = cv2.VideoCapture(0)
	font = cv2.FONT_HERSHEY_PLAIN
	try:
		while i<2:
			ret,frame=cap.read()
			decode = pyzbar.decode(frame)
			for obj in decode:
				name=obj.data
				name2= name.decode()
				nn,ii,pp,dd = name2.split(' ')
				db = sqlite3.connect('Student Database.db')
				c = db.cursor()
				c.execute('''CREATE TABLE IF NOT EXISTS Record(Name TEXT, StudentID TEXT,Phone TEXT, Dept TEXT, TimenDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL )''')
				c.execute("INSERT INTO Record(Name, StudentID, Phone, Dept) VALUES (?,?,?,?)", (nn,ii,pp,dd))
				db.commit()
				i=i+1
			cv2.imshow("QRCode",frame)
			cv2.waitKey(2)
			cv2.destroyAllWindows
		print("Successfully Recorded.")
			
	except:
		print("Wrong QR input!!!")

# ©|Anupa_Dinuranga
#--------CreateDatabaseForStudents--------------
def database():
	conn = sqlite3.connect('Student Database.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(Student_name TEXT, Student_ID TEXT, Contact, Dept TEXT)")
	conn.commit()
	conn.close()
database()

# ©|Anupa_Dinuranga
#------AddingNewStudent-------------
def add_User():
	Li = []
	S_name=str(input("Please Enter Student Name: "))
	S_id=str(input("Please Enter Student Id: "))
	S_contact= input("Please enter Student Contact No: ")
	S_dept= input("Please enter Student Department: ")
	Li.extend((S_name,S_id,S_contact,S_dept))
 
# ©|Anupa_Dinuranga
#-------using List Compression to convert a list to str---------
	listToStr = ' '.join([str(elem) for elem in Li])
	print(Back.YELLOW + "Please Verify the Information")
	print("Student Name       = "+ S_name)
	print("Student ID         = "+ S_id)
	print("Student Contact    = "+ S_contact)
	print("Student Department = "+ S_dept)
	input("Press Enter to continue or CTRL+C to Break Operation")
	conn = sqlite3.connect('Student Database.db')
	c = conn.cursor()
	c.execute("INSERT INTO all_record(Student_name, Student_ID, contact, department) VALUES (?,?,?,?)", (S_name,S_id,S_contact,S_dept))
	conn.commit()
	conn.close()
	qr= pyqrcode.create(listToStr)
	if not os.path.exists('./QrCodes'):
		os.makedirs('./QRCodes')
	qr.png("./QRCodes/" +S_name+ ".png",scale=8)

# ©|Anupa_Dinuranga
#--------------ViewDatabase--------------------
def viewdata():
	conn = sqlite3.connect('Student Database.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Record")
	rows = c.fetchall()
	for row in rows:
		print(row)
	conn.close()
# ©|Anupa_Dinuranga
#------------AdminView-----------------
def afterlogin():
	print("+------------------------------+")
	print("|  1 - Add New Student          |")
	print("|  2 - Veiw Record              |")
	print("|  3 - Exit                     |")
	print("+------------------------------+")
	user_input = input("Enter Your Choice: ")
	if user_input == '1':
		add_User()
	if user_input == '2':
		viewdata()
	if user_input == '3':
		exit()
  
# ©|Anupa_Dinuranga
#--------------Login------------------
def login():
	print(Back.CYAN+ 'Please Enter Password : ')
	print(Back.YELLOW+"_____QR Code Attendace System_____")
	password = getpass.getpass()
	if password =='1234':
		for i in tqdm(range(4000)):
			print("",end='\r')
		print("------------------------------------------------------------------------------------------------------------------------")
		print(Back.BLUE+"_____QR Code Attendace System_____")
		afterlogin()
	if password != '1234':
		print("Invalid Password!!!")
		login()

# ©|Anupa_Dinuranga
#-----------MainPage-----------------
def banner():
		print("+------------------------------------------+")
		print(" _____STUDENT ATTENDANCE MARKING SYSTEM_____")
		print("|        1- Mark Attendance                |")
		print("|        2- Admin Login                    |")
		print("|        0- Exit                           |")
		print("+------------------------------------------+")
		print()
		user_input2 = input("Enter Your Choice: ")
		if user_input2== '1':
			scan()
		if user_input2 == '2':
			login()
		if user_input2 == '0':
			exit()
if __name__ == "__main__":
	banner()
 	

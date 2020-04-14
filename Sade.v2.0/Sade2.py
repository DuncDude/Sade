
#shebanf
#!/bin/bash

#Libraries
try:
	from bs4 import BeautifulSoup
	
	import requests
	
	import urllib.request
	
	import os
	
	import fnmatch
	
	import numpy
	
	import face_recognition

except:
	print("you seem to be missing some libraries")

#GLOBAL VARIBLES

#page number of pornhub
x = 0
#amount saved and lost
amountS = 1
amountL = 1


#Pause Function
def Pause():
	pase = input("Press Enter.. ")
	return

def Banner():
#Prints banner and clear screen at each new page
	#clear screen
	os.system('cls' if os.name == 'nt' else 'clear')
	print("SADE")
                             
                             
	print("___ PORNHUB Facial Matching________________________________________________________ ")
	#return to function that called
	return


def download(url, fileName):
	full_path = "./knownFaces/" + fileName
	urllib.request.urlretrieve(url,full_path)
	return 




#porn pics
def pPics():
	Banner()
	global x
	global amountS
	global amountL
	print("---------------Starting Scrape of Page " + str(x) + " of PornPics----------------------")
	page = requests.get("https://www.pornpics.com/pornstars/" + str(x) + "/")

#parse the data into html
	soup = BeautifulSoup(page.content, 'html.parser')
# We can now print out the HTML content of the page, formatted nicely, using the prettify method on the BeautifulSoup object:
#print(soup.prettify())

#print pornstar names and rearrage with dashes to be url friendly
	for a in soup.find_all('a', class_="rel-link"):
		if a.img:
		#print(a.img['alt'])
			name = a.img['alt']
			fileName1 = name.replace(' ','.')
			print("PornStar: " + fileName1)
			print(a.img['data-src'])
			#profile = requests.get("https://www.pornhub.com/pornstar/" + fileName1)
			#soup2 = BeautifulSoup(profile.content, 'html.parser')
		#print(soup2)
			#lady = soup2.find('img', id="getAvatar")
			try:
				#print("Image URL: " +lady['src'])
				url1 = a.img['data-src']
				#call for image dowload
				download(url1,fileName1)
				print("Downloaded picture!")
				amountS += 1
			except:
				print("Not Verrified User No Thumbnail!")
				amountL += 1
		#print(soup2)
			#try:
			#	for div in soup2.find_all('div', class_="coverImage"):
			#		if div.img:
			#			url1 = div.img['src']
			#			print(url1)
			#		#call for image dowload
			#			fileName1 = fileName1.replace('-',' ')
			#			download(url1,fileName1)
			#			print("Downloaded Banner!")
			#			amountS += 1
	#
	#		except:
	#			print("No Verrified User No Banner!")
	#			amountL += 1
	#when page runs out of porn stars check next page
	x = int(x)
	x +=1
	print("------------------End of Page-----------------------")
	print("Pictures Saved: " + str(amountS))
	print("Pictures lost: " + str(amountL))
	sucess = (amountS/(amountS + amountL))*100
	print("Success Rate: " + str(sucess))
	pPics()
	return	



#download the page with a requests GET

def Run():
	Banner()
	global x
	global amountS
	global amountL
	print("---------------Starting Scrape of Page " + str(x) + " of PornHub----------------------")
	page = requests.get("https://www.pornhub.com/pornstars?page=" + str(x))

#parse the data into html
	soup = BeautifulSoup(page.content, 'html.parser')
# We can now print out the HTML content of the page, formatted nicely, using the prettify method on the BeautifulSoup object:
#print(soup.prettify())

#print pornstar names and rearrage with dashes to be url friendly
	for a in soup.find_all('a', class_="js-mxp"):
		if a.img:
		#print(a.img['alt'])
			name = a.img['alt']
			fileName1 = name.replace(' ','-')
			print("PornStar: " + fileName1)
	
			profile = requests.get("https://www.pornhub.com/pornstar/" + fileName1)
			soup2 = BeautifulSoup(profile.content, 'html.parser')
		#print(soup2)
			lady = soup2.find('img', id="getAvatar")
			try:
				#print("Image URL: " +lady['src'])
				url1 = lady['src']
				#call for image dowload
				download(url1,fileName1)
				print("Downloaded picture!")
				amountS += 1
			except:
				print("Not Verrified User No Thumbnail!")
				amountL += 1
		#print(soup2)
			try:
				for div in soup2.find_all('div', class_="coverImage"):
					if div.img:
						url1 = div.img['src']
						print(url1)
					#call for image dowload
						fileName1 = fileName1.replace('-',' ')
						download(url1,fileName1)
						print("Downloaded Banner!")
						amountS += 1
	
			except:
				print("No Verrified User No Banner!")
				amountL += 1
	#when page runs out of porn stars check next page
	x = int(x)
	x +=1
	print("------------------End of Page-----------------------")
	print("Pictures Saved: " + str(amountS))
	print("Pictures lost: " + str(amountL))
	sucess = (amountS/(amountS + amountL))*100
	print("Success Rate: " + str(sucess))
	Run()
	return

def check():
	Banner()
	known_faces = []
	results_faces = []
	print("----------Working Directory Files ")
    #list files in working directory
	print("Files: ")
	listOfFiles = os.listdir('./')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			print(entry)
	fileU= input("ENter image file to check: ")
	print("Files Being checked---------------: ")
	listOfFiles = os.listdir('./knownFaces')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			style = "_data"
			entryTitle = entry + style
			print(entryTitle)
			entryTitle = face_recognition.load_image_file("./knownFaces/" + entry)
			#see if photos are valid delete the rest
			try:
				encodedEntry = entry
				results_faces.append(encodedEntry)
				encodedEntry = encodedEntry + "_encoding"
				encodedEntry = face_recognition.face_encodings(entryTitle)[0]
				known_faces.append(encodedEntry)
				
			except IndexError:
				print("I wasn't able to locate any faces in: " + entry + " Deleting image..")
				#os.remove("./knownFaces/" + entry)
	#print("Database Cleaned!")
	
	unknown_image = face_recognition.load_image_file("./" + fileU)
	unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

	#compare to list
	results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
	for i in range(len(results)):
		if results[i] == True:
			print("Likely the face of " + results_faces[i])
	print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
	Pause()
	return

def clean():
	print("Files Being checked---------------: ")
	listOfFiles = os.listdir('./knownFaces')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			style = "_data"
			entryTitle = entry + style
			print(entryTitle)
			entryTitle = face_recognition.load_image_file("./knownFaces/" + entry)
			#see if photos are valid delete the rest
			try:
				encodedEntry = entry
				encodedEntry = encodedEntry + "_encoding"
				encodedEntry = face_recognition.face_encodings(entryTitle)[0]
				
			except IndexError:
				print("I wasn't able to locate any faces in: " + entry + " Deleting image..")
				os.remove("./knownFaces/" + entry)
	print("Database Cleaned!")
	Pause()
	return
	
	
	
def advance():
	Banner()
	known_faces = []
	results_faces = []
	print("----------Working Directory Files ")
    #list files in working directory
	print("Files: ")
	listOfFiles = os.listdir('./')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			print(entry)
	fileU= input("ENter image file to check: ")
	delete=input("Would you like to delete files that have no recognizable faces (y/n): ")
	tol= input("Set tolerance level, lower is more strict matching (default is 0.6): ")
	if tol:
		tol = float(tol)
	else:
		tol = float('0.6')
	#print all folders
	print("----------FOLDERS")
	for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))
	folder= input("Enter folder of images: ")
	print("Files Being checked---------------: ")
	listOfFiles = os.listdir('./' + folder)
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			style = "_data"
			entryTitle = entry + style
			print(entryTitle)
			entryTitle = face_recognition.load_image_file("./" + folder+"/" + entry)
			#see if photos are valid delete the rest
			try:
				encodedEntry = entry
				results_faces.append(encodedEntry)
				encodedEntry = encodedEntry + "_encoding"
				encodedEntry = face_recognition.face_encodings(entryTitle)[0]
				known_faces.append(encodedEntry)
				
			except IndexError:
				print("I wasn't able to locate any faces in: " + entry + " Deleting image..")
				if delete == 'y':
					os.remove("./" + folder + "/" + entry)
	print("Database Cleaned!")
	
	unknown_image = face_recognition.load_image_file("./" + fileU)
	unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

	#compare to list
	results = face_recognition.compare_faces( known_faces, unknown_face_encoding, tol)
	for i in range(len(results)):
		if results[i] == True:
			print("Likely the face of " + results_faces[i])
	print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
	Pause()
	return

def sanitize():
	print("Files Being checked---------------: ")
	listOfFiles = os.listdir('./knownFaces')
	pattern = "*"
	for entry in listOfFiles:
		if fnmatch.fnmatch(entry, pattern):
			style = "_data"
			entryTitle = entry + style
			print(entryTitle)
			entryTitle = face_recognition.load_image_file("./knownFaces/" + entry)
			#see if photos are valid delete the rest
			try:
				encodedEntry = entry
				encodedEntry = encodedEntry + "_encoding"
				encodedEntry = face_recognition.face_encodings(entryTitle)[0]
				
			except IndexError:
				print("I wasn't able to locate any faces in: " + entry + " Deleting image..")
				os.remove("./knownFaces/" + entry)
	print("Database Cleaned!")
	Pause()
	return

def populate():
	Banner()
	print("[1]. Use Pornhub")
	print("[2]. Use PornPics.com")
	choice = input("ENter CHoice: ")
	if choice:
		if choice == '1':
			x=input("Select start Page #: ")
			Run()
		if choice == '2':
			x=input("Select start Page #: ")
			pPics()
	else:
		return

def Home():
	#List Options
	Banner()
	global x
	x= 0
	print("Top Menu")
	print("[1]. Populate Face DataBase")
	print("[2]. Check Image against Default DataBase")
	print("[3]. Advanced Check Image against Choice Database")
	print("[4]. Sanitize Database")
	print("[q]. Quit")
	choice = input("ENter CHoice: ")
	if choice:
		if choice == '1':
			populate()
		if choice == '2':
			check()
		if choice == '3':
			advance()
		if choice == '4':
			sanitize()
		if choice == 'q':
			Banner()
			quit()
	else:
		Home()
	Home()
#Spaslh screen
def splash():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("    SADE")                 
	print("___ PORNHUB Facial Matching________________________________________________________ ")
	print("                d$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$L")
	print("                M$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	print("                M$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$N")
	print("                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$N.")
	print("                 #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.")
	print("                 $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$.")
	print("                J$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b")
	print("                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	print("                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#TTR$$$$$$$$$$$$R")
	print("                ?$$$$$$$$$$$$$$$$$$$$$$$$$$$$R$MX!!!$$$$$$$$$$$$R")
	print("               . ^$$$$$$$$$$$$$$$$$$$$$$$$$$RM?R$!!!$$$$$$$$$$$$F")
	print("               'h..$$$$$$$$$$$$$$$$$$$$$$$R!M!!!!$X!$$$$$$$$$$$$v")
	print("                 ^""$$$$$$$$$$$$$$$$$$$$Rl!!!!!!!M!M!$$$$$$$$$F")
	print("                     $$$$$$$$$$$$$$*$BDX!!!!!!XU@M!!!!$$$$$$F")
	print("                     E $$$$$$$$$$R?$*$$$$X!!!8$$$*R$!!$$$$#`")
	print("                     N **$$$$$$$?!!?!!!!??!!!??!!!?!!!$$*")
	print("                     4:  4$$$$$$R!!!!!!!!!!!!!!!!!!!!!$*x@*")
	print("                      '  d$$$$$$!!!!!!!!!!!!!!!!!!!!!!#d~")
	print("                     ..u@* H$$$$X!!!~~!!!!!!!:~!!!!!!9$$-")
	print("                  '****`    J*$$R!!~` `~!!X!!! !:~!!!M#$L")
	print("                          '""4$$$!!~~~   ~!!!!!!!!!!XE4$M")
	print("                             J$$$K!~~   ..iXUUX!!!!!@EM$R")
	print("                             $$$$$X!~ ~'R$$$$$$!!!!@$$M$$")
	print("                            .J$R*$$M:~`~~#R$R#!!!X$$$*9$R")
	print("                           d* $> 'R!!!::~  ~:!!XWRM$F '$")
	print("                          4   ^  :!!~~!Mhx:XXU@RMMM$   *")
	print("                          4     :!~!~~ !MMMMMMMMMMMMML*i")
	print("                          '  .+?!~~~  ~ `?MMMMMMMMMMMMMM:.")
	print("                         .:!!~`~~       /~!?MMMMMMMMMMMMMMMHx.")
	print("            ..:mmm@!!??!!!!!!~         /~~~!!?MMMMMMMMMMMMMMMMMMc.........")
	print("          :!!~ ~  `~  ``~\~~~~~   _~~ ~!~~_~~~!!!!!~!!!~!!!*?*~~~~ ~~    ~!x.")
	print("         !!~~~             ~~~~~     ~~~~~!!_~~~~~~~~~~~~~~~~~~~~        ``~!")
	print("       !!~                 ~~~~~   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~           ~`")
	print("       !!~~                   ~~~  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     ~")
	print("       !~ ~:                  '~~~`~~~~~~~~~~~~~~~~~~~~~~~~~~~~             '")
	print("      J~   ~                    ~~~~`~'~~: ~~~`~~`~~~~~~~~~~~~              ~")
	print("      X!                        '~~~~~~~~~~~~~:~    ~~  ~~~_~              '~")
	print("      R~                          `~ ~ ~  ~`   ~        `~                 ~~")
	Pause()
	Home()
splash()
Home()	
	

Run()
print("Goodbye")

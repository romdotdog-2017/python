import glob
import random
import os
import re
import msvcrt
import vpk as vpklib
import json
from tqdm import tqdm
from shutil import copyfile
from colorama import init, Fore, Style
init()

class NewVPK(object):
	def __init__(self, path):
		self.vpk = vpklib.open(path)
		self.path = path
		self.name = os.path.splitext(path)[0].split("\\")[-1]
		self.selectedTypes = None
		self.files = None
		types = []
		for file in self.vpk.items():
			#file[0] is the name
			fileName, fileExtension = os.path.splitext(file[0])
			if not (fileExtension in types):
				types.append(fileExtension)
		self.types = types
		

	def analyzeToTypes(self):
		files = {}
		for fileType in self.types:
			files[fileType] = []
		for file in self.vpk.items():
			fileName, fileExtension = os.path.splitext(file[0])
			if (fileExtension in self.types):
				files[fileExtension].append(file[0])
		self.files = files

class WindowsFS(object):
	def __init__(self, path):
		self.path = path
		self.name = os.path.splitext(path[:-1])[0].split("\\")[-1]
		self.selectedTypes = None
		self.files = None
		self.items = [r+f for r,d,f in os.walk(path)]
		types = []
		for file in self.items:
			#file[0] is the name
			fileName, fileExtension = os.path.splitext(file)
			if not (fileExtension in types):
				types.append(fileExtension)
		self.types = types
		

	def analyzeToTypes(self):
		files = {}
		for fileType in self.types:
			files[fileType] = []
		for file in self.items:
			fileName, fileExtension = os.path.splitext(file[0])
			if (fileExtension in self.types):
				files[fileExtension].append(file[0])
		self.files = files


temp = r"D:\FSSTEMP"
try:
	os.mkdir(temp)
except:
	pass

options = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-+"

mainOptions = ["Unpack VPK", "Raw File System"]
repackOptions = ["Pack to VPK", "Leave as is"]

def clear():
	os.system("cls")
clear()

def choose(arr, message):
	enter = True
	toggles = [True] * len(arr)
	def reprint():
		print(Fore.YELLOW + message)
		print(Fore.YELLOW + "==Please toggle the types you want, then press enter==")
		for i, j in enumerate(arr):
			print(Fore.GREEN + "[" + options[i] + "]" + Fore.CYAN + " " + j + " (" + ("x" if toggles[i] else "") + ")")
	reprint()
	while enter:
		if msvcrt.kbhit():
			keyhit = msvcrt.getch()
			if keyhit == b'\r':
				enter = False
			else:
				key = options.index(keyhit.decode("utf-8"))
				if key < len(arr):
					toggles[key] = not toggles[key]
					clear()
					reprint()	
	types = []
	for i, fileType in enumerate(arr):
		if toggles[i]:
			types.append(fileType)
	return types

def choice(arr):
	print(Fore.YELLOW + "==Please specify an option==")
	for i, j in enumerate(arr):
		print(Fore.GREEN + "[" + options[i] + "]" + Fore.CYAN + " " + j)
	return options.index(msvcrt.getch().decode("utf-8"))

print(Fore.YELLOW + "==**File System Shuffler**==");
op1 = choice(mainOptions)
clear()
print(Fore.YELLOW + "==**Finished Product**==");
op2 = choice(repackOptions)
clear()

if op1 == 0:
	globFiles = glob.glob (r".\*.vpk")
	files = []
	for file in globFiles:
		if re.search(r"\d\d\d.vpk", file) == None:
			files.append(file)
	if len(files) == 0:
		clear()
		print(Fore.RED + "No available VPK files in directory.")
		os.system("pause")
		os.system("exit")
	print(Fore.YELLOW + "==**Available Files**==")
	fileChosen = files[choice(files)]
	vpk = NewVPK(fileChosen)
	clear()
	vpk.selectedTypes = choose(vpk.types, "==**File Types**==")
	vpk.analyzeToTypes()

	##START CORRUPTIONS!!!
	# use mkdirs
	print(Fore.WHITE)
	for i, fileType in enumerate(vpk.selectedTypes):
		sub = vpk.files[fileType]
		description = "{} Files ({} of {})".format(fileType, i+1, len(vpk.selectedTypes))
		for file in tqdm(sub, desc=description):
			try:
				toReplace = sub[random.randint(0,len(sub)-1)]
				dest = "./shuffled_" + vpk.name + "/"
				os.makedirs(dest + '/'.join(toReplace.split('/')[0:-1]), exist_ok=True)
				vpk.vpk.get_file(file).save(dest + toReplace)
			except Exception as e:
				print(e)
elif op1 == 1:
	directories = ["Current Directory"] + glob.glob('./*/')
	print(Fore.YELLOW + "==**Available Folders**==")
	directoryChosen = directories[choice(directories)]
	if directoryChosen == "Current Directory":
		directoryChosen = "./"
	folder = WindowsFS(directoryChosen)
	clear()
	folder.selectedTypes = choose(folder.types, "==**File Types**==")
	folder.analyzeToTypes()

	##START CORRUPTIONS!!!
	# use mkdirs
	print(Fore.WHITE)
	for i, fileType in enumerate(folder.selectedTypes):
		sub = folder.files[fileType]
		description = "{} Files ({} of {})".format(fileType, i+1, len(folder.selectedTypes))
		for file in tqdm(sub, desc=description):
			try:
				toReplace = sub[random.randint(0,len(sub)-1)]
				dest = "./shuffled_" + folder.name + "/"
				os.makedirs(dest + '/'.join(toReplace.split('/')[0:-1]), exist_ok=True)
				copyfile(file, dest+toReplace)
			except Exception as e:
				print(e)




os.system("pause")

# temp = "./temp"
# try:
# 	os.mkdir(temp)
# except:
# 	print("temp already exists")

# files = glob.glob ("./**/*.wav", recursive=True)

# for file1 in files:
# 	files.remove(file1)
# 	i2 = random.randint(0,len(files))
# 	file2 = files[i2]
# 	del files[i2]
# 	#file 1 to temp
# 	tempfile1 = (temp + "/" + re.search(r"[\w_]+?.wav", file1).group(0))
# 	print(tempfile1)
# 	os.rename(file1, tempfile1)

# 	#file 2 to 1
# 	os.rename(file2, file1)

# 	#tempfile to file2
# 	os.rename(tempfile1, file2)



import requests
import re
import datetime
import time
import calendar 


def get_time(text):
	first = text.find("-")
	second = text.find("-",first+1)
	day = text[:first]
	month = text[first+1:second]
	year = text[second+1:] 
	day_int = int(day)
	month_int = int(list(calendar.month_abbr).index(month))
	year_int = int(year)
	x = datetime.datetime(year_int, month_int, day_int)
	y =time.mktime(x.timetuple())
	out = str(y)
	return y

days=[]
days_data=[]
creds=[
	["u1503134","15594"],
	["u1503137","15181"],
	["u1503138","15032"],  
	["u1503140","15264"],
	["u1503141","15486"],
	["u1503143","15276"],
	["u1503145","15399"],
	["u1503146","15202"],
	["u1503147","15240"],
	["u1503148","15508"],
	["u1503149","15279"],
	["u1503151","15754"],
	["u1503153","15210"],
	["u1503154","15485"],
	["u1503155","15560"],
	["u1503157","15514"],
	["u1503158","15699"],
	["u1503159","15674"],
	["u1503161","15493"],
	["u1503162","15584"],
	["u1503163","15755"],
	["u1503164","15779"],
	["u1503165","15201"],
	["u1503167","15556"],
	["u1503168","15437"],
	["u1503169","15540"],
	["u1503170","15600"],
	["u1503171","15038"],
	["u1503172","15498"],
	["u1503173","15729"],
	["u1503175","15250"],
	["u1503176","15469"],
	["u1503177","15252"],
	["u1503179","15756"],
	["u1503184","15615"],
	["u1503186","15532"],
	["u1503188","15311"],
	["u1503189","15601"],
	["u1503190","15261"],
	["u1503191","15258"],
	["u1503192","15730"],
	["u1503193","15380"],
	["u1503194","15270"],
	["u1503195","15577"],
	["u1503197","15224"],
	["u1503198","15349"]]
#creds=[["u1503162","15584"],["u1503145","15399"]]
local_electives=["2019S8CS-A-CS468","2019S8CS-A-CS462","2019S8CS-A-CS472","2019S8CS-A-CS466","2019S8CS-A-CS464"]
global_electives = []
subjects=[]
x=0
while(x<len(creds)):
	payload = {'user': creds[x][0], 'pass': creds[x][1]}
	x+=1
	session = requests.Session()
	r = session.get('https://www.rajagiritech.ac.in/stud/Parent/varify.asp', data=payload)
	##print(r.text)
	#get cookies
	#here the session_cookies dictionary contains only one entry
	#it is the session ID
	session_cookies = session.cookies.get_dict()
	#go to attendance page
	r = requests.post('https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp', cookies=session_cookies)
	##print(r.text)
	#this is the page which displays the dropdown containing the list of semesters
	#the semester code is required to create the url to the page where attendance data is displayed
	#that url is of the form "https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp?code=2019S8CS-C" ...
	#... where 2019S8CS-C is the semester code obtained from the dropdown
	#the last entry in the dropdown is the current semester
	dropdown_page = r.text
	dropdown_list=[]
	#in the html soucrce, every entry in the dropdown is of the form <option value="2015CS-C-S1">2015CS-C-S1</option>
	while(dropdown_page.find("<option value=")!=-1):
			startIndex = dropdown_page.find("<option value=") + len("<option value=")
			endIndex = dropdown_page.find("</option>")
			dropdown_entry=dropdown_page[startIndex:endIndex]
			##print(dropdown_entry)
			dropdown_entry = dropdown_entry[dropdown_entry.find(">")+1:]
			##print("--|"+dropdown_entry+"|--")
			dropdown_list.append(dropdown_entry)
			dropdown_page = dropdown_page[endIndex+1:]
			#print(dropdown_page)

	##print(dropdown_list)
	no_of_semesters = len(dropdown_list)
	current_sem = dropdown_list[no_of_semesters-1]
	#succesfully obtained valid semester codes

	#now we can navigate to the attendance page
	attendance_page_url = "https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp?code="
	#append the current semester code to the url
	attendance_page_url += current_sem
	##print(attendance_page_url)
	#obtain souce of attendance_page_url
	semid_payload = {'code': current_sem}
	r = requests.post('https://www.rajagiritech.ac.in/stud/KTU/Parent/Leave.asp', cookies=session_cookies, data=semid_payload)
	attendance_page = r.text
	##print(attendance_page)

	#collect all useful data from attendance page
	#get the user name
	USERNAME = "Jane Doe"
	name_startIndex = attendance_page.find("Logged In User :")
	if(name_startIndex!=-1):
		focus = attendance_page[name_startIndex:]
		name_startIndex = focus.find("Logged In User :")+len("Logged In User :")
		name_endIndex = focus.find("</div>")
		USERNAME = focus[name_startIndex:name_endIndex]
		#remove leading and trailing whitespaces
		USERNAME = USERNAME.strip()
		#remove multiple spaces
		USERNAME = re.sub(' +', ' ', USERNAME)
		#convert to title case
		USERNAME = USERNAME.title()
		print("--|"+USERNAME+"|--")

	#get index of first entry in table_view
	startIndex = attendance_page.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\"")
	endIndex = attendance_page.find("<!-- Detailed Ends***************** -->")
	focus = attendance_page[startIndex:endIndex]
	##print (focus)


	#loop to extract data from table
	startIndex = focus.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")
	while (startIndex!=-1):
		startIndex=startIndex+len("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")
		endIndex = focus.find("</TD>")
		day=focus[startIndex:endIndex]
		#print(day)
		temp_focus = focus[endIndex+9:focus.find("</TR>")]
		#print(temp_focus)
		
		start = temp_focus.find("font color")
		day_data=[]
		day_data.append(get_time(day))
		
		first = day.find("-")
		day_text = day[:first]
		day_int = int(day_text)
		if(day_int<10):
			day="0"+day

		day_data.append(day)

		while(start != -1):
			end = temp_focus.find("</font></TD>")
			line = temp_focus[start:end] 
			line = line[line.find(">")+1:]
			'''
			if(line==""):
				line = "-----"
			if(line in local_electives):
				line = "L_ELE"
			else:
				if (line not in subjects):
					subjects.append(line)
			'''
			if(line==""):
				line = "-----"
			if(line in local_electives):
				line = "L_ELE"
			if (line not in subjects):
				subjects.append(line)
			#print(line)	
			day_data.append(line)
			temp_focus = temp_focus[end+13:]
			start = temp_focus.find("font color")

		
		focus = focus[focus.find("</TR>")+10:]
		startIndex = focus.find("<TD valign=\"middle\" align=\"center\" bgcolor=\"#aaaaaa\" Height=\"35\" Width=\"8%\">")

		if(day_data not in days_data):
			days.append(day)
			days_data.append(day_data)
	##sort the days_data
	from operator import itemgetter
	sorted_days_data = sorted(days_data,key=itemgetter(0))

	#display the data
	i = 0
	while(i<len(sorted_days_data)):
		print(sorted_days_data[i])
		i=i+1
	print("--|"+USERNAME+"|--")




#clean the data
clean=[]
i = 0
print("\n\n")


#total array will contain total class data of all subjects
#yay!

total = []
for z in range (len(subjects)):
	total.append(0)

print ("NON_ELECTIVES are :",subjects)
print ("LOCAL_ELECTIVES are :",local_electives)
print ("GLOBAL_ELECTIVES are :",global_electives) 
print ("\nALL :",subjects,"\n")

while(i<len(sorted_days_data)):
	#for each entry in sorted_days_data...
	focus_group=[]
	focus_group.append(sorted_days_data[i])
	#find entries with same day info and add it to focus_group
	j=i+1
	while(True):
		if (j >= len(sorted_days_data)):
			break
		if(sorted_days_data[j][1]==sorted_days_data[i][1]):
			focus_group.append(sorted_days_data[j])
			j=j+1
		else:
			break

	out = focus_group[0]
	if(len(focus_group)==1):
		donothing=0
		##print(">>>FOCUS GROUP for "+sorted_days_data[i][1]+" is ")
		##print("\t",focus_group[0])
	else:
		##print("---FOCUS GROUP for "+sorted_days_data[i][1]+" is ")
		missing=[]
		for k in range (len(focus_group)):
			##print("\t",focus_group[k])
			if(k == 0):
				for a, b in enumerate(focus_group[k]):
					if (b == '-----'):
						missing.append(int(a))
				##print("missing elements are ",missing)
			else:
				for l in range (len(missing)):
					if (focus_group[k][missing[l]]!="-----"):
						out[missing[l]] = focus_group[k][missing[l]]

	print("OUT IS->",out)
	#add to total class of each class in out
	p=2
	while (p<len(out)):
		ind = subjects.index(out[p])
		total[ind] = total[ind] + 1
		p = p + 1

	clean.append(out)
	i=j

print("\n")

for i in range (len(subjects)):
	print (subjects[i],"--",total[i])

timetable = [
	['CS402', 'LIBRY', 'CS404', 'G_ELE', 'CS492', 'CS492', 'CS492'],
	['CS402', 'CS404', 'L_ELE', 'G_ELE', 'CS492', 'CS492', 'CS492'],
	['L_ELE', 'CS492', 'CS492', 'CS492', 'CS492', 'CS492', 'CS492'],
	['L_ELE', 'CS404', 'CS402', 'G_ELE', 'CS492', 'CS492', 'CS492'],
	['CS404', 'CS402', 'L_ELE', 'G_ELE', 'CS492', 'CS492', 'CS492']
	]


			

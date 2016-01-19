import requests as rq
from bs4 import BeautifulSoup
import os
import errno
import csv
from urllib import parse

dictionary_All_user_names = {1: 'dexter2016', 2 : 'mustafaihssan'}

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def dic_names(op):
	if parse.unquote(op) not in dictionary_All_user_names.values(): # dictionary_All_user_names.has_key(op)
		key = list(dictionary_All_user_names)[-1] + 1
		dictionary_All_user_names[key] =  parse.unquote(op)
		w = open("t/dictionary_All_user_names.txt",'w+',encoding='utf-8')
		w.write(str(dictionary_All_user_names))	
		w.close() 
		return key
	else:
		for key in dictionary_All_user_names.keys():
			if op == dictionary_All_user_names[key]:
				return key;

# def make_file(date, path):

# 	make_sure_path_exists(path)
# 	with open(path, 'w') as csvfile:
#        writer = csv.writer(csvfile)

#         # name = name of the poster
#         # post = the post contant 
#         # father_post_num = the post is replay to 
#         # OP   = the OP number
#         # time = what time it was posted
#         # points = upvoted  

#         writer.writerow(('name', 'post', 'father_post_num','OP', 'time', 'points'))

#         writer.writerows(
#             (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project in projects
#         )

def trade_spider(max_pages):
	page = 0
	while page <= max_pages:
		page += 1
		url = "https://io.hsoub.com/go/" + str(page)  #str(page)
		print(url)
		source_code = rq.get(url)
		plain_text  = source_code.text
		soup = BeautifulSoup(plain_text, 'html.parser')

		# All_Users_name
		All_Users = []
		for link in soup.findAll('a',{'class':'usr26'})[1:]:
			All_Users.append(link.get('href')[3:])

		# post
		int = 1
		bol = False
		for link in soup.findAll('div',{'class':'commentContent post_content'}):
			bol = True
			link = str(link.contents)
			User_key = dic_names(All_Users[int-1])
			
			path = "t/Page_"+ str(page)
			text = "/P_"+str(int)+"-U_"+str(User_key)+".txt"
			make_sure_path_exists(path)
			fw = open(path+text,'w+',encoding='utf-8')
			fw.write(link)	
			fw.close()
			int += 1

		# tree
		tree = []
		int = 1
		for comment in soup.findAll('div',{'class':'comment'}):
			tree.append(comment['class'])
			int+=1
		for item in tree:
			lvl = (float(item[2][4]))
			#print(("	"*round(lvl)), end="")
			#print(item)
		
		# op
		if soup.findAll('div',{'class':'commentContent post_content'}):
			OP_Name			   = soup.find('a',{'class': 'usr26'}).text
			OP_Post 		   = " "
			if not str(soup.find('div',{'class': 'articleBody'})):
				OP_Post	       = soup.find('div',{'class': 'articleBody'}).text
			OP_Positive_Points = soup.find('a',{'class': 'positive'}).text
			OP_Negative_Points = soup.find('a',{'class': 'negative'}).text

			OP_key = dic_names(OP_Name)
			op_data = {OP_Name,OP_key,OP_Post,OP_Positive_Points,OP_Negative_Points}

			text = "/11_OP_"+str(page)+"-U_"+str(OP_key)+".txt"
			w = open(path+text,'w+',encoding='utf-8')
			w.write(str(op_data))	
			w.close()

		


			

trade_spider(34555)





# https://io.hsoub.com/go/34075  
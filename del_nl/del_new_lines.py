file_name = input() + ".txt"
myfile = open(file_name,"rt", encoding = 'UTF8')
myfile.seek(0)
context = myfile.read()
context = context.replace("\n","")
myfile = open("after_"+file_name, "wt", encoding = 'UTF8')
myfile.write(context)
myfile.close()

import requests
import csv
from bs4 import BeautifulSoup
url = "https://nces.ed.gov/COLLEGENAVIGATOR/"
home="?s=all&sp=4&pg="

hrefs= list()

def fetch(p):
    r = requests.get(url+home+p)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find('tr', class_ = 'resultsW')

    t=res.contents[2]
    a=t.contents[0]
    h=a.get('href')
    hrefs.append(h)

    siblings = res.find_next_siblings('tr')
    for t in siblings:
        t = t.contents[2]
        a = t.contents[0]
        h=a.get('href')
        hrefs.append(h)


# for i in range(1,2,1):
#     s=str(i)
# #     fetch(s)
# hrefs.append('?s=all&sp=4&pg=1&id=100654')
# hrefs.append( '?s=all&sp=4&pg=2&id=138947')
# hrefs.append( '?s=all&sp=4&pg=1&id=237215')

fetch("0")


titles=["Name","Street","City","State","Zip","Phone","Website","Type","Awards","Campus Setting"," Campus Housing","Student Population","Student to Faculty ratio"]

data= list()
def getCollegeInfo(link):
    
    collegeInstance = list()
    r = requests.get(url+link)
    html = r.content
    Collegesoup = BeautifulSoup(html, 'html.parser')

    collegeDash = Collegesoup.find('div',class_ = 'divInst')
    par = collegeDash.find_next_sibling()
    collegeInfo=par.get_text(separator=", ")
    temporary=collegeInfo.split(',')
    collegeInfo=collegeInfo.split(',')

    temporary.pop(0)
    temporary.pop(-2)
    temporary.pop()

    street=""
    for i in temporary:
        if(street==""):
            street+=i
        else:
            street=street+","+i
    

    collegeInstance.append(collegeInfo[0])
    collegeInstance.append(street)
    collegeInstance.append(collegeInfo[-2])

    StatePin=collegeInfo[-1].rsplit(" ",1)

    collegeInstance.append(StatePin[0])
    collegeInstance.append(StatePin[1])
    
    srb = Collegesoup.find_all('td', class_ = 'srb')
    for elem in srb:
        sib = elem.find_next_sibling()
        text = sib.get_text(separator=", ").strip()    
        collegeInstance.append(text)
    print(collegeInstance)
    data.append(collegeInstance)


for link in hrefs:
    column=0
    getCollegeInfo(link)

filename = "output.csv"
    
# writing to csv file 
with open(filename, 'w', newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(titles) 
        
    # writing the data rows 
    csvwriter.writerows(data)


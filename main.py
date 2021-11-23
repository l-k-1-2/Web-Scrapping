import requests
import xlsxwriter
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


# for i in range(5,8,1):
#     s=str(i)
#     fetch(s)
# hrefs.append('?s=all&sp=4&pg=1&id=100654')
# hrefs.append( '?s=all&sp=4&pg=2&id=138947')
# hrefs.append( '?s=all&sp=4&pg=1&id=237215')

fetch("0")

wb=xlsxwriter.Workbook('output.xlsx')
worksheet=wb.add_worksheet()
row=0
column=0

titles=["Name","Street","City","State","Zip","Phone","Website","Type","Awards","Campus Setting"," Campus Housing","Student Population","Student to Faculty ratio"]
bold = wb.add_format({'bold': True})

for i in titles:
    worksheet.write(row, column,i,bold)
    column+=1
row+=1
def getCollegeInfo(link, row, column):
    
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
            
    print(collegeInfo[0])
    print(street)

    worksheet.write(row, column, collegeInfo[0])
    column+=1
    worksheet.write(row, column, street)
    column+=1
    worksheet.write(row, column, collegeInfo[-2])
    column+=1

    StatePin=collegeInfo[-1].rsplit(" ",1)
    worksheet.write(row, column, StatePin[0])
    column+=1
    worksheet.write(row, column, StatePin[1])
    column+=1
    
    srb = Collegesoup.find_all('td', class_ = 'srb')
    for elem in srb:
        sib = elem.find_next_sibling()
        text = sib.get_text(separator=", ").strip()
        
        worksheet.write(row, column, text)
        column+=1

for link in hrefs:
    column=0
    getCollegeInfo(link, row, column)
    row+=1

wb.close()



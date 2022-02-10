import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib import parse


wsu_headers = {
    'Host': 'cardinal.wayne.edu',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Origin': 'https://wayne.edu',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://wayne.edu/',
    'Accept-Language': 'en,en-CA;q=0.9,en-US;q=0.8,bn;q=0.7',
}
    
def checkCourse(url, courseSearch):
    college=parse.parse_qs(parse.urlparse(url).query)['name'][0]
    response=requests.get(url, headers=wsu_headers)
    html = response.content.decode('ISO-8859-1') 
    html= html.replace("&nbsp;", "")
    html= html.replace("\r", "")
    for (courseNum, courseTitle, courseWayne) in re.findall(r'<td>(.*)<\/td>[\r\n]+.*<td>(.*)<\/td>[\r\n]+.*<td>(.*)', html):
        if(courseWayne == courseSearch):
            print(college, "----", courseTitle, "----", courseNum)
            

def checkSchool(course):
    #MICHIGAN SCHOOLS
    data = {
      'school': '',
      'STAT': 'MI',
      'NATN': '',
      'Submit32': 'Submit'
    }
    response = requests.post('https://cardinal.wayne.edu/transfer/tc_search_results.cfm', headers=wsu_headers, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    web_url='https://cardinal.wayne.edu/transfer/'
    for a in soup.find_all('a', href=True):
        theurl= a['href']
        finalurl=urljoin(web_url,theurl)
        if "name=" in finalurl:
            checkCourse(finalurl, course)
            
        

def getInput():
    print("-------------------------------------------------------------------------------------")
    print("\t\t\tCourse Equivalency Program")
    print("-------------------------------------------------------------------------------------")
    course=input("What course equivalent are you looking for? (e.g. BE2100) :  ").upper()
    print("-------------------------------------------------------------------------------------")
    print("Searching Courses With Wayne State University Course Equivalent:" , course)
    print("-------------------------------------------------------------------------------------")
    checkSchool(course)
    

getInput()
from bs4 import BeautifulSoup
htmltxt = "<p>Hello World</p>"
soup = BeautifulSoup(htmltxt,features="html.parser")
print(soup.text)
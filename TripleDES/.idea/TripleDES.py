import urllib.request
from bs4 import BeautifulSoup
import webbrowser

# specify the URL of the HTML file
url = 'file:///C:/FIEK/V2 S2/Data Security/TripleDES/TripleDES/.idea/index.html'

# open the URL and read the HTML content
html = urllib.request.urlopen(url).read()

# create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# extract the information you need
title = soup.title.string

webbrowser.open_new_tab(url)

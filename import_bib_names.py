import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.babynames.org.uk/biblical-baby-names-list.htm')
soup = BeautifulSoup(r.text, 'lxml')

# print(soup.prettify())

bib_names = (soup.find_all(style="width: 210px"))
# bib_names_final = bib_names

final_bib_names = []
for row in bib_names:
    row = row.get_text().replace(u'\xa0',u'').replace(' - ', '').encode("ascii").split('Biblical')
    for name in row:
        final_bib_names.append(name)

# print final_bib_names

writer = open('bib_names_list.txt', 'w')
writer.writelines(["%s\n" % name for name in final_bib_names])
writer.close()
#
# test = open('bib_names_list.txt', 'r')
# for name in test:
#     print name
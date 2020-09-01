from xml.etree import ElementTree

# parse() 함수로 파일을 읽고 ElementTree 객체를 생성
tree = ElementTree.parse('test.xml')

# getroot() 메서드로 XML의 루트 element를 추출
root = tree.getroot()

import pandas as pd

data = []
for item in root.findall('ArMap'):
    # find() 메서드로 element 탐색, text 속성으로 값을 추출
    sggcd = item.find('sggcd').text
    sggnm = item.find('sggnm').text
    link = item.find('tmalistlink').text
    dataframe = pd.DataFrame({
        '시구군코드':[sggcd],
        '시구군':[sggnm],
        'URL':[link],
    })
    data.append(dataframe)

result = pd.concat(data)
result
# coding=utf-8
import os,json,urllib2,zlib,re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
''' 从新房首页获取城市列表，此处获取不全 '''
def get_text(url):
    res=urllib2.urlopen(url)
    content=zlib.decompress(res.read(),16+zlib.MAX_WBITS)
    soup=BeautifulSoup(content,'lxml')
    city_list=soup.find_all('div',class_='city20141104nr',style='display:none')
    lis=[]
    dic_city={}
    for i in city_list:
        #print len(i.find_all('a'))
        lis+=i.find_all('a')
    for i in lis:
        city_name = str(i).split('>')[1].encode('gbk').strip('</a')
        dic_city[city_name] = i['href']
    return dic_city
'''获取各城市所有页面'''
def get_city_page(city_url):
    res=urllib2.urlopen(city_url)
    content=zlib.decompress(res.read(),16+zlib.MAX_WBITS)
    #html = re.sub("</html>","",content,flags=re.S|re.IGNORECASE)+"</html>"
    soup=BeautifulSoup(content,'html5lib')
    #print soup.encode('gbk')
    for i in  soup.find_all('div',class_='page'):
        nextpage=i.find('a',class_='next')['href'].split('/')[-2].split('b')[-1].encode('gbk')
        print nextpage
        print nextpage[-1]
        lastpage=i.find('a',class_='last')['href'].split('/')[-2].split('b')[-1]
        print i.find('a',class_='last')['href']
        print lastpage
        print lastpage[1:len(lastpage)]
        city_page_list=[city_url]
        for i in range(int(nextpage[-1]),int(lastpage[1:len(lastpage)])):
            city_page_list.append(city_url+'b9'+str(i)+'/')
        return city_page_list


def get_newhourse_info2(city_list):
    path = 'E:\\sf-2\\'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass
    for keys in city_list:
        f = open(path + keys + '.txt', 'w+')
        f.write('name' + '\t' + 'address' + '\t' + 'price' + '\n')
        for citypage in get_city_page(city_list[keys]):
            print citypage
            info = urllib2.urlopen(citypage)
            info2 = zlib.decompress(info.read(), 16 + zlib.MAX_WBITS)
            soup = BeautifulSoup(info2, 'html5lib')
            soup_list = soup.find_all('div', class_='nlc_details')
            soup_list_scond = soup.find_all('div', class_='sslalone')
            if len(soup_list) > 1:
                print soup_list
                for i in soup.find_all('div', class_='nlc_details'):
                    # print str(i.find('div',class_='nlcd_name')).strip('</a>').encode('gbk')
                    try:
                        name = \
                        str(i.find('div', class_='nlcd_name')).split('target="_blank">')[-1].strip('</a>').split('\n')[
                            1].strip('')  # .encode('gbk')
                        name1 = re.sub('\t', '', name)
                    except:
                        name1 = ''
                    try:
                        address = i.find('div', class_='address').a['title']  # address
                    except:
                        address = ''
                    try:
                        tel = i.find('div', class_='tel').p.encode('gbk')
                        tel2 = re.sub('<span>', '', tel)
                        tel21 = re.sub('</span>', '', tel2)
                        tel3 = re.sub('</?p>', '', tel21)
                    except:
                        tel3 = ''
                    try:
                        price = str(i.find('div', class_='nhouse_price').span)  # .encode('gbk')
                        price1 = re.search('[0-9]+', price).group()
                    except:
                        price1 = ''
                    try:
                        state = str(i.find('div', class_='fangyuan')).encode('gbk')
                        state1 = re.sub('<|>|=|/|\w+', '', state)
                    except:
                        state1 = ''
                    print name1, tel3, address, price1
                    f.write(name1 + '\t' + address + '\t' + price1 + '\n')
            elif soup_list_scond:
                print soup_list_scond
                for i in soup_list_scond:
                    try:
                        name = i.find('dl', class_='clearfix').dt.img['alt']  # .encode('gbk')
                    except:
                        name = ''
                    try:
                        price1 = i.find('dl', class_='clearfix').dd.find('div',
                                                                         class_='fr')  # find_all('dd',class_='pt08')#.encode('gbk')
                        price = re.search('\d{4,8}', str(price1)).group()  # .encode('gbk')
                    except:
                        price = ''
                    try:
                        adress1 = str(i.find('dl', class_='clearfix').find('div', class_='fl add')).split('<a>')[
                            -1]  # .encode('gbk')
                        adress = re.split('</a>', adress1)[0]  # .encode('gbk')
                    except:
                        adress = ''
                    f.write(str(name) + '\t' + str(adress) + '\t' + str(price) + '\n')


if __name__ == '__main__':
    city_list = get_text('http://newhouse.fang.com/house/s/')

    get_newhourse_info2(city_list)
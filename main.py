#-*- codeing = utf-8
from bs4 import BeautifulSoup
import re         #正则表达式，用于文字匹配
import urllib.request,urllib.error #指定url，获取网页数据
import xlwt      #进行excel操作
def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)

    #./表示保存在当前文件夹下
    savepath = ".\\豆瓣电影Top250.xls"
    #3.保存数据
    saveData(datalist,savepath)

#全局变量，正则的具体应用
#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     #compile创建正则表达式对象，表示规则（字符串的模式） #r+单引号，忽视所有的特殊符号
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   #re.S 让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>') #/d表示数字
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S) #?:0次或一次

#爬取网页
def getData(baseurl):
    datalist = [] #列表存储网页获取的数据

    for i in range(0,10):       #每页25条数据，调用获取页面信息的函数，10次
        url = baseurl + str(i*25)
        html = askURL(url)      #保存获取到的网页源码，访问一次，获取一页

         # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser") #使用html.parser解析器
        for item in soup.find_all('div',class_="item"):     #查找符合要求的字符串，形成列表/循环查找每个电影的信息
            #class_类别要加下划线
            #print(item)   #测试：查看电影item全部信息

            data = []    #保存一部电影的所有信息
            item = str(item)

            #接下来利用re库通过正则表达式查找信息
            #影片详情的链接
            link = re.findall(findLink,item)[0]     #re库用来通过正则表达式查找指定的字符串/两个参数，前者为规则，后者为要筛选的字符串/0表示找符合要求的第一个值
            data.append(link)                       #列表里添加链接

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)                     #添加图片

            titles = re.findall(findTitle,item)     #片名可能只有一个中文名，没有外国名
            if(len(titles) == 2):
                ctitle = titles[0]                  #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #去掉无关的符号
                data.append(otitle)                 #添加外国名
            else:
                data.append(titles[0])
                data.append(' ')        #外国名字留空(保证后续信息不受影响)

            rating = re.findall(findRating,item)[0]
            data.append(rating)                        #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)                       #提加评价人数

            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace("。","")    #去掉句号
                data.append(inq)                #添加概述
            else:
                data.append(" ")                #有的没有概述，留空

            bd = re.findall(findBd,item)[0]    #电影信息
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)   #通过替换去掉<br/>
            bd = re.sub('/'," ",bd)     #替换/
            data.append(bd.strip())     #strip()去掉前后的空格

            datalist.append(data)       #把处理好的一部电影信息放入datalist

    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 94.0.4606.71 Safari / 537.36 SE 2.X MetaSr 1.0"
    }
    #访问网页
    request = urllib.request.Request(url,headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request) #接受网页返回的信息
        html = response.read().decode("utf-8")  #解析response
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#保存数据
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象，后一参数：样式压缩
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)    #创建工作表,后一参数：每一单元输入覆盖以前的内容
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])      #数据

    book.save(savepath)       #保存

if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
    print("爬取完毕！")
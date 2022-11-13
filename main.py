import requests
from bs4 import BeautifulSoup
from lxml import etree
from flask import Flask, request, url_for, redirect, render_template

# create flask app
app = Flask('testapp')


# find numbers by html class
def findByClass(url, html_class):
    templist = []  # list of numbers
    req = requests.get(url)
    page = BeautifulSoup(req.content, 'html.parser')
    for number in page.find_all(class_=html_class):
        templist.append(number.text)
    nums = list(map(lambda sub: int(''.join([n for n in sub if n.isnumeric()])), templist))  # string to int
    return nums


# get paragraph from MIT by XPATH
def getParagraph():
    info = "From MIT: "
    url = 'https://news.mit.edu/2021/covid-masks-environment-0720'
    req = requests.get(url)
    page = BeautifulSoup(req.text, 'html.parser')
    about = etree.HTML(str(page))
    infolist = about.xpath('//*[@id="block-mit-content"]/div/article/div/div[7]/div[1]/div/div/p[3]/text()')
    infolist.extend(about.xpath('//*[@id="block-mit-content"]/div/article/div/div[7]/div[1]/div/div/p[5]/text()'))
    info += str(infolist[0])
    info += " "
    info += str(infolist[1])
    return info  # string created from xpath scraping


# main route
@app.route('/')
def index():
    return render_template('index.html')


# case route
@app.route('/cases', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('cases.html', nums=nums, dead=dead, alive=alive, usNums=usNums, usDead=usDead, usAlive=usAlive)


# impact route
@app.route('/impact', methods=['GET', 'POST'])
def impact_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('impact.html', bl=bl, ai=ai, hl=hl, nh=nh, oh=oh, an=an, wh=wh)


# env route
@app.route('/env', methods=['GET', 'POST'])
def env_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('env.html', sus=sus)


# main function
if __name__ == "__main__":
    # get case numbers, put into list
    us_list = findByClass('https://www.worldometers.info/coronavirus/country/us/', "maincounter-number")
    canada_list = findByClass('https://www.worldometers.info/coronavirus/country/canada/', "maincounter-number")
    mexico_list = findByClass('https://www.worldometers.info/coronavirus/country/mexico/', "maincounter-number")

    # find total north american numbers
    totalNumbers = us_list[0] + canada_list[0] + mexico_list[0]
    nums = "{:,}".format(totalNumbers)

    totalDeaths = us_list[1] + canada_list[1] + mexico_list[1]
    dead = "{:,}".format(totalDeaths)

    totalRecovered = us_list[2] + canada_list[2] + mexico_list[2]
    alive = "{:,}".format(totalRecovered)

    # get total us numbers
    usNums = "{:,}".format(us_list[0])
    usDead = "{:,}".format(us_list[1])
    usAlive = "{:,}".format(us_list[2])

    # find numbers by ethnicity, convert to int from string
    eth = findByClass('https://covidtracking.com/race', "f18b9")
    bl = "{:,}".format(eth[0])
    ai = "{:,}".format(eth[1])
    hl = "{:,}".format(eth[2])
    nh = "{:,}".format(eth[3])
    wh = "{:,}".format(eth[4])
    an = "{:,}".format(eth[6])
    oh = "{:,}".format(eth[5])

    # get environmental paragraph
    sus = getParagraph()

    # run flask
    app.run()


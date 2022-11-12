import requests
from bs4 import BeautifulSoup
from lxml import etree
from flask import Flask, request, url_for, redirect, render_template

# global lists for ease
global us_list
global canada_list
global mexico_list

# create flask app
app = Flask('testapp')


# find case numbers
def findNumbers(url):
    templist = []
    req = requests.get(url)
    page = BeautifulSoup(req.content, 'html.parser')
    for number in page.find_all(class_="maincounter-number"):
        templist.append(number.text)
    nums = list(map(lambda sub: int(''.join([n for n in sub if n.isnumeric()])), templist))
    return nums


# find cases by ethnicity
def findByEthnicity():
    url = 'https://covidtracking.com/race'
    templist = []
    req = requests.get(url)
    page = BeautifulSoup(req.content, 'html.parser')
    for number in page.find_all(class_="f18b9"):
        templist.append(number.text)
    nums = list(map(lambda sub: int(''.join([n for n in sub if n.isnumeric()])), templist))
    return nums


# get paragraph from MIT
def getSusParagraph():
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
    return info


# main route
@app.route('/')
def index():
    return render_template('index.html')


# case route
@app.route('/cases', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('cases.html', nums=nums, dead=dead, alive=alive)


# impact route
@app.route('/impact', methods=['GET', 'POST'])
def impact_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('impact.html', bl=bl, ai=ai, hl=hl, nh=nh, oh=oh, an=an)


# env route
@app.route('/env', methods=['GET', 'POST'])
def env_func():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('env.html', sus=sus)


# main function
if __name__ == "__main__":
    us_list = findNumbers('https://www.worldometers.info/coronavirus/country/us/')
    canada_list = findNumbers('https://www.worldometers.info/coronavirus/country/canada/')
    mexico_list = findNumbers('https://www.worldometers.info/coronavirus/country/mexico/')

    totalNumbers = us_list[0] + canada_list[0] + mexico_list[0]
    nums = "{:,}".format(totalNumbers)

    totalDeaths = us_list[1] + canada_list[1] + mexico_list[1]
    dead = "{:,}".format(totalDeaths)

    totalRecovered = us_list[2] + canada_list[2] + mexico_list[2]
    alive = "{:,}".format(totalRecovered)

    eth = findByEthnicity()
    bl = "{:,}".format(eth[0])
    ai = "{:,}".format(eth[1])
    hl = "{:,}".format(eth[2])
    nh = "{:,}".format(eth[3])
    an = "{:,}".format(eth[5])
    oh = "{:,}".format(eth[4])

    sus = getSusParagraph()

    app.run()


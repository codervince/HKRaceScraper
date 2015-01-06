import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from tutorial.items import HKResultItem
import urlparse
import re
import string


''''
todo: have Rule callback 2nd function for odds data 
fix images 
update items - easy
postprocess - send to SQL Server 1st via SQLalchemy (later: postgres) 

'''

class RacesSpider(CrawlSpider):
    name = "HKResultsRaces"
    allowed_domains = ["racing.hkjc.com"]

    def __init__(self, racedate='', racecoursecode= ' ', *args, **kwargs):    
        super(RacesSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/%s/1' % (racedate, racecoursecode)]

    # start_urls = [
    #     'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/ST/1' % racedate
    # ]

#     rules = (Rule (SgmlLinkExtractor(allow=("index\d00\.html", ),restrict_xpaths=('//p[@id="nextpage"]',))
# , callback="parse_items", follow= True)
#     ,
# )


    rules = (
        # /racing/Info/Meeting/Results/English/Local/20150104/ST/2
        Rule(LinkExtractor(allow=('racing/Info/Meeting/Results/English/Local/.*', ), deny=('subsection\.php',)), callback='parse_items', follow=True)
        ,)

    def parse_items(self, response):
        self.log('Hi, data from items! %s\n' % response.url)
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # item = HKraces2()

        #race metadata race number, raceindex
        #class distance prizemoney? going, course if communicate with database 
        RaceNumberIndex = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[1]/text()').extract()
        RaceNumber = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[1]/text()').re(r'RACE (.*) \(')
        RaceIndex = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[1]/text()').re(r'RACE\s*\d*(.*)')
        RaceIndex2 = [ RaceIndex[0].translate('()')]

        #needs to get urls for later processing
        Url = [response.url]

        # we know that image url has certain format: http://racing.hkjc.com/racing/content/Images/RaceResult/20150104R1_S.jpg
        # imageLink = response.css('img').xpath('@src').re(r'RaceResult(.*)')
        # imageLinka = urlparse.urljoin("http://racing.hkjc.com/racing/content/Images/RaceResult", imageLink[0])
        # imageLink.insert(0,"http://racing.hkjc.com/racing/content/Images/RaceResult")

        # classDistRatingSpan = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[1]/text()').extract()
        # Going = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[3]').extract()
        # RaceName = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[2]/td[1]').extract()
        # RailType = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[2]/td[3]').extract()
        # PrizeMoney = response.xpath('/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[3]/td[1]').extract()

        # classDistRatingSpan /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[1]

        items = [] 
        for sel in response.xpath("/html/body/div[2]/div[2]/div[2]/div[6]/table/tbody"):
            Place = sel.xpath('tr/td[1]/text()').extract()
            Trainer= sel.xpath('tr/td[5]/a/text()').extract()
            HorseNo = sel.xpath('tr/td[2]/text()').extract()
            Horse = sel.xpath('tr/td[3]/a/text()').extract()
            HorseCode = sel.xpath('tr/td[3]/text()').extract()
            Jockey = sel.xpath('tr/td[4]/a/text()').extract()
            Trainer = sel.xpath('tr/td[5]/a/text()').extract()    
            ActualWt = sel.xpath('tr/td[6]/text()').extract()
            DeclarHorseWt = sel.xpath('tr/td[7]/text()').extract()
            Draw = sel.xpath('tr/td[8]/text()').extract()
            LBW = sel.xpath('tr/td[9]/text()').extract()
            RunningPosition = sel.xpath('tr/td[10]/table/tr/td/text()').extract()
            FinishTime = sel.xpath('tr/td[11]/text()').extract()    
            WinOdds = sel.xpath('tr/td[12]/text()').extract()
            item = HKResultItem()
            item["RaceIndex"] = RaceIndex2
            item["RaceNumber"] = RaceNumber
            # item["image_urls"] = imageLinka
            items.append(item)
            print(RaceNumberIndex)
            print(RaceNumber)
            print(RaceIndex)
            print(Url)
            # print(classDistRatingSpan)
            # print(Going)
            # print(RaceName)
            # print(RailType)
            # print(PrizeMoney)
            print(Place) 
            print(Trainer)
            print(HorseNo) 
            print(Horse) 
            print (HorseCode) 
            print(Jockey)
            print(Trainer) 
            print(ActualWt) 
            print(DeclarHorseWt)
            print(Draw) 
            print(LBW) 
            print(RunningPosition) 
            print(FinishTime) 
            print(WinOdds)             
        return items
          #get dividend data table
          # /html/body/div[2]/div[2]/div[2]/div[7]/table/tbody/tr/td[1]/table
          # /html/body/div[2]/div[2]/div[2]/div[7]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[3] WinDiv
          # /html/body/div[2]/div[2]/div[2]/div[7]/table/tbody/tr/td[1]/table/tbody/tr[4]/td[3] Place1Div

          #TODO: this does not print
          #GRAB image link
          #grab video link
          #pipe to CSV or better JSON- > database
    def parse_odds(self, response):
        self.log('Hi, data for odds! %s\n' % response.url)
        for sel2 in response.xpath("/html/body/div[2]/div[2]/div[2]/div[7]/table/tbody/tr/td[1]/table/tbody"):
            WinDiv = sel2.xpath('/tr[3]/td[3]/text()').extract()
            Place2Div = sel2.xpath('/tr[4]/td[3]/text()').extract()
            Place3Div = sel2.xpath('/tr[5]/td[3]/text()').extract()
            Place4Div = sel2.xpath('/tr[6]/td[3]/text()').extract()
            QNDiv = sel2.xpath('/tr[7]/td[3]/text()').extract()
            QP12Div = sel2.xpath('/tr[7]/td[3]/text()').extract()
            QP13Div = sel2.xpath('/tr[8]/td[3]/text()').extract()
            QP23Div = sel2.xpath('/tr[9]/td[3]/text()').extract()
            TierceDiv = sel2.xpath('/tr[10]/td[3]/text()').extract()
            TrioDiv = sel2.xpath('/tr[11]/td[3]/text()').extract()
            FirstFourDiv = sel2.xpath('/tr[12]/td[3]/text()').extract()
            print WinDiv, Place2Div, Place3Div   
          #scrape image http://www.hkjc.com/english/racing/finishphoto.asp?racedate=20150104R1_L.jpg
          # http://www.hkjc.com/english/racing/finishphoto.asp?racedate=20140101R1_L.jpg  


#download videos 
#a with href attr 'javascript:OpenPopWin' 
# response.xpath("//a[contains(@href,'javascript:OpenPopWin')]/@href").extract()
# gets [u"javascript:OpenPopWin('/racing/video/play.asp?type=replay-full&date=20150104&no=01&lang=eng',640,390);"]
#baseurl = 'http://racing.hkjc.com' 
#maybe generoc: /racing/video/play.asp?type=replay-full&date=20150104&no=01&lang=eng
#we know racecoursecore and date

#all info incl race

# response.xpath("//div[contains(@class,'rowDiv15')]").extract()

#to get table headers:
#response.xpath("//div[contains(@class,'clearDivFloat') and contains(@class, 'rowDiv15')]/table/thead/tr/td").extract()
#to get table data
#response.xpath("//div[contains(@class,'clearDivFloat') and contains(@class, 'rowDiv15')]/table/tbody/tr/td").extract()

#place /html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[2]/td[1]
            #response.xpath("//div[contains(@class,'clearDivFloat') and contains(@class, 'rowDiv15')]").extract()

#header  names
# response.xpath("//td[contains(@class,'raceinfoDivWidth')]/text()").extract()

#figures only
# response.xpath("//td[normalize-space(contains(@class,'raceinfoDivWidth'))]/text()").extract()

#response.xpath("//div[contains(@class,'rowDiv15')]").extract()

#everythingL
#response.xpath("//div[contains(@class,'rowDiv15')]/table/tbody/tr/td").extract()

#data from table , eacch horse
# response.xpath("//div[contains(@class,'rowDiv15')]/table/tbody/tr").extract()[0]


#trainr of horse 1 (trainer is 5th column)
# /html/body/div[2]/div[2]/div[2]/div[6]/table/tbody/tr[1]/td[5]


#img button to click to get to next races
#/html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/img
#race2 from race1
# /html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/a 
#race3 from race1
# /html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[5]/a
#last race from race1
# /html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[12]/a/
#all races
# /html/body/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[13]/a



#sectional button 
# a src attribute = /racing/Info/StaticFile/English/Images/Racing/sectional_time_btn.gif
# or: /html/body/div[2]/div[2]/div[2]/div[4]/div/a

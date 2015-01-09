import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.loader.processor import Join, MapCompose
from tutorial.items import HKResultItem
import urlparse
import re
import string
import os
import pprint

''''
todo: 

download video as file 
postprocess - e.g. incident report -> news feed
postprocess times correct format plus do some light aggregate work 
-- horsetofollow??
--> 2nd parser horseTracker ==  masterdata + news + trackwork 
DB- 1 SQL Server (later: postgres) 
Integrate sectionals data
(twitter extract tips data)
(horse data)
'''

class RacesSpider(CrawlSpider):
    name = "HKResultsRaces"
    allowed_domains = ["racing.hkjc.com", "http://www.hkjc.com", "www.hkjc.com"]

    def __init__(self, racedate='', racecoursecode= ' ', *args, **kwargs):    
        super(RacesSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/%s/1' % (racedate, racecoursecode)]
        self.racedate = racedate
        self.racecoursecode = racecoursecode
    # start_urls = [
    #     'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/ST/1' % racedate
    # ]

#     rules = (Rule (SgmlLinkExtractor(allow=("index\d00\.html", ),restrict_xpaths=('//p[@id="nextpage"]',))
# , callback="parse_items", follow= True)
#     ,
# )


    rules = (
        # /racing/Info/Meeting/Results/English/Local/20150104/ST/2
        Rule(LinkExtractor(allow=('http://www.hkjc.com/english/racing/display_sectionaltime.asp?.*', ), deny=('racing/Info/Meeting/Results/English/Local/.*',)), callback='parse_sectionals', follow=True),

        Rule(LinkExtractor(allow=('racing/Info/Meeting/Results/English/Local/.*', ), deny=('subsection\.php',)), callback='parse_raceresults', follow=True)
        ,
        

        )

    def parse_sectionals(self,response):
        #
        self.log('Hi, data from sectionals! %s\n' % response.url)
        #ex url http://www.hkjc.com/english/racing/display_sectionaltime.asp?All=0&RaceDate=04%2F01%2F2015&Raceno=4
        # filename = response.url.split("/")[-1]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # item = HKraces2()
        items = []
        for sel in response.xpath("/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody"):
            #/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[10]/div
            #SecPlace = response.xpath('/tr[4]/td[1]/div').extract()
            #SecHorseNo /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[2]/div
            #SecHorseName /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[3]/div/a
            #Sec1DBL /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[4]/table/tbody/tr/td[2] 
            #sec1Time /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[5]/td[1]
            #sec2DBL /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[5]/table/tbody/tr/td[2]
            #sec2Time /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[5]/td[2]
            #sec3DBL /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[4]/td[6]/table/tbody/tr/td[2]
            #sec3Time /html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[5]/td[3]
            Sec4Time= response.xpath("/html/body/table/tbody/tr/td[2]/table[2]/tbody/tr/td/font/a/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr[5]/td[4]")
            item = HKResultItem()
            item["Sec4Time"] = Sec4Time   
            items.append(item)
            print(Sec4Time)

        return items



    def parse_raceresults(self, response):
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
        RaceIndex2 = [ RaceIndex[0].replace('(', '').replace(')', '')] #out of range
        #needs to get urls for later processing
        Url = [response.url]
        #date and racecoursecode
        Racedate = Url[0].split('/')[-3]
        Racecoursecode = Url[0].split('/')[-2]
        Racenumber = Url[0].split('/')[-1]
         

        # we know that image url has certain format: http://racing.hkjc.com/racing/content/Images/RaceResult/20150104R1_S.jpg
        # inrace positions /20150101R1_S.jpg
        imageLink = response.css('img').xpath('@src').re(r'RaceResult(.*)')

        #construct on fly
        normalizedRaceNumber = '0' + RaceNumber[0] if int(RaceNumber[0]) < 10 else RaceNumber
        fullReplayurl = [ "http://racing.hkjc.com/racing/video/play.asp?type=replay-full&date=" + self.racedate + 
        "&no=" + normalizedRaceNumber[0] +  "&lang=eng"
        ]

        #FILES - video 
        #MULTI A  http://racing.hkjc.com/racing/video/play.asp?type=replay-full&date=20150104&no=01&lang=eng date and racenumber
        #PASS THRU http://racing.hkjc.com/racing/video/play.asp?type=passthrough&date=20150104&no=01&lang=eng date and racenumber

        imageLinka = [ "http://racing.hkjc.com/racing/content/Images/RaceResult" + imageLink[0] ] 


        #racing incident report if present
        #look for td text() contains Racing Incident Report
        if response.xpath('//td[contains(., "Racing Incident Report")]') != []:
            IncidentReport = response.xpath('//td[@class="lineH18 padding trBgBlue2"]/text()').extract()


        #odds table
        WinDiv = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[0].extract()
        Place2Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[1].extract()
        Place3Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[2].extract()
        Place4Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[3].extract()
        QNDiv = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[4].extract()
        QP12Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[5].extract()
        QP13Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[6].extract()
        QP23Div = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[7].extract()
        TierceDiv = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[8].extract()
        TrioDiv = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[9].extract()
        FirstFourDiv = response.xpath('//td[@class= "number14 tdAlignR"]/text()')[10].extract()



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
            item["Url"] = Url
            item["Racedate"] = Racedate
            item["Racecoursecode"] = Racecoursecode
            item["RaceIndex"] = RaceIndex2
            item["Horse"] = Horse
            item["IncidentReport"] = IncidentReport
            item["RaceNumber"] = RaceNumber
            item["image_urls"] = imageLinka
            item["WinDiv"] = WinDiv
            item["file_urls"] = fullReplayurl           #multiple URLS?

            if IncidentReport:
                HorseReport = ' '.join([el for el in re.findall('[A-Z][A-Z].*', IncidentReport[0]) if Horse[0] in el])  
                item["HorseReport"] = HorseReport    
            items.append(item)


            #debugging######################
            print(RaceNumberIndex)
            print(RaceNumber)
            print(RaceIndex)
            print(Url)
            print(IncidentReport)
            # print(classDistRatingSpan)
            # print(Going)
            # print(RaceName)
            # print(RailType)
            # print(PrizeMoney)
            print(Place) 
            print(Trainer)
            print(HorseNo) 
            print(Horse) 
            print(HorseCode) 
            print(Jockey)
            print(Trainer) 
            print(ActualWt) 
            print(DeclarHorseWt)
            print(Draw) 
            print(LBW) 
            print(RunningPosition) 
            print(FinishTime) 
            print(WinOdds)
            print(fullReplayurl)
            print(imageLinka)
            print(WinDiv)
            print(HorseReport)
            #####################################
            
            # Place2Div = sel2.xpath('/text()')[1].extract()
            # Place3Div = sel2.xpath('/text()')[2].extract()
            # Place4Div = sel2.xpath('/text()')[3].extract()
            # QNDiv = sel2.xpath('/text()')[4].extract()
            # QP12Div = sel2.xpath('/text()')[5].extract()
            # QP13Div = sel2.xpath('/text()')[6].extract()
            # QP23Div = sel2.xpath('/text()')[7].extract()
            # TierceDiv = sel2.xpath('/text()')[8].extract()
            # TrioDiv = sel2.xpath('/text()')[9].extract()
            # FirstFourDiv = sel2.xpath('/text()')[10].extract()
              
             
         #instea  of returning yeield another Request  e.g. yield Request(url=reqUrl,meta={'caturl':reqUrl},callback=self.getSecondCategory)                
        return items
        #yield scrapy.Request(Url[0], callback=self.parse_odds) 


   



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

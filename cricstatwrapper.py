from urllib import urlopen
from bs4 import BeautifulSoup
import io


def fetch(link) :
    seedpage_html=urlopen(link).read()
    soupify=BeautifulSoup(seedpage_html, 'html.parser')
    descriptionMeta = soupify.find("meta", { "name" : "description" })
    if(not descriptionMeta) :
        return
    else :
        descriptionMeta = descriptionMeta["content"]
    description = descriptionMeta.split(",")
    date = (description[-2]+description[-1]).strip()
    matchName = description[-3].split("at")[0]
    matchLocation = description[-3].split(" at ")[1]
    
    tables = soupify.find_all("table", "batting-table innings")
    table_soupify = BeautifulSoup(str(tables),'html.parser')
    rows = table_soupify.find_all("tr")
    player_name=""
    runs_scored=""
    minutes_batted=""
    balls_faced=""
    no_of_4s = ""
    no_of_6s = ""
    strike_rate = ""
    dismissal_info = ""
    
    for r in rows : 
        if("batsman-name" in str(r)):
            row_soupify = BeautifulSoup(str(r),'html.parser')
            player_name = row_soupify.find("a",{"class":"playerName"}).findAll(text=True)[0].strip()
            td_list = row_soupify.find_all("td")
            count=0
            for td in td_list : 
                if("dismissal-info" in str(td)):
                    dismissal_info = str(td)[len('<td class="dismissal-info">'):-len('</td>')]
                    dismissal_split = dismissal_info.split("\t")
                    dismissal_info = dismissal_split[0]
                    continue
                if("bold" in str(td)):
                    count+=1
                    runs_scored = str(td)[len('<td class="bold">'):-len('</td>')]
                    continue
                if(count==1):
                    minutes_batted = str(td)[len('<td class="">'):-len('</td>')]
                    count+=1
                    continue
                if(count==2):
                    balls_faced = str(td)[len('<td class="">'):-len('</td>')]
                    count+=1
                    continue
                if(count==3):
                    no_of_4s = str(td)[len('<td class="">'):-len('</td>')]
                    count+=1
                    continue
                if(count==4):
                    no_of_6s = str(td)[len('<td class="">'):-len('</td>')]
                    count+=1
                    continue
                if(count==5):
                    strike_rate = str(td)[len('<td class="">'):-len('</td>')]
                    count+=1
                    continue
            f = io.open("batting_stats/"+player_name+".csv", 'a')
            if("," in matchName):
                matchName = "\""+matchName+"\""
            if("," in matchLocation):
                matchLocation = "\""+matchLocation+"\""
            if("," in date):
                date = "\""+date+"\""
            csvString = date+","+matchName+","+matchLocation+","+runs_scored+","+balls_faced+","+minutes_batted+","+no_of_4s+","+no_of_6s+","+strike_rate+","+dismissal_info+"\n"
            f.write(csvString)
            csvString=""
            f.close()
            
    bowling_tables = soupify.find_all("tr")
    bowling_table_soupify = BeautifulSoup(str(bowling_tables),'html.parser')
    rows = bowling_table_soupify.find_all("tr")
    player_name=""
    overs_bowled=""
    maidens_bowled=""
    runs_conceded=""
    wickets_taken = ""
    economy = ""
    
    for r in rows : 
        if("bowler-name" in str(r)):
            row_soupify = BeautifulSoup(str(r),'html.parser')
            player_name = row_soupify.find("a",{"class":"playerName"}).findAll(text=True)[0].strip()
            td_list = row_soupify.find_all("td")
            count=0
            for td in td_list : 
                if("bowler-name" in str(td)):
                    count+=1
                    continue
                if(count==1):
                    overs_bowled = str(td)[len('<td>'):-len('</td>')]
                    count+=1
                    continue
                if(count==2):
                    maidens_bowled = str(td)[len('<td>'):-len('</td>')]
                    count+=1
                    continue
                if(count==3):
                    runs_conceded = str(td)[len('<td>'):-len('</td>')]
                    count+=1
                    continue
                if(count==4):
                    wickets_taken = str(td)[len('<td>'):-len('</td>')]
                    count+=1
                    continue
                if(count==5):
                    economy = str(td)[len('<td>'):-len('</td>')]
                    count+=1
                    continue
            f = io.open("bowling_stats/"+player_name+".csv", 'a')
            if("," in matchName):
                matchName = "\""+matchName+"\""
            if("," in matchLocation):
                matchLocation = "\""+matchLocation+"\""
            if("," in date):
                date = "\""+date+"\""
            csvString = date+","+matchName+","+matchLocation+","+overs_bowled+","+maidens_bowled+","+runs_conceded+","+wickets_taken+","+economy+"\n"
            f.write(csvString)
            csvString=""
            f.close()

fh = io.open("matchURLs.txt","r")
links = fh.readlines()
count=0
for link in reversed(links) :
    count+=1
    print str(count)+": Fetching : "+link
    try :
        fetch(link)
    except Exception, e: 
        print "Exception for "+link
        print str(e)
        exf = io.open("exceptions.txt","a")
        exf.write(unicode(str(link)+ " "+ str(e)))
#!/usr/bin/env python
 
# xdspider.py
# Usage: ./xdspider.py [commands]
# Commands                        Commands Description
# --out filename                # master output filename, will become filename_sha1-hash-of-url
# --format format               # master output format {JSON, CSV, XML}
# --import filename             # import configs from file (json only)
# --export filename             # export the default config to file (json only)
# --no-save                     # disables file output, prints output data to console
# --debug                       # enables application debugging mode
# -h                            # outputs help menu
# -?                            # outputs help menu
# -help                         # outputs help menu
#
# call via python via sh (on linux), cmd (on windows), python (multi platform) or
# mark xdspider.py as executable using command "chmod 755" on linux to call directly
#
# Name: XDSpider
# Description: A highly customizeable website site mapper spider written in python,
#              supporting link priority rating using user definable regex,
#              supporting link exclusing using user definable regex,
#              supporting link depth limiting,
#              supporting multi-threading,
#              supporting multiple site config
#
# Requirements: threading, urllib2, time, datetime, timedelta, sys, re, BeautifulSoup 4, json, hashlib, xml.sax.saxutils
#              
# Version: 2.0.0.0-stable
# Author: Dean Van Greunen
# Email Addresses: deanvg9000@gmail.com | evoprogrammer@gmail.com
# Keybase: https://www.keybase.io/DeanVanGreunen
# Copyright: Dean Van Greunen (c) 2017. All Rights Reserved.
#
# EULA (End User License Agreement):
#     Use of XDSpider is granted for commercial or personal.
#     Modification of XDSpider is DENIED.
#     Selling of XDSpider is DENIED.
#     Distribution of XDSpider is DENIED, A distro of XDSpider can be obtained by emailing deanvg9000@gmail.com
#
#     Do not edit this "EULA" (defined above)
#     breaking license agreements or failing to comply is a legal offence under international and local governing laws.

def XDSpider_Version():
    return "2.0.0.0-stable"

import threading
import urllib2
import time
from datetime import datetime, timedelta
import sys
import re
from bs4 import BeautifulSoup
import json
import hashlib
from xml.sax.saxutils import escape
configs_ = {
            "force2https": 0,           # forces application to parse all links with only https.
            "follow_redirects" : 1,     # application accepts and follows all redirects.
            "multi_threaded": 1 ,       # use for multi threading.
            "format":"xml",             # default output format (xml, csv, json).
            "depth" : 1,                # default of 1 links deep per link from base link. from page x to page a->b.
            "save2file" : 1,            # if set will output to file.
            "exclusion_list": [         # default is None, Set to a list of strings in the form of a regex "file.extension".
            ],
            "rating":[                 # global ratings for links using regex,
                                       # parsing down, the link which best matches will be used.
                {
                    "regex":"^.*\\.example\\.com.*$",
                    "value":1.00
                },
                {
                    "regex":"^.*$",
                     "value":0.80
                }
            ],
            "remove": [                 # if any of the listed is in the link then it removes it.
            ],
            "websites": [
                {
                    "output":"sitemap.xml",
                    "format":"xml",
                    "url":"http://www.example.com/",
                    "depth" : 2,
                    "allow_linked_domains":1
                }
            ],
            "headers": {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0",
                "Accept-Language":"en-US,en;q=0.5",
                "Upgrade-Insecure-Requests":1,
                "Connection":"keep-alive",
                "Referer":""
            }
    } #because static doesn't exist :/

counter = 0
class XDSpider(threading.Thread):
    prop_re    = None   # compiled regex
    debug      = False  # used for debugging purposes only
    spidering  = False  # used for tread (only allow spider to be called once)
    configs    = dict() # empty list for configs
    links      = list() # empty list for storage of valid links
    failed     = list() # empty list for storage of error links (everything but 200 (4XXs, 5XXs....))

    #threaded - single (one class instance per site)
    #url = url to spider
    #lvl = depth
    def StartSpider(self, configs):
        global configs_
        self.configs = configs
        self.configs["site_time"] = 0
        try:
            self.configs["depth"] = configs["depth"]
        except:
            self.configs["depth"] = configs_["depth"]
        try:
            self.configs["rating"] = configs["rating"]
        except:
            self.configs["rating"] = configs_["rating"]
        try:
            self.configs["remove"] = configs["remove"]
        except:
            self.configs["remove"] = configs_["remove"]
        try:
            self.configs["format"] = configs["format"]
        except:
            self.configs["format"] = configs_["format"]
        try:
            self.configs["output"] = configs["output"]
        except:
            self.configs["output"] = "sitemap_"+configs["url"].replace("http://","").replace("https://","").replace("/","-").replace(".","_")
        try:
            self.configs["allow_linked_domain"] = configs["allow_linked_domain"]
        except:
            self.configs["allow_linked_domain"] = 1
        try: 
            if self.configs["exclusion_list"] == None:
                self.configs["exclusion_list"].update(configs_["exclusion_list"])
        except:
            self.configs["exclusion_list"] = configs_["exclusion_list"]
        if self.debug:
            print(self.configs)
        return

    def run(self):
        global configs_
        if self.configs["url"] == None:
            print("Error - Blank Website Url or Configs Broken.")
            return
        gen_start = time.time()
        self.links.append(self.configs["url"])
        print("> Starting: " + self.configs["url"])
        self.Spider(self.configs["url"],int(self.configs["depth"]))
        gen_end = time.time()
        self.configs['site_time']  = str(gen_end - gen_start)
        if configs_['save2file']:
            print("> Dumping " + self.configs["url"] + " to " + self.configs['output'])
            f = open(self.configs['output'],"w")
            f.write(self.Output())
            f.close()
        else:
            print self.Output()
        print("> Completed: " + self.configs["url"])
        return

    def Output(self):
        if self.configs["allow_linked_domains"] != 1:
            links = []
            links.append(self.configs["url"])
            for x in self.links:
                if x != None:
                     if self.configs["url"] in x:
                         links.append(x)
            self.links = links
        
        if self.configs['format'] == "xml":
            return self.OutputXML()
        if self.configs['format'] == "json":
            return self.OutputJSON()
        if self.configs['format'] == "csv":
            return self.OutputCSV()
        return "Output Error - No Format Specified"

    def Spider(self, url, lvl=4, scheme="", domain="", port=""):
        if lvl == None or int(lvl) <= 0:
            return
        if not self.include(url):
            return
        if self.configs["allow_linked_domains"]==0:
            if self.configs["url"] not in url:
                return
        if scheme == "" or domain == "" and url != "":
            self.prop_re = re.compile("^(https?:\/\/)([^\/]+):(\d+)/?(.+)")
            url = "".join(url).encode('ascii','ignore')
            rex = self.prop_re.search(url)
            if rex != None:
                scheme = rex.group(1)
                domain = rex.group(2) 
                port = rex.group(3)
            else:
                self.prop_re = re.compile("^(https?:\/\/)([^\/]+)/?(.+)")
                rex = self.prop_re.search(url)
                if rex != None:
                    scheme = rex.group(1)
                    domain = rex.group(2) 
                    port = ""
             
        if url[0] == "#":
            return

        _links = self.getPageLinks(self.getHTML(self.fixURL(url,scheme, domain,port)),scheme, domain,port)

        _links = self.unique(_links)
        _links = self.excluded_exclusions(_links)

        if _links != None:
            for __link in _links:
                if __link != None:
                    __link = self.fixURL(__link,scheme, domain,port)
                    if __link not in self.links:
                        self.links.append(__link)
                        self.Spider(__link, lvl-1,"")        
        return

    def include(self, link):
        for str_ in self.configs["exclusion_list"]:
            if str_ in link:
                return False
        return True

    def fixURL(self, url, scheme, domain,port):
        if url != None:
            if url[0] != "/" and url[0] != "h":
                url = "/"+url
            url = ((scheme + domain + (":"+port if port!="" else "") + url) if url[0] == "/" else url)
        return url
    # Bounce if depth reached
    # GetLinksFromLinks
    # BounceLinks till no more found
    # downloader + retries of 3
    def getHTML(self, link, retries=3):
        global debug
        global counter
        #downloads page and returns html data
        while retries>=0:
            try:
                if debug:
                    counter+=1
                    print("> ["+str(counter)+"] Scanning "+str(link))
                response = urllib2.urlopen(link)
                html = response.read()
                response.close()
                return html
            except Exception as e:
                self.failed.append(link)
                if debug:
                    print(e)
            retries = retries-1
        return ""

    #parser            
    def getPageLinks(self, html_page_data, scheme, domain, port):
        global debug
        soup = BeautifulSoup(html_page_data, 'html.parser')
        links = list()
        a_s = soup.find_all('a')
        a_s = self.unique(a_s)
        for link in a_s:
            if link != None:
                url = None
                try:
                    url = link['href'] if link['href'] else None
                except:
                    pass
                if url != None:
                    if url[0] == "#":
                        continue
                    if "javascript" in url:
                        continue
                    if "mailto" in url:
                        continue
                    if "tel" in url:
                        continue
                    url = self.fixURL(url,scheme, domain,port)
                    links.append(url)
        return self.unique(links)

    def ticktotimestr(self, t):   
            d = [10000,60,60,24,365]
            s = ["seconds", "minutes", "hours", "days", "years"] 
            i = 0
            for x in d:
                if t >=x:
                    t = float(t / x)
                    i = i + 1
            return str(t)+str(s[i])

    def unique(self, y):
        # order preserving
        noDupes = []
        [noDupes.append(i) for i in y if not noDupes.count(i)]
        return noDupes

    def excluded_exclusions(self, y):
        # order preserving
        noExcludes = []
        [noExcludes.append(i) for i in y if self.include(i)]
        return noExcludes

    def Help():
        print("> python xdspider.py [--urls http://ww.example.com/] [--file <siteurls.csv> ] [--get-defaults] [--get-defaults-save <config.ini>] [--configs <config.ini>] [--format <XML|CSV|JSON>]")
        return None

    def OutputXML(self):
        gen_start = time.time()
        data=""
        head='<?xml version="1.0" encoding="UTF-8"?>'+"\r\n"
        data+='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'+"\r\n"
        for link in self.links:
            if link != None:
                data+="    <url>"+"\r\n"
                data+="        <loc>"+escape(str("".join(link)))+"</loc>"+"\r\n"
                data+="        <changefreq>"+["daily","weekly","monthly","yearly"][0]+"</changefreq>"+"\r\n"
                data+="        <priority>"+str(self.getPriority(link))+"</priority>"+"\r\n"
                data+="    </url>"+"\r\n"
        data+='</urlset>'+"\r\n"
        gen_end = time.time()
        gen_time = (gen_end-gen_start)
        comments = "<!-- Time Taken To Parse Site: "+self.ticktotimestr(float(self.configs["site_time"]))+" -->\r\n"
        comments += "<!-- Time Taken To Gen Sitemap: "+self.ticktotimestr(float(gen_time))+" -->\r\n"
        comments += "<!-- Total Time Elapsed: "+self.ticktotimestr(float(self.configs["site_time"])+gen_time)+" -->\r\n"
        comments += "<!-- Total Links: "+str(len(self.links))+" -->\r\n"
        return str(head+comments+data)

    def getPriority(self, link):
        priority = 0 # default of 1
        if self.configs["rating"] != None:
            for rex in self.configs["rating"]:
                c_rex = re.compile(rex["regex"])
                m_rex = c_rex.match(link)
                if m_rex != None:
                    x = rex["value"]
                    if x >= priority:
                        priority = x
        return priority

    def OutputJSON(self):
        data=""
        data+=('[')+"\r\n"
        data+=('    urls: [')+"\r\n"
        for link in self.links:
            data+='{'+"\r\n"
            data+='"loc":"'+link+'"'+"\r\n,"
            data+='"changefreq":"'+["daily","weekly","monthly","yearly"][3]+'"'+"\r\n,"
            data+='"priority":"1.00"'+"\r\n"
            data+='}'+"\r\n"
        data+=']'+"\r\n"
        return data

    def OutputCSV(self):
        data=""
        for link in self.links:
            data+=link+"\r\n"
        return data

def main():
    global configs_
    global debug
    configs_['save2file'] = 1
    print("XDSpider - Version "+ XDSpider_Version())    
    args_x = sys.argv # + list("--debug") #+ list({"--configs configs.json --debug --out sitemap --format xml"})
    args_x = " ".join(args_x).split(" ")
    if len(args_x) == 1:
    	print("> try using -h")
    	return
    if ("-h" in args_x or "-help" in args_x or "-?" in args_x or "--h" in args_x or "--help" in args_x):
    	print """ Usage: ./xdspider.py [commands]
Commands                      Commands Description
--out filename                master output filename, will become filename_sha1-hash-of-url
--format format               master output format {JSON, CSV, XML}
--import filename             import configs from file (json only)
--export filename             export the default config to file (json only)
--no-save                     disables file output, prints output data to console
--debug                       enables application debugging mode
-h                            outputs help menu
--h                            outputs help menu
-?                            outputs help menu
-help                         outputs help menu
--help                         outputs help menu
"""
        return
    
    
    if "--debug" in args_x:
        debug = True
        print(args_x)
    else:
        debug = False

    #"--export"
    if "--export" in args_x:
        try:
            f = open(args_x[args_x.index("--export")+1],"w")
            json.dump(configs_,f,indent=4, sort_keys=False)
            f.close()
        except Exception as e:
            print(e)
        return

    #--import
    if "--import" in args_x:
        try:
            f = open(args_x[args_x.index("--import")+1],"r")
            configs_ = json.loads("".join(f.readlines()).replace("'", "\"").replace("/", "\\/"))
            f.close()
        except Exception as e:
            print(e)
            return

    #--format <XML | JSON | CSV>
    if "--format" in args_x:
        configs_["format"] = args_x[args_x.index("--format")+1]

    #--out filename
    if "--out" in args_x:
        configs_["output_file"] = args_x[args_x.index("--out")+1]
        configs_["save2file"] = 1

    #--no-save
    if "--no-save" in args_x:
        configs_["save2file"] = 0

    threads = []
    for i in range(len(configs_["websites"])):
        threads.append(XDSpider())
        threads[i].StartSpider(configs_["websites"][i])
        threads[i].start()
    return

if __name__ == "__main__":
    main()

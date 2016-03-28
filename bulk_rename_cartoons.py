#! /usr/bin/python3

#script to rename files downloaded from watch cartoon online into something more understandable.

from urllib import request, parse
from os import rename


#details of the HTTP request to find episodes.
#url of first episode, replace {} with episode number
baseUrl = "http://www.watchcartoononline.com/monster-episode-{}-english-dubbed"

ext = ".flv" #file extension of video

userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"

#start harvesting the episodes from:
firstEp = 1
#stop extracting episodes at episode number
lastEp = 74

#what to call the new filenames, {} is the episode number
#automatically suffixed with the extension 
new_file_name_template = "Monster-E{}"

#loop through all episodes from first to last
for episode in range(firstEp,lastEp+1):
#def findUrl(episode):
    
    epcode = "{0:02d}".format(episode)
 
    print("episode " + epcode + ":")
    
    requestUrl = baseUrl.replace("{}", str(episode))
    
    browser_headers = {"User-Agent": userAgent, "Referer": requestUrl}

    #step 0: find the i frame which has the url of the embdded thing
    req = request.Request(requestUrl, headers=browser_headers, method="GET")
    response = request.urlopen(req)
    
    data = response.read().decode("utf-8")
    #receive a html file with the i frame
    
    iframe_findstr = """<iframe id="frameAnimeuploads0" src="""
    
    
    start = data.find(iframe_findstr)
    start += len(iframe_findstr)
    start += 1 # for the \" at the end
    
    end = data.find(ext, start)
    end += len(ext)
    
    requestUrl = data[start:end]
    requestUrl = parse.unquote(requestUrl)
    
    
    file_name = requestUrl.split('/')[-1]
    new_file_name = new_file_name_template.replace("{}", epcode) + ext
       
    response.close()       
    
    print("rename: " + file_name + " to " + new_file_name)
    
    rename(file_name, new_file_name)

print("done!")


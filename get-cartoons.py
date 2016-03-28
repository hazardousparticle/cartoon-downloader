#! /usr/bin/python3

#script to search watch cartoon online and download all episodes from a show.

import urllib.request, urllib.parse
import sys
from HTTPDownloader import HTTPDownloader
from multiprocessing import Process

#=============================================================
#cusomizable parameters
max_threads = 5


#details of the HTTP request to find episodes.
#url of first episode, replace {} with episode number
baseUrl = "http://www.watchcartoononline.com/monster-episode-{}-english-dubbed"

ext = ".flv" #file extension of video

#this comes from what the web browser would request when streaming
requestBody = "fuck_you=&confirm=Click+Here+to+Watch+Free%21%21"

userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"

#string to match, indicating the stream URL from the HTTP response
startSearch = "back.jpg&#038;file="
endSearch = ext #end of the url we want to download (illegaly :p )

#start harvesting the episodes from:
firstEp = 1
#stop extracting episodes at episode number
lastEp =  74


#the stuff starts here...

#array of threads running the downloads
processes=[]
#lastEp = lastEp + 1

#loop through all episodes from first to last
#for episode in range(firstEp,lastEp):
def findUrl(episode):
 
    print("episode " + "{0:02d}".format(episode) + ":")
    
    requestUrl = baseUrl.replace("{}", str(episode))
    
    browser_headers = {"User-Agent": userAgent, "Referer": requestUrl}

    
    
    #step 0: find the i frame which has the url of the embdded thing
    req = urllib.request.Request(requestUrl, headers=browser_headers, method="GET")
    response = urllib.request.urlopen(req)
    
    data = response.read().decode("utf-8")
    #receive a html file with the i frame
    
    iframe_findstr = """<iframe id="frameAnimeuploads0" src="""
    
    
    start = data.find(iframe_findstr)
    start += len(iframe_findstr)
    start += 1 # for the \" at the end
    
    end = data.find(ext, start)
    end += len(ext)
    
    requestUrl = data[start:end] 
    
    response.close()
    
       
    
    
    #find stream in webpage with flash embedded
    #1. request a the URL to simulate clicking "click to watch free"
    #   post request
    
    browser_headers = {"User-Agent": userAgent, "Referer": requestUrl, "Content-Type": "application/"+ \
    "x-www-form-urlencoded", "Content-Length": str(len(requestBody))}
    
    req = urllib.request.Request(requestUrl, data = requestBody.encode(), headers=browser_headers, method="POST")
    response = urllib.request.urlopen(req)

    #read the stream for the network and convert to string
    data = response.read().decode("utf-8")
    #2. receive a html file with the flash plugin in the embded tag
    
    response.close()

    start = data.find(startSearch)
    #start position (in characters)
    #video URL starts at this offset
    
    start += len(startSearch)
    #add length of startSearch to start position.
    #URL starts after the instance of this string
       
    end = data.find(endSearch)
    end += len(endSearch)
    data = data[start:end]
    
    #url decode
    data = urllib.parse.unquote(data)
    #cant have spaces in urls, so only encode those.
    url = data.replace(" ", "%20")
    print("Download URL: " + url)
    
    del data
    
    #http download stuff
    #p = Process(target = HTTPDownloader.download_file, args=(url,) )
    #processes.append(p)
    return url
                
threads_count = int((lastEp - firstEp ) / max_threads) + 1

if threads_count <= 0:
    threads_count = (lastEp - firstEp)

print("Episodes: " + str(lastEp - firstEp))
print("Blocks: " + str(threads_count + 1) )
print(" of " + str(max_threads) + " to download")


for i in range(threads_count):
    #groups all threads into blocks of max_threads
    cur_thread_block = i * max_threads
    
    if (lastEp - cur_thread_block) < max_threads:
        max_threads = lastEp - cur_thread_block
        
    for i in range(max_threads):
        cur_thread = cur_thread_block + i
        
        #url = "aaa"
        
        url = findUrl(cur_thread + 1)
        
        #print(str(cur_thread + 1) + url)
        
        p = Process(target = HTTPDownloader.download_file, args=(url,) )
        processes.append(p)
                     
        processes[cur_thread].start()
        
    
    for i in range(max_threads):
        processes[cur_thread_block + i].join()
    



#    try:
#        #stuff
#        	   
#    #quit gracefully on ctrl c
#    except KeyboardInterrupt:
#        print("Aborted")
#        exit(0);
#    #errors in each file to download, skip and move to next
#    except Exception as detail:
#        pass
#        print("file " + epCode + " failed")
#        print(detail)
#        print("")

#del requestUrl
#del headers

print("done!")


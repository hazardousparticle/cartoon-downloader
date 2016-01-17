#! /usr/bin/python3

#script to search watch cartoon online and download all episodes from a show.

import urllib.request, urllib.parse
import sys

#=============================================================
#cusomizable parameters
#details of the HTTP request to find episodes.
baseUrl = "http://www.animeuploads.com/embed_jw51.php?file=Death%20Note/[RaX]-DthNte-"
ext = ".flv" #file extension of video
#this comes from what the web browser would request when streaming
requestBody = "fuck_you=&confirm=Click+Here+to+Watch+Free%21%21"

userAgent = "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:39.0)" + \
"Gecko/20100101 Firefox/39.0"

#string to match, indicating the stream URL form the HTTP response
startSearch = "back.jpg&#038;file="
endSearch = "DthNte-" # + episode number + .flv

#start harvesting the episodes from:
firstEp = 1
#stop extracting episodes at episode number (add 1, cause the loop stops at N - 1)
lastEp =  30

#block sise of file downloader default: 8192
block_sz = 8192

#loop through all episodes from first to last
for i in range(firstEp,lastEp):
    try:
        epCode = "{0:02d}".format(i)
        print("episode " + epCode + ":")
        requestUrl = baseUrl + epCode + ext
        browser_headers = {"User-Agent": userAgent, "Referer": requestUrl, "Content-Type": "application/"+ \
        "x-www-form-urlencoded", "Content-Length": str(len(requestBody))}
        
        #find stream in webpage with flash embedded
        #1. request a the URL to simulate clicking "click to watch free"
        #   post request
        
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
        
        endSearch1 = endSearch + epCode + ext
        #string to match to find end of URL in received data
        
        end = data.find(endSearch1)
        end += len(endSearch1)
        data = data[start:end]
        
        #url decode
        data = urllib.parse.unquote(data)
        #cant have spaces in urls, so only encode those.
        url = data.replace(" ", "%20")
        print("Download URL: " + url)
        
        del data
        
        #get file to download
        file_name = url.split('/')[-1]
        u = urllib.request.urlopen(url)
        f = open(file_name, 'wb')
        #request metadata
        meta = u.headers.get("Content-Length")
        file_size = int(meta)
        print("Downloading: %s, Bytes: %s" % (file_name, file_size))

        #DL the file in blocks and update the progress
        file_size_dl = 0
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            
            
            
            file_size_mb=(file_size_dl / (1024*1024))
            dl_progress=(file_size_dl * 100. / file_size)
            #printf("format", file_size_mb, dl_progress)
            status = "\r{a:4.2f} MiB [{b:3.2f}%]".format(a=file_size_mb, b=dl_progress)
            sys.stdout.write(status)

        u.close()
        f.close()
        print("")
        print("Downloaded: " + file_name)
    #quit gracefully on ctrl c
    except KeyboardInterrupt:
        print("Aborted")
        exit(0);
    #errors in each file to download, skip and move to next
    except Exception as detail:
        pass
        print("file " + epCode + " failed")
        print(detail)
        print("")

#del requestUrl
#del headers

print("done!")


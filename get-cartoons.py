#! /usr/bin/python

#script to search watch cartoon online and download all episodes from a show.

import httplib, urllib, urllib2

#details of the HTTP request to find episodes.
host = "www.animeuploads.com"
baseUrl = "http://www.animeuploads.com/embed_jw51.php?file=Death%20Note/[RaX]-DthNte-"
ext = ".flv" #file extension of video
requestBody = "fuck_you=&confirm=Click+Here+to+Watch+Free%21%21"

userAgent = "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:39.0)" + \
        "Gecko/20100101 Firefox/39.0"

#string to match, indicating the stream URL form the HTTP response
startSearch = "back.jpg&#038;file="
endSearch = "DthNte-" # + episode number + .flv

#start harvesting the episodes from:
firstEp = 1
#stop extracting episodes at episode number (add 1, casue the loop stop at N - 1)
lastEp =  10


#loop through all episodes from first to last
for i in range(firstEp,lastEp):
    try:
        print "death note ep " + str(i) + ":"
        requestUrl = baseUrl + str(i) + ext
        headers = {"User-Agent": userAgent, "Referer": requestUrl, "Content-Type": "application/"+ \
        "x-www-form-urlencoded", "Content-Length": "48"}
        
        conn = httplib.HTTPConnection(host)
        conn.request("POST", requestUrl, requestBody, headers)
        response = conn.getresponse()

        data = response.read()
        #print data
        
        conn.close()
        
        start = data.find(startSearch)
        #start position (in characters)
        #video URL starts at this offset
        
        start += len(startSearch)
        #add length of startSearch to start position.
        #URL starts after the instance of this string
        
        endSearch1 = endSearch + str(i) + ext
        #string to match to find end of URL in received data
        
        end = data.find(endSearch1)
        end += len(endSearch1)
        data = data[start:end]
        
        print "Found: " + data
        
        #url decode
        data = urllib.unquote(data).decode('utf8')
        
        url = data.replace(" ", "%20")
        print "DL URL: " + url
        
        #get file to download
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        #DL the file in blocks and update the progress
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()    
        print ""
    except Exception as detail:
        pass
        print "file " + str(i) + " failed"
        print detail 
        print ""

#del requestUrl
#del headers

print "done!"


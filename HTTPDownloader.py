import urllib
import threading
import sys

class HTTPDownloader:
    
    # the downloading thread
    @staticmethod
    def download_file(url):
        if len(url) == 0:
            return
        
        
        #block sise of file downloader default: 8192
        block_sz = 8192
    
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
            #dl_progress=(file_size_dl * 100. / file_size)
            #printf("format", file_size_mb, dl_progress)
            #status = "\r{a:4.2f} MiB [{b:3.2f}%]".format(a=file_size_mb, b=dl_progress)
            #sys.stdout.write(status)

        u.close()
        f.close()
        print("Downloaded: " + file_name + " ({a:4.2f} MiB ".format(a=file_size_mb) + " )")


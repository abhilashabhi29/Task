
import os
import requests, zipfile, StringIO

class Download():
    def csv_download(self,urls,path):
        for i  in urls:
            try:
                r = requests.get(i, stream=True,timeout=10)
                if r.status_code==200:
                    z = zipfile.ZipFile(StringIO.StringIO(r.content))

                    #save files to folder named "files"
                    z.extractall(os.path.join(path,'files'))
                print ("Data extracted from",i)

            except requests.exceptions.RequestException as e:
                print ("Data cannot be extracted from",i)

        return True

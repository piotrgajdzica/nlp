user="gienek@gmail.com"
# lpmn=r"""any2txt|wcrft2({"morfeusz2":false})|iobber|liner2({"model":"n82","output":"tei:gz"})"""
# lpmn=r"""any2txt|wcrft2({"morfeusz2":false})|iobber|liner2({"model":"n82","output":"tei:gz"})|spejd"""
lpmn=r"""any2txt|wcrft2|liner2({"model":"n82"})"""
# lpmn=r"""any2txt|wcrft2"""
import json
from urllib.request import urlopen, Request
import glob
import os
import time
url="http://ws.clarin-pl.eu/nlprest2/base" 

def upload(file):
        with open (file, "rb") as myfile:
            doc=myfile.read()
        return urlopen(Request(url+'/upload/',doc,{'Content-Type': 'binary/octet-stream'})).read().decode('utf-8')

def process(data):
        print(data)
        doc=json.dumps(data)

        taskid = urlopen(Request(url+'/startTask/',doc.encode('utf-8'),{'Content-Type': 'application/json'})).read().decode('utf-8')
        time.sleep(0.2)
        resp = urlopen(Request(url+'/getStatus/'+taskid))
        data=json.load(resp)
        while data["status"] == "QUEUE" or data["status"] == "PROCESSING" :
            print(data, taskid)
            time.sleep(10)
            resp = urlopen(Request(url+'/getStatus/'+taskid))
            data=json.load(resp)
        if data["status"]=="ERROR":
            print("Error "+data["value"])
            return None
        print(data.keys())
        return data["value"]


def process_single_file(input, output):

    in_path = input
    out_path= output
    global_time = time.time()
    file = in_path
    fileid=upload(file)
    print("Processing: "+file)
    data={'lpmn':lpmn,'user':user,'file':fileid}
    data=process(data)
    if data is None:
        return
    data=data[0]["fileID"]
    content = urlopen(Request(url+'/download'+data)).read().decode('utf-8')
    # print(content)
    with open (out_path+'.ccl', "w", encoding='utf-8') as outfile:
            outfile.write(content)
    return "GLOBAL %s seconds ---" % (time.time() - global_time)

def main():
    in_path = 'paczka/*'
    out_path= 'out/'
    process_single_file('paczka/2000_696.txt', 'out/2000_696.txt')
    # global_time = time.time()
    # for file in glob.glob(in_path):
    #     start_time = time.time()
    #     fileid=upload(file)
    #     print("Processing: "+file)
    #     data={'lpmn':lpmn,'user':user,'file':fileid}
    #     data=process(data)
    #     if data==None:
    #         continue
    #     data=data[0]["fileID"]
    #     content = urlopen(Request(url+'/download'+data)).read().decode('utf-8')
    #     # print(content)
    #     with open (out_path+os.path.basename(file)+'.ccl', "w", encoding='utf-8') as outfile:
    #             outfile.write(content)
    # print("GLOBAL %s seconds ---" % (time.time() - global_time))


if __name__ == '__main__':
    main()

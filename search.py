


import json
import requests
import re

def split():
    words=input('\n\nINPUT THE WORDS YOU WANT TO MAKE SEARCH\nINPUT "quit" for quit program\n')
    word_list=re.split(r'[-,/,\s]',words)
    word_list_1=[]
    for word in word_list:
        word=word.lower()
        word=re.sub(r'[^a-z0-9]','',word)
        word_list_1.append(word)
    return word_list_1

def list_desc(LIST):
  
    a = {}
    for i in LIST:
        if i in a:
            a[i] = a[i] + 1
        else:
            a[i] = 1
  
    b = sorted(a.items(),key=lambda item:item[1],reverse=True)
    c=[]
    for item in b:
        c.append(item[0])
    return c

def search(word):
    r=requests.get('https://world-d839b.firebaseio.com/index/'+word+'.json') 
    result=json.loads(r.text)
    word={}
    if result!=None:
        for dic in result:
            if dic.get("ID") is not None:
                if word.get("ID") is None:
                    word["ID"]=[dic["ID"]]
                else:
                    word["ID"].append(dic["ID"])
                word["ID"]=list_desc(word["ID"])


            if dic.get("Code") is not None:
                if word.get("Code") is None:
                    word["Code"]=[dic["Code"]]
                else:
                    word["Code"].append(dic["Code"])
                word["Code"]=list_desc(word["Code"])


            if dic.get("Language") is not None:
                if word.get("Language") is None:
                    word["Language"]=[dic["Language"]]
                else:
                    word["Language"].append(dic["Language"])
                word["Language"]=list_desc(word["Language"])


    return word
            
def diff(listA,listB):
    retA = [i for i in listA if i in listB]
    return retA
def union(a,b):
    c=[]
    for i in a:
        c.append(i)
    for i in b:
        if i not in diff(a,b):
            c.append(i)
    return c          

if __name__ == '__main__':
    while True:
        result={}
        word_list_1=split()
        if word_list_1==['quit']:
            break
        
        elif len(word_list_1)==2:
            for word in word_list_1:
                dic=search(word) 
                result[word]=dic
            result[word_list_1[0]+' '+word_list_1[1]]={}
        
            if result[word_list_1[0]].get("ID") !=None and result[word_list_1[1]].get("ID") !=None:
                if diff(result[word_list_1[0]]["ID"],result[word_list_1[1]]["ID"])!=[]:
                    d=diff(result[word_list_1[0]]["ID"],result[word_list_1[1]]["ID"])
                    result[word_list_1[0]]["ID"]=union(d,result[word_list_1[0]]["ID"])
                    result[word_list_1[1]]["ID"]=union(d,result[word_list_1[1]]["ID"])
                    result[word_list_1[0]+' '+word_list_1[1]]["ID"]=d



            if result[word_list_1[0]].get("Code") !=None and result[word_list_1[1]].get("Code") !=None:
                if diff(result[word_list_1[0]]["Code"],result[word_list_1[1]]["Code"])!=[]:
                    d=diff(result[word_list_1[0]]["Code"],result[word_list_1[1]]["Code"])
                    result[word_list_1[0]]["Code"]=union(d,result[word_list_1[0]]["Code"])
                    result[word_list_1[1]]["Code"]=union(d,result[word_list_1[1]]["Code"])
                    result[word_list_1[0]+' '+word_list_1[1]]["Code"]=d


            if result[word_list_1[0]].get("Language") !=None and result[word_list_1[1]].get("Language") !=None:
                if diff(result[word_list_1[0]]["Language"],result[word_list_1[1]]["Language"])!=[]:
                    d=diff(result[word_list_1[0]]["Language"],result[word_list_1[1]]["Language"])
                    result[word_list_1[0]]["Language"]=union(d,result[word_list_1[0]]["Language"])
                    result[word_list_1[1]]["Language"]=union(d,result[word_list_1[1]]["Language"])
                    result[word_list_1[0]+' '+word_list_1[1]]["Language"]=d
                
        
            
        else:    
            for word in word_list_1:
                dic=search(word) 
                result[word]=dic
        j_result=json.dumps(result,indent=4)
        print(j_result)








import csv
import json
import math
import requests
import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def transjson(jsonpath, csvpath):
    fw = open(jsonpath, 'w', encoding='latin-1')  
    fo = open(csvpath, 'r', newline='',encoding='latin-1')   

    ls = []

    for line in fo:
        line = line.replace("\n", "")  
        ls.append(line.split(","))
        

    j=0
    while j<len(ls[0]):
        ls[0][j]=ls[0][j].strip()
        j+=1
 
        
    
    for l in ls:
        
        i=0
        while i<len(l):
            l[i]=l[i].strip("'").strip(' ').strip("'")
            if l[i].isdigit():
                l[i]=int(l[i])
            elif is_number(l[i]):
                l[i]=float(l[i])
            elif '#' in l[i]:
                l[i]=l[i].replace('#','').strip()
            
            i+=1

        if len(l)>len(ls[0]):
            if l[0] in ['COD','FSM','VGB','VIR']:
                l[1]=l[1]+' '+l[2]
                del l[2]
            else:
                l[11]=l[11]+' '+l[12]
                del l[12]    
                


    for i in range(1, len(ls)):  
        ls[i] = dict(zip(ls[0], ls[i]))  
        
    
    json.dump(ls[1:], fw, sort_keys=True, indent=4)
    
    fo.close()
    fw.close()
    
 
    
  
def index():
    index_dict={}
    m_list=["$",",",".","[","]","#","(",")","\\","|",">","<"]
    
    with open("city.json", 'r') as f:
        j_city =json.loads(f.read())
    with open('country.json', 'r') as f:
        j_country = json.load(f)
    with open('countrylanguage.json', 'r') as f:
        j_countrylanguage = json.load(f)
        
        
    for dic in j_city:
        for x in dic.items():
            key=x[0]
            element=x[1]
            if type(element)==str:
                element=element.lower()
                for m in m_list:
                    if m in element:
                        element=element.replace(m,'')
                
                        
                if "-"or"/"or" " in element:
                    element=re.split(r'[-,/,\s]',element)
                    for e in element:
                        dic_e={'TABLE':'city','COLUMN':x[0],'ID':dic["ID"]}
                        if index_dict.get(e)==None:                                             
                            index_dict[e]=[dic_e]
                        else:
                            index_dict[e].append(dic_e)
                                                                    
                            
                else:
                    dic_e={'TABLE':'city','COLUMN':x[0],'ID':dic["ID"]}
                    if index_dict.get(element)==None:                                             
                        index_dict[element]=[dic_e]
                    else:
                        index_dict[element].append(dic_e)
                    
    for dic in j_country:
        for x in dic.items():
            key=x[0]
            element=x[1]
            if type(element)==str:
                element=element.lower()
                for m in m_list:
                    if m in element:
                        element=element.replace(m,'')
                
                        
                if "-"or"/"or" " in element:
                    element=re.split(r'[-,/,\s]',element)
                    for e in element:
                        dic_e={'TABLE':'country','COLUMN':x[0],'Code':dic["Code"]}
                        if index_dict.get(e)==None:                                             
                            index_dict[e]=[dic_e]
                        else:
                            index_dict[e].append(dic_e)
                                                                    
                            
                else:
                    dic_e={'TABLE':'country','COLUMN':x[0],'Code':dic["Code"]}
                    if index_dict.get(element)==None:                                             
                        index_dict[element]=[dic_e]
                    else:
                        index_dict[element].append(dic_e)
                    
    for dic in j_countrylanguage:
        for x in dic.items():
            key=x[0]
            element=x[1]
            if type(element)==str:
                element=element.lower()
                for m in m_list:
                    if m in element:
                        element=element.replace(m,'')
                
                        
                if "-"or"/"or" " in element:
                    element=re.split(r'[-,/,\s]',element)
                    for e in element:
                        dic_e={'TABLE':'countrylanguage','COLUMN':x[0],'Language':dic["Language"]}
                        if index_dict.get(e)==None:                                             
                            index_dict[e]=[dic_e]
                        else:
                            index_dict[e].append(dic_e)
                                                                    
                
                else:
                    dic_e={'TABLE':'countrylanguage','COLUMN':x[0],'Language':dic["Language"]}
                    if index_dict.get(element)==None:                                             
                        index_dict[element]=[dic_e]
                    else:
                        index_dict[element].append(dic_e)

    index_dict_1={}

    for x in index_dict.keys():
        x_1=re.sub(r'[^a-z0-9]','',x)
        
        if index_dict_1.get(x_1)==None:                                             
            index_dict_1[x_1]=index_dict[x]
        else:
            index_dict_1[x_1].extend(index_dict[x])
    del index_dict_1['']

    return index_dict_1
                        
                  



if __name__ == '__main__':
  
    j_city=transjson('./city.json', './city.csv')
    j_country=transjson('./country.json', './country.csv')
    j_countrylanguage=transjson('./countrylanguage.json', './countrylanguage.csv')
    

       
    with open("city.json", 'r') as f:
        j_city =json.loads(f.read())
        j_city =json.dumps(j_city)
    requests.put('https://world-d839b.firebaseio.com/'+'city.json',j_city)
    
    
    with open('country.json', 'r') as f:
        j_country = json.load(f)
        j_country =json.dumps(j_country)
    requests.put('https://world-d839b.firebaseio.com/'+'counrty.json',j_country)    
        
        
    
    with open('countrylanguage.json', 'r') as f:
        j_countrylanguage = json.load(f)
        j_countrylanguage =json.dumps(j_countrylanguage)
    requests.put('https://world-d839b.firebaseio.com/'+'counrtylanguage.json',j_countrylanguage)   
    
    index_dict_1=index()
    js = json.dumps(index_dict_1, indent=4, separators=(',', ':'))
    requests.put('https://world-d839b.firebaseio.com/'+'index.json',js)


    

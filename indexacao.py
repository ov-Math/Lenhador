#!/usr/bin/env python
# -*- coding: utf-8 -*-

from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.analysis import StandardAnalyzer
from whoosh.index import create_in, open_dir
import os

stopwords = ["de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas", "este", "fosse", "dele", "tu", "e", "vocês", "vos", "lhes", "meus", "minhas", "eu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", "hajam", "houvesse", "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei",  "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos", "teriam"]

schema = Schema(bookname=TEXT(stored=True), category=TEXT(stored=True), year=NUMERIC(stored=True), content=TEXT(analyzer=StandardAnalyzer(stoplist=stopwords)), url=ID(stored=True))

if not os.path.exists("whoosh_index"):
    os.mkdir("whoosh_index")
ix = create_in("whoosh_index", schema)
ix.close()

try:
    ix = open_dir("whoosh_index")
    writer = ix.writer()
    for dirname in os.listdir(os.getcwd()+"/Obras"):
        path = os.getcwd()+"/Obras/"+dirname
        for filename in os.listdir(path):
            print(filename)
            file = open(path+"/"+filename , 'r', encoding="cp1252")
            line = file.readline()
            result = line.split(",")
            cat = result[0]
            ano = result[-1]
            if "-" in ano:
                ano = ano.split("-")[0]
            name = ""
            for i in range(1,len(result)-1):
                if i == 1:                
                    name += result[i]    
                else:
                    name += "," + result[i]
            print(cat, name, ano)
            writer.add_document(bookname=name, category=cat, year=ano, content=file.read(), url="http://machado.mec.gov.br/images/stories/pdf/"+dirname+"/"+filename.split(".")[0]+".pdf")
    writer.commit()
finally:
    ix.close()

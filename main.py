from flask import Flask, jsonify, render_template, request

from datetime import datetime
import pickle
import sys
import ctg_interface
from ctg_interface import searchCTG, aggregateOutcomes
from lda_clustering import generateLDAvis

import testingGround

app = Flask('app')

outraw_nct = ""

@app.route('/flaskTest')
def hello_world():
  return render_template("index.html", message="Hello Flask!");

  #return 'Hello, World!!'
  
  
@app.route('/tst')
def test():
  return jsonify(testingGround.runTests())
  
  
  
@app.route("/table")
def table():
  return render_template("sortableTableOriginal.html")
  
  
@app.route("/table2")
def table2():
  return render_template("table2.html")


@app.route("/")
def table2temp():
  return render_template("table2_template.html")



@app.route("/<searchType>/<query>")
def showOutcomes(searchType, query):
  
  updateCache(searchType, query,
  request.user_agent.string)
  
  df = searchCTG(searchType, query)
  global outraw_nct
  outraw_nct, out_nct, out_links, nct_title, nct_1stposted = aggregateOutcomes(df)
  
  meta = {'query': query.upper(), 'searchType': searchType.upper(),
    'count':len(nct_title)}
  
  return render_template("resTable.html", out_nct = out_nct, out_links=out_links, header = [("Outcome", 40), ( "Number of Trials", 15), ("Trials Using This Outcome", 45)], meta=meta)
  
  
@app.route("/clusterNgram")
def clusterOutcomes():
  
  return render_template("cluster.html")
  
  
  
@app.route("/clusterLDA")
def ldaOutcomes():
  if outraw_nct == "":
    return jsonify("Error. Outcomes do not appear to have been extracted and aggregated yet!")
  else:
    outraw_sorted = sorted(outraw_nct.keys(), key=lambda x: len(outraw_nct[x]), reverse=True)
    
    outcomes = outraw_sorted[:2000]
    generateLDAvis(outcomes, 10)
    return render_template("lda_vis.html")
    #return jsonify(list(outraw_nct.keys()))
  
@app.route("/initCache")
def initCache():
  cache = {datetime.now(): "<initialized>"}
  pickle.dump(cache, open("cache.p", "wb"))
  return jsonify("Cache initialized. Contents: " + str(cache))
  

@app.route("/displayCache")
def displayCache():
  cache = pickle.load(open("cache.p", "rb"))
  
  cachesorted = sorted(cache.items(), key= lambda x: x[0], reverse=True)
  #return jsonify("Cache Contents: " + str(cache))
  return render_template("cacheTable.html", header=[("Timestamp", 30), ("SearchType", 10), ("Query", 30), ("User-Agent", 30)], 
  cache=cachesorted)
  
  
  
  
def initLogs():
  log = open("static/progressLog.txt", "w", buffering=1)
  err = open("static/errorLog.txt", "w", buffering=1)
  sys.stdout = log
  sys.stderr = err
  
def updateCache(searchType, query, useragent):
  cache = pickle.load(open("cache.p", "rb"))
  cache[datetime.now()] = (searchType, query, useragent)
  pickle.dump(cache, open("cache.p", "wb"))
  
@app.route("/stopwords")
def getStopWords():
  return jsonify(ctg_interface.readStopWords())
  

initLogs() 
app.run(host='0.0.0.0', port=8080)
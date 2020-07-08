import pandas
from datetime import datetime
from urllib import request, parse
from io import StringIO
from collections import defaultdict
import string
import re


def searchCTG(searchType, rawquery):
    if searchType not in ["cond", "term"]:
      raise ValueError("Search type must be 'cond' or 'term'")
      
    query = parse.quote(rawquery)
    print("input query: ", rawquery, " -- query after parsing: ", query)
    print(f"searchCTG has been called - Search type: {searchType} - Query: {query}")
    t0 = datetime.now()
    dfs = []
    chunk_num = 1
    while True:
        try:
            p = request.urlopen(f"https://clinicaltrials.gov/ct2/results/download_fields?{searchType}={query}&down_flds=all&down_count=10000&down_fmt=csv&down_chunk={chunk_num}")
        except Exception as e:
            print("Exception: ", e)
            break
        data = StringIO(p.read().decode())
        print(data)
        df = pandas.read_csv(data)
        dfs.append(df)
        chunk_num += 1
    
    t1 = datetime.now()
    df = pandas.concat(dfs)
    
    print(f"{searchType} search for query: \"", rawquery, "\" yielded ", len(df), " results in ", t1-t0, " seconds.")
    return df
    
    
    
#TO DO: EXAPAND, maybe?
def normalize_outcome(o):
  #on = o.translate(str.maketrans(" ", " ", string.punctuation)) 
  on = o.replace("'s", " ")
  on = re.sub(r'\(.*\)', " ", on)
  print("on now: ", on)
  #on = on.translate(str.maketrans(" ", " ", string.punctuation))
  on = on.translate(str.maketrans({c:" " for c in string.punctuation}))
  print("and now: ", on)
  on = " ".join([word.lower().strip() for word in on.split(" ") if word != ""])
  return on
  
def getBestOriginal(normo, d):
  return sorted(d[normo].items(), key=lambda x: x[1], reverse=True)[0][0]
  
  
def getNCTlink(nctnum):
  nctnum = nctnum.replace("'", "")
  return '<a href="https://clinicaltrials.gov/ct2/show/' + nctnum+ '" target="_blank">' + nctnum + "</a>"
  
  
def aggregateOutcomes(df):
  print("aggregateOutcomes function has been called!")
  outraw_nct = defaultdict(lambda: set())
  out_nct = defaultdict(lambda: set())
  outs_orig = defaultdict(lambda: defaultdict(lambda:0))
  nct_title, nct_1stposted = dict(), dict()
  for _, row in df.iterrows():
    if pandas.isnull(row["Outcome Measures"]):
      continue
    outs = row["Outcome Measures"].split("|")
    for o in outs:
      normo = normalize_outcome(o)
      outraw_nct[o].add(row['NCT Number'])
      out_nct[normo].add(row['NCT Number'])
      outs_orig[normo][o] += 1
    nct_title[row['NCT Number']] = row['Title']
    nct_1stposted = row['NCT Number'] = row['First Posted']
    
  print("Number of outcomes after normalization: ", len(out_nct))
  out_nct_sorted = sorted([(k, list(v)) for (k,v) in out_nct.items()], key=lambda x: len(x[1]), reverse=True)
  
  out_nct_sorted_links = [(getBestOriginal(k,outs_orig),[getNCTlink(n) for n in v ]) for (k,v) in out_nct_sorted]
  
  return outraw_nct, out_nct_sorted, out_nct_sorted_links, nct_title, nct_1stposted
  
  
def readStopWords():
  with open("stop_words.txt") as f:
    raw = f.read()
    stop_words = [l.strip().lower() for l in raw.split("\n")]
    stop_words = [_ for _ in stop_words if _ != "" ]
  
  return stop_words
  
  
def getNGrams():
  return []
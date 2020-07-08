import ctg_interface



def runTests():
  print("Testing method has been called!")
  
  
  #df = ctg_interface.searchCTG( "cond", "covid")
  
 # print(type(df))
 # print("header of dataframe: ",
  # df.columns)
  #print(df.head())
  
  #return("This is the testing ground. Hello world")
  #out_nct, _, _ = ctg_interface.aggregateOutcomes(df)
  
  #print(type(out_nct))
  #print(out_nct[0])
  x= "transplant-related mortality."
  print(x)
  return(ctg_interface.normalize_outcome(x))
  #return out_nct
  

if __name__ == '__main__':
  runTests()
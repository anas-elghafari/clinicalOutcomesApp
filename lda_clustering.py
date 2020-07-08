import pyLDAvis
from pyLDAvis import sklearn as sklearn_lda

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.decomposition import LatentDirichletAllocation as LDA


def generateLDAvis(outcomes, num_topics):
  #outcomes = [x.upper() for x in outcomes]
  
  vecType = TfidfVectorizer
  #vecs = vecType(stop_words='english', ngram_range=(2,4), lowercase=True, max_df=0.2, min_df=0.02)
  
  vecs = vecType(stop_words= 'english', ngram_range=(2,2), lowercase=True, max_df=0.2, min_df=0.01)
  
  # Fit and transform the processed titles
  count_data = vecs.fit_transform(outcomes)
  lda = LDA(n_components=num_topics, n_jobs=10)
  lda.fit(count_data)
  LDAvis_prepared = sklearn_lda.prepare(lda, count_data, vecs)
  pyLDAvis.save_html(LDAvis_prepared, "templates/lda_vis.html")
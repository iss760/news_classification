# news_classification

## explanation

* news category classification model through natural language processing in TF-IDF method.
* only Korean news is supported.
* news data are based on Naver news.

##### directory
* news_data : data directory for classification. \
(reference data for each category)
* preprocessing_data : stopword handling files and build files.

##### files
* data_loader.py : get news data through the API and elasticsearch module two ways.
* news_classification.py : categorize the categories of documents you want to classify.
* news_crawler.py : get Naver news.
* test_file.py :  you can try this project from this file.
* tokenizer.py : preprocesses and tokenizes words, documents and sets of documents.

## instructions
1. You must have a key to get news data via data_loder.py.\
(If you need token_key, please contact my email. Actually, I recommend you to get news by news_crawler.py.)
2. You need to generate a ranking_token, standard_tdm and standard_tf_idf in news_data directory.\
 (If you think it is unnecessary, you can use the existing ranking token, TDM and TF-IDF. Ranking tokens are created with ranking_token_bulild.py. TDM and TF-IDF are created with tf_idf_build.py.)
3. You can see the category of the news by activating the classifier function of the news classification class in news_classification.py.
4. 
<pre><code>from news_classification import News_Classificaion
nc = News_Classificaion()
nc.classifier('news_data') 
</code></pre>
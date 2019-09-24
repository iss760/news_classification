# news_classification

* news category classification model through natural language processing in TF-IDF method.
* only Korean news is supported.
* news data are based on Naver news.

[directory]
* news_data : data directory for classification. \
(reference data for each category)
* preprocessing_data : stopword handling files and build files.

[files]
* data_loader.py : get news data through the API and elasticsearch module two ways.
* news_classification.py : categorize the categories of documents you want to classify.
* news_crawler.py : get Naver news.
* test_file.py :  you can try this project from this file.
* tokenizer.py : preprocesses and tokenizes words, documents and sets of documents.
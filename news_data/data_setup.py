import json
import math
from collections import OrderedDict
from nltk import FreqDist
from tokenizer import KrTokenizer


# 표준 DTM, TF-IDF 생성 함수
def create_standard_tf_idf(rank_count=100):
    """
    :param rank_count: (int) DTM 생성을 위한 카테고리 별 랭킹 토큰의 갯수, default=100
    """
    category_list = [100, 101, 102, 103, 104, 105]
    category_count = len(category_list)

    # 데이터 로드
    load_file = []
    for category in category_list:
        with open('./news_data/ranking_token_' + str(category) + '.json', 'r', encoding='UTF-8') as f:
            load_file.append(json.load(f))

    # 토큰 추출, 토큰 리스트 생성
    token_list = []
    for _load_file in load_file:
        for j in range(len(_load_file['token'])):
            token_list.append(_load_file['token'][j][0])

    # Distinct 토큰 리스토로 변환
    unique_token_list = list(set(token_list))
    # Distinct 토큰 리스토 크기
    size = len(unique_token_list)

    # DTM 배열 생성
    dtm_matrix = [[0 for _ in range(size)] for _ in range(category_count)]
    for i, token in enumerate(unique_token_list):
        for j in range(category_count):
            for k in range(rank_count):
                if token == load_file[j]['token'][k][0]:
                    dtm_matrix[j][i] = load_file[j]['token'][k][1]

    # DTM 저장
    save_data = OrderedDict()
    save_data['token'] = unique_token_list
    save_data['dtm'] = dtm_matrix
    json.dump(save_data, open('./news_data/standard_dtm.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent='\t')

    # TF-IDF 생성
    tf_idf_matrix = dtm_to_tf_idf(dtm_matrix,)

    # TF-IDF 저장
    save_data2 = OrderedDict()
    save_data2['token'] = unique_token_list
    save_data2['tf_idf'] = tf_idf_matrix
    json.dump(save_data2, open('./news_data/standard_tf_idf.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent='\t')

# DTM 을 TF-IDF 로 변환 하는 함수
def dtm_to_tf_idf(dtm_matrix):
    """
    :param dtm_matrix: (list) DTM 리스트
    :return: (list) TF-IDF로 변환 된 리스트
    """
    col_size = len(dtm_matrix[0])
    row_size = len(dtm_matrix)
    tf_idf_matrix = [[0 for _ in range(col_size)] for _ in range(row_size)]
    for i in range(row_size):
        for j in range(col_size):
            tf_idf_matrix[i][j] = math.log(row_size / (dtm_matrix[i][j] + 1)) * dtm_matrix[i][j]

    return tf_idf_matrix

# 복수개의 뉴스 본문들을 통해 랭킹 토큰 json 생성 함수
def ranking_token_build(category, doc_ls):
    krt = KrTokenizer()

    news_body_contents_list = doc_ls

    # 토그나이징, 전처리
    tokenized_news_list = krt.extract_morphs_for_all_document(news_body_contents_list)
    for i in tokenized_news_list:
        print(i)

    # 토크나이징 하나로 통합
    combined_news_token = []
    for tokenized_news in tokenized_news_list:
        combined_news_token = combined_news_token + tokenized_news

    fdist = FreqDist(combined_news_token)
    temp_list = fdist.most_common(100)

    save_data = OrderedDict()
    save_data['token'] = temp_list
    save_data['category'] = category

    json.dump(save_data, open('./ranking_token_' + str(category) + 'json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent='\t')

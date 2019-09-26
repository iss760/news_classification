import json
import math
import pandas as pd

from numpy.linalg import norm
from numpy import dot
from nltk import FreqDist

from tokenizer import KrTokenizer


class News_Classificaion():
    def __init__(self):
        self.p_category_list = {
            100: '정치',
            101: '경제',
            102: '사회',
            103: '생활/문화',
            104: '세계',
            105: 'IT/과학',
            106: 'UNK'
        }
        self.category_list = [100, 101, 102, 103, 104, 105]
        self.category_count = len(self.category_list)

    # 데이터 구조화 함수
    def to_dataFrame(self, index_list, value_list):
        """
        :param index_list: (list) 열 인덱스
        :param value_list: (list) 각 행 값들
        :return: (dataFrame)구조화 한 데이터
        """
        data = {}
        for i in range(len(index_list)):
            temp = []
            for j in range(len(value_list)):
                temp.append(value_list[j][i])
            data[index_list[i]] = temp
        result = pd.DataFrame(data, index=['정치', '경제', '사회', '생활', '세계', 'IT'])

        return result

    # 코사인 유사도 측정 함수
    def cos_sim(self, doc1, doc2):
        """
        :param doc1: (list) TF-IDF 처리 된 문서
        :param doc2: (list) TF-IDF 처리 된 문서
        :return: (float) 두 문서의 코사인 유사도
        """
        return dot(doc1, doc2) / (norm(doc1) * norm(doc2))

    # DTM 을 TF-IDF 로 변환 하는 함수
    def dtm_to_tf_idf(self, dtm_matrix):
        """
        :param dtm_matrix: (list) DTM 리스트
        :return: (list) TF-IDF로 변환 된 리스트
        """
        col_size = len(dtm_matrix)
        row_size = 1

        tf_idf_matrix = [0 for _ in range(col_size)]
        for i in range(col_size):
            tf_idf_matrix[i] = math.log(row_size/(dtm_matrix[i] + 1)) * dtm_matrix[i]

        return tf_idf_matrix

    # 하나의 문서를 BOW(Bag of Word) 형태의 리스트로 변한 하는 함수
    def to_bow(self, token_list, rank_count=100):
        """
        :param token_list: (list) 토크나이징 된 문서
        :param rank_count: (int) DTM 생성을 위한 카테고리 별 랭킹 토큰의 갯수, default=100
        :return: (list) 표준에 맞게 BOW 형식으로 변환 된 리스트
        """
        with open('./news_data/standard_tf_idf.json', 'r', encoding='UTF-8') as f:
            load_file = json.load(f)
        standard_token_list = load_file['token']
        size = len(load_file['token'])

        fdist = FreqDist(token_list)
        temp_list = fdist.most_common(rank_count)

        bow_list = [0 for _ in range(size)]
        for i, st_token in enumerate(standard_token_list):
            for token in temp_list:
                if st_token == token[0]:
                    bow_list[i] = token[1]

        return bow_list

    # 토크나이징 된 문서를 TF-IDF 로 변환
    def to_tf_idf(self, token_list):
        bow = self.to_bow(token_list)
        return self.dtm_to_tf_idf(bow)

    def classifier(self, doc):
        krt = KrTokenizer()

        # 문서 토크나이징
        tokenized_doc = krt.extract_morphs_for_single_doc(doc)
        data = self.to_tf_idf(tokenized_doc)

        with open('./news_data/standard_tf_idf.json', 'r', encoding='UTF-8') as f:
            load_file = json.load(f)
        standard_tf_idf_value = load_file['tf_idf']

        temp = []
        for i in range(6):
            temp.append(round(self.cos_sim(standard_tf_idf_value[i], data) * 100, 2))

        temp_sorted = sorted(temp)
        temp_sorted.sort(reverse=True)
        first_category = self.p_category_list[int(temp.index(temp_sorted[0])) + 100]
        second_category = self.p_category_list[int(temp.index(temp_sorted[1])) + 100]
        print('1st : ' + str(first_category) + ' (' + str(temp_sorted[0]) + '%)')
        print('2nd : ' + str(second_category) + ' (' + str(temp_sorted[1]) + '%)')

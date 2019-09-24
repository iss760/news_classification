import datetime
import requests
import json
from datetime import timedelta
from elasticsearch import Elasticsearch


# 엘라스틱 서치 모듈을 통한 데이터 로드
class Data_Load_ES():
    def __init__(self):
        self.es = Elasticsearch('http://211.180.114.181:5000')

    def data_load(self, _start_day, _end_day, origin_nm_list):
        """
        :param _start_day: 검색 시작 날짜
        :param _end_day:  검색 끝 날짜
        :param origin_nm_list: 검색 매체명 리스트
        :return: None
        """
        es = self.es
        es.info()

        # 검색 시작 날짜
        start_day = datetime.datetime.strptime(_start_day, '%Y-%m-%d').date()
        # 검색 끝 날짜
        end_day = datetime.datetime.strptime(_end_day, '%Y-%m-%d').date()
        day = start_day

        # 날짜 순환
        result = {}
        while True:
            # 매체 별 순환
            news_count = {}
            for origin_nm in origin_nm_list:
                req = es.search(index='news', body={"size": 50,
                                                    "from": 0,
                                                    "query": {
                                                        "bool": {
                                                            "must": [
                                                                {"term": {"type.keyword": "news"}},
                                                                {"term": {"language": "ko"}},
                                                                {"term": {"origin_nm": origin_nm}}
                                                                ],
                                                            "filter": {
                                                                "range": {
                                                                    "reg_date": {
                                                                        "gte": str(day),
                                                                        "lte": str(day + timedelta(1)),
                                                                        "format": "yyyy-MM-dd"
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    })
                body_ls = []
                cat_ls = []
                source_ls = []
                token_ls = []
                date_ls = []

                # 파싱
                for idx in range(len(req['hits']['hits'])):
                    body_ls.append(req['hits']['hits'][idx]['_source']['body'])
                    cat_ls.append(req['hits']['hits'][idx]['_source']['category'])
                    source_ls.append(req['hits']['hits'][idx]['_source']['origin_nm'])

                    # 토큰 데이터 로드에 오류 존재함
                    try:
                        token_ls.append(req['hits']['hits'][idx]['_source']['tokenizing'])
                    except  Exception as e:
                        token_ls.append('')

                    try:
                        temp = req['hits']['hits'][idx]['_source']['reg_date']
                        date = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S')
                        date = datetime.date(date.year, date.month, date.day)
                        date_ls.append(date)
                    except Exception as e:
                        date_ls.append('')

                try:
                    news_count[source_ls[0]] = len(body_ls)
                except Exception as e:
                    pass

                # 데이터 확인
                for i in range(len(body_ls)):
                    #print(cat_ls[i])
                    #print(body_ls[i])
                    print('(' + source_ls[i] + ') ' + token_ls[i])

            result[str(day)] = news_count

            # 날짜 하루 전으로
            day = day - timedelta(1)
            # 검색 끝 날짜 도달시 종료
            if day == end_day:
                break

        print('\n')
        print(result)

        return


# API를 통한 데이터 로드
class Data_Load_API():
    def __init__(self):
        # 매체명 리스트
        self.url = 'http://211.180.114.181/newsapi/data'
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}

    def data_load(self, _start_day, _end_day, origin_nm_list):
        """
        :param _start_day: 검색 시작 날짜
        :param _end_day: 검색 끝 날짜
        :param origin_nm_list: 검색 매체명 리스트
        :return: None
        """
        url = self.url
        headers = self.headers

        # 검색 시작 날짜
        start_day = datetime.datetime.strptime(_start_day, '%Y-%m-%d').date()
        # 검색 끝 날짜
        end_day = datetime.datetime.strptime(_end_day, '%Y-%m-%d').date()
        day = start_day

        # 날짜 별 순환
        result = {}
        body_ls =[]
        url_ls = []
        while True:
            # 매체 별 순환
            news_count = {}
            for origin_nm in origin_nm_list:
                # 토큰 키 로드 (API 이용 토큰 무단 배포금지)
                with open('./token_key.json', 'r', encoding='UTF-8') as f:
                    token_file = json.load(f)
                token_key = token_file['token']

                params = {
                    'token': token_key,
                    'pageNumber': 0,
                    'size': 30,
                    'search': [
                        {'key': 'body', 'value': []},
                        {'key': 'language', 'value': ['ko']},
                        {'key': 'origin_nm', 'value': [origin_nm]}
                    ],
                    'order': {},
                    'filter': {'from': str(day),
                               'to': str(day + timedelta(1))}
                }

                response = requests.post(url, data=json.dumps(params), headers=headers, timeout=100)
                load_data = json.loads(response.text)

                # 데이터 확인
                for data in load_data['message']['data']:
                    # print(data['origin_url'])
                    # print('(' + data['origin_nm'] + ', ' + data['reg_date'] + ') ' + data['body'])
                    body_ls.append(data['body'])
                    url_ls.append(data['origin_url'])
                try:
                    news_count[origin_nm] = len(load_data['message']['data'])
                except Exception as e:
                    pass

            result[str(day)] = news_count

            # 날짜 하루 전으로
            day = day - timedelta(1)
            # 검색 끝 날짜 도달시 종료
            if day == end_day:
                break

        print('\n')
        print(result)
        print('\n')

        return body_ls, url_ls


if __name__ == '__main__':
    dl_api = Data_Load_API()

    start_day = '2019-09-19'
    end_day = '2019-09-16'
    origin_nm_list = [  # '연합뉴스',
                        # '프레시안',
                        # '뉴시스',
                        # '국민일보',
                        # '미디어오늘',
                        # '머니투데이',
                        # '매일경제',
                         '서울경제',
                         '파이낸셜뉴스',
                        # '한국경제',
                        # '헤럴드경제',
                        # '이데일리',
                        # '동아일보',
                        # '문화일보',
                        # '세계일보',
                        # '조선일보',
                        # '중앙일보',
                        # '한겨례'
                      ]

    body_ls, url_ls = dl_api.data_load(start_day, end_day, origin_nm_list)

    for _body_ls, _url_ls in zip(body_ls, url_ls):
        print(_body_ls)
        print(_url_ls)

from data_loader import Data_Load_API
from news_classification import News_Classificaion


dl_api = Data_Load_API()
nc = News_Classificaion()


start_day = '2019-09-24'
end_day = '2019-09-23'
origin_nm_list = [  # '연합뉴스',
                    # '프레시안',
                    # '뉴시스',
                     '국민일보',
                    # '미디어오늘',
                    # '머니투데이',
                    # '매일경제',
                    # '서울경제',
                    # '파이낸셜뉴스',
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

for url, body in zip(url_ls, body_ls):
    print(url)
    nc.classifier(body)

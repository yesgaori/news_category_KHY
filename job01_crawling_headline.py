from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
import os

# 1. 카테고리 설정 (네이버 섹션 번호와 매칭)
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
df_titles = pd.DataFrame()

# User-Agent 설정 (차단 방지)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

# 저장 폴더 생성 (폴더가 없으면 에러 발생함)
os.makedirs('./crawling_data', exist_ok=True)

for i in range(6):
    url = "https://news.naver.com/section/10{}".format(i)
    resp = requests.get(url, headers=headers)  # headers 추가
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 클래스 선택자 확인 (네이버 개편에 따라 변경될 수 있음)
    title_tags = soup.select('.sa_text_strong')

    titles = [tag.text.strip() for tag in title_tags]  # 공백 제거 포함

    # 섹션별 데이터프레임 생성
    df_section_titles = pd.DataFrame(titles, columns=['title'])
    df_section_titles['category'] = category[i]

    # *** 수정 포인트: 생성한 df_section_titles를 병합해야 함 ***
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)

    print(f"{category[i]} 카테고리 수집 완료: {len(titles)}건")

# 결과 확인
print("\n--- 데이터 요약 ---")
print(df_titles.head())
print(df_titles.info())
print(df_titles['category'].value_counts())

# 파일 저장
file_name = './crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d'))
df_titles.to_csv(file_name, index=False, encoding='utf-8-sig')  # 인덱스 제외 및 한글 깨짐 방지
print(f"\n파일 저장 성공: {file_name}")
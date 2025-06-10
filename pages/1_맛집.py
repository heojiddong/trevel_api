import streamlit as st
import requests
import re

st.title("🍜 여행지 맛집 추천")

# 여행지 확인
location = st.session_state.get("location")
if not location:
    st.warning("여행지를 먼저 입력해 주세요 (메인 페이지에서)")
    st.stop()

# Kakao API 함수
def search_places(query):
    headers = {
        "Authorization": f"KakaoAK {st.secrets['KAKAO_API_KEY']}"
    }
    params = {"query": query, "size": 10}
    res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params=params)
    return res.json().get("documents", [])

# 네이버 블로그 검색 함수 + 키워드 요약
def get_food_and_features(query):
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"]
    }
    params = {
        "query": query,
        "display": 1,
        "sort": "sim"
    }
    res = requests.get("https://openapi.naver.com/v1/search/blog.json", headers=headers, params=params)
    items = res.json().get("items", [])
    if not items:
        return None, None

    desc = items[0]["description"]
    clean = re.sub(r"<.*?>", "", desc)

    # 음식 키워드 후보 (원하면 추가 가능)
    food_keywords = ["돈가스", "초밥", "라면", "회", "국밥", "떡볶이", "마라탕", "스시", "우동", "족발", "냉면", "해산물", "파스타", "스테이크", "한식", "양식", "중식", "분식", "뷔페", "정식"]
    feature_keywords = ["가성비", "뷰", "친절", "인테리어", "혼밥", "데이트", "줄", "대기", "예약", "깔끔", "조용", "감성", "푸짐", "분위기", "웨이팅"]

    found_foods = [k for k in food_keywords if k in clean]
    found_features = [k for k in feature_keywords if k in clean]

    return found_foods, found_features

# 장소 검색 실행
query = f"{location} 맛집"
results = search_places(query)

# 결과 출력
if results:
    for place in results:
        name = place['place_name']
        address = place['road_address_name'] or place['address_name']
        map_url = place['place_url']

        st.markdown(f"### 📍 {name}")
        st.write(f"📌 주소: {address}")
        st.markdown(f"🔗 [카카오맵 보기]({map_url})")

        # 네이버 블로그에서 요약 키워드 추출
        food, feature = get_food_and_features(f"{location} {name}")
        if food:
            st.write("🍽️ 대표 음식:", ", ".join(food))
        if feature:
            st.write("💬 특징:", ", ".join(feature))
        if not food and not feature:
            st.write("ℹ️ 블로그 후기를 찾을 수 없습니다.")

        st.markdown("---")
else:
    st.info("검색 결과가 없습니다.")

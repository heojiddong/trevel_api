import streamlit as st
import requests
import re

st.title("🍜 여행지 맛집 추천")

# 여행지 확인
location = st.session_state.get("location")
if not location:
    st.warning("❗ 먼저 메인 화면에서 여행지를 입력해 주세요.")
    st.info("📝 메인 페이지에서 '부산', '제주도' 등 여행지를 입력한 뒤 이 페이지를 다시 열어보세요.")
    st.stop()

# Kakao API 함수
def search_places(query):
    headers = {
        "Authorization": f"KakaoAK {st.secrets['KAKAO_API_KEY']}"
    }
    params = {"query": query, "size": 10}
    res = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params=params)
    return res.json().get("documents", [])

# 특징 키워드 → 자연어 문장 매핑 (※ '맛집' 제외됨)
feature_descriptions = {
    "가성비": "가성비가 좋다는 평이 많습니다.",
    "뷰": "전망이 좋은 곳으로 알려져 있습니다.",
    "친절": "직원들이 친절하다는 후기가 있습니다.",
    "인테리어": "인테리어가 세련되었다는 평이 많습니다.",
    "혼밥": "혼밥하기 편안한 분위기입니다.",
    "데이트": "데이트 장소로도 잘 어울린다는 평이 있습니다.",
    "줄": "줄을 서야 할 수도 있으니 참고하세요.",
    "대기": "대기 시간이 있을 수 있습니다.",
    "예약": "예약이 필요한 식당입니다.",
    "깔끔": "깔끔하고 정돈된 환경이 특징입니다.",
    "조용": "조용하고 아늑한 분위기입니다.",
    "감성": "감성적인 분위기로 꾸며져 있습니다.",
    "푸짐": "양이 푸짐하다는 후기가 많습니다.",
    "분위기": "분위기가 좋다는 평이 있습니다.",
    "웨이팅": "웨이팅이 길 수 있으니 참고하세요.",
    "서비스": "서비스가 좋다는 평가가 있습니다.",
    "청결": "매장이 청결하게 유지되고 있습니다."
}

# 네이버 블로그 검색 함수 + 키워드 추출
def get_food_and_features(query):
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"]
    }
    params = {
        "query": query,
        "display": 3,
        "sort": "sim"
    }
    res = requests.get("https://openapi.naver.com/v1/search/blog.json", headers=headers, params=params)
    items = res.json().get("items", [])
    if not items:
        return None, None

    combined_text = ""
    for item in items:
        title = re.sub(r"<.*?>", "", item.get("title", ""))
        desc = re.sub(r"<.*?>", "", item.get("description", ""))
        combined_text += f"{title} {desc} "

    food_keywords = [
        "돈가스", "초밥", "라면", "회", "국밥", "떡볶이", "마라탕", "스시", "우동", "족발",
        "냉면", "해산물", "파스타", "스테이크", "한식", "양식", "중식", "분식", "뷔페", "정식"
    ]
    feature_keywords = list(feature_descriptions.keys()) + ["맛집"]

    found_foods = sorted(set([k for k in food_keywords if k in combined_text]))
    found_features = sorted(set([k for k in feature_keywords if k in combined_text]))

    return found_foods, found_features

# Kakao 장소 검색
query = f"{location} 맛집"
all_results = search_places(query)

# '맛집' 키워드가 블로그에 언급된 장소만 필터링
filtered_results = []
for place in all_results:
    name = place["place_name"]
    food, features = get_food_and_features(f"{location} {name}")
    if features and "맛집" in features:
        # '맛집' 키워드는 출력에서 제외
        clean_features = [f for f in features if f != "맛집"]
        filtered_results.append((place, food, clean_features))

# 결과 출력
if filtered_results:
    for place, food, features in filtered_results:
        name = place["place_name"]
        address = place["road_address_name"] or place["address_name"]
        map_url = place["place_url"]

        st.markdown(f"### 📍 {name}")
        st.write(f"📌 주소: {address}")
        st.markdown(f"🔗 [카카오맵 보기]({map_url})")
        if food:
            st.write("🍽️ 대표 음식:", ", ".join(food))
        if features:
            for f in features:
                if f in feature_descriptions:
                    st.write("💬", feature_descriptions[f])
        st.markdown("---")
else:
    st.info("‘맛집’ 키워드가 포함된 블로그 후기를 찾을 수 있는 장소가 없습니다.")

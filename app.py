import os
import streamlit as st
from kakao_api import address_to_coords, search_kakao_places
from naver_api import search_naver_blog

st.title("🌴 여행지 기반 맛집 추천")

place = st.text_input("여행지를 입력하세요 (예: 부산 해운대)")
keyword = st.text_input("찾고 싶은 것 (예: 바다 카페, 한식 맛집)")

if st.button("검색하기") and place and keyword:
    x, y = address_to_coords(place)
    if x and y:
        results = search_kakao_places(keyword, x=x, y=y)
        if not results:
            st.warning("검색 결과가 없습니다.")
        for r in results[:5]:  # 상위 5개 장소
            st.subheader(r["place_name"])
            st.write(f"📍 주소: {r['road_address_name']}")
            st.write(f"🔗 지도 보기: [카카오맵 링크]({r['place_url']})")
            blogs = search_naver_blog(r["place_name"])
            if blogs:
                st.write("📝 블로그 후기:")
                for b in blogs:
                    st.markdown(f"- [{b['title']}]({b['link']})")
            st.markdown("---")
    else:
        st.error("주소를 좌표로 변환하지 못했습니다.")

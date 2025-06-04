import streamlit as st

st.set_page_config(page_title="여행 추천 서비스", page_icon="✈️")

st.title("🌍 여행지 추천 서비스")
st.markdown("여행지를 입력하면 추천 정보를 안내해드려요!")

location = st.text_input("여행지를 입력하세요", placeholder="예: 부산, 제주도")

if location:
    st.session_state["location"] = location
    st.success(f"여행지 **{location}**가 저장되었습니다!")
else:
    st.info("좌측 메뉴에서 추천 항목을 확인하려면 여행지를 먼저 입력하세요.")

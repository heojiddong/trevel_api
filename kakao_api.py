import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

def search_kakao_places(query, x=None, y=None, radius=5000):
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": query, "size": 10}
    if x and y:
        params.update({"x": x, "y": y, "radius": radius})
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    res = requests.get(url, headers=headers, params=params)
    return res.json().get("documents", [])

def address_to_coords(address):
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    res = requests.get(url, headers=headers, params=params)
    docs = res.json().get("documents", [])
    if docs:
        return docs[0]["x"], docs[0]["y"]
    return None, None

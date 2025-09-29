# # pip freeze > requirements.txt
# from youtube_transcript_api import YouTubeTranscriptApi
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, parse_qs


# def fetch_transcript(video_id, language="ko"):
#     """
#     유튜브 video_id와 언어코드로 자막(스크립트) 텍스트를 반환
#     """
#     try:
#         ytt_api = YouTubeTranscriptApi()
#         transcript_list = ytt_api.list(video_id)
#         transcript = None

#         try:
#             transcript = transcript_list.find_transcript([language])
#         except Exception:
#             try:
#                 transcript = transcript_list.find_generated_transcript([language])
#             except Exception:
#                 try:
#                     transcript = next(iter(transcript_list))
#                 except Exception:
#                     return "Error: No transcript available."

#         lang_info = transcript.language_code if transcript else ""

#         transcript_data = transcript.fetch()
#         text_list = []

#         for entry in transcript_data:
#             if hasattr(entry, 'text') and entry.text:
#                 text_list.append(entry.text)
#             elif isinstance(entry, dict) and 'text' in entry:
#                 text_list.append(entry['text'])

#         full_text = ' '.join(text_list)
#         return f"[{lang_info}] {full_text}"

#     except Exception as e:
#         return f"Error fetching transcript: {e}"
    
# def get_youtube_title_alternative(video_url):
#     try:
#         response = requests.get(video_url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
#         title = soup.find("meta", property="og:title")
#         return title["content"] if title else "Error: Title not found in the page"
#     except Exception as e:
#         return f"Error fetching title: {e}"
    
# def get_video_id(url: str) -> str:
#     """
#     유튜브 URL에서 video_id 추출
#     """
#     parsed_url = urlparse(url)
#     if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
#         query_params = parse_qs(parsed_url.query)
#         return query_params.get("v", [None])[0]
#     elif parsed_url.hostname in ["youtu.be"]:
#         return parsed_url.path.lstrip("/")
#     return None

# video_id = get_video_id("https://www.youtube.com/watch?v=YKrNsHX9dzY")
# title = get_youtube_title_alternative("https://www.youtube.com/watch?v=YKrNsHX9dzY")
# result = fetch_transcript(video_id, "ko")

# print(title, result)

# # Third-party Libraries
# from fastapi import APIRouter, Depends, Path
# from fastapi_pagination import Page, paginate
# from sqlalchemy.orm import Session
# from typing_extensions import Annotated
# import xml.etree.ElementTree as ET
# import requests
# import xmltodict

# # Local Application Modules
# from app.utils import get_db
# import config

# router = APIRouter()

# @router.get(
#     path="/",
#     tags=["공공데이터포털"],
#     summary="국립중앙의료원_전국 응급의료기관 정보 조회 서비스",
# )
# def get_emergency_infos(db: Session = Depends(get_db)):
#     url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytBassInfoInqire"
#     params = {"serviceKey": config.DATA_SECRET_KEY, "numOfRows": 1000, "pageNo": 1}

#     response = requests.get(url, params=params)
#     data_dict = xmltodict.parse(response.content)

#     items = data_dict["response"]["body"]["items"]["item"]

#     filtered = []
#     # 산부인과 응급 대응 가능 병원을 뽑는 로직
#     for item in items:
#         # 응급실 여부
#         is_hvec = int(item.get("hvec") or 0) > 0
#         # 응급실 운영 여부
#         is_dutyEryn = item.get("dutyEryn", "0") == "1"
#         # 산부인과 여부
#         is_OB_GYN = "산부인과" in item.get("dgidIdName", "")
#         # 산부인과 응급상황 대응 가능 여부 = 조산 산모 수용 가능
#         is_MKioskTy8 = item.get("mkioskTy8", "N") == "Y"
#         # 산부인과 응급상황 대응 가능 여부 = 신생아 수용 가능
#         is_MKioskTy10 = item.get("mkioskTy10", "N") == "Y"

#         if is_hvec and is_dutyEryn and (is_OB_GYN or is_MKioskTy8 or is_MKioskTy10):
#             filtered.append({
#                 "기관명": item.get("dutyName", ""),
#                 "우편번호": item.get("postCdn1", "") + item.get("postCdn2", ""),
#                 "주소": item.get("dutyAddr", ""),
#                 "대표전화": item.get("dutyTel1", ""),
#                 "응급실전화": item.get("dutyTel3", ""),
#             })

#     return {"data": filtered}

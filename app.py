"""젠틀페이 — 메인 랜딩 단일 페이지 (Flask, DB 없음)"""
import os

from dotenv import load_dotenv
from flask import Flask, Response, render_template

load_dotenv()
app = Flask(__name__)

# 사이트 대표 URL (canonical/OG/sitemap 기준) — 도메인 확정 시 .env SITE_URL 에 퓨니코드로 입력
SITE_URL = os.environ.get("SITE_URL", "http://localhost:5080").rstrip("/")
# 채널톡 상담 페이지 URL — 모든 상담/신청 CTA가 여기로 연결됨
CHANNEL_TALK_URL = os.environ.get("CHANNEL_TALK_URL", "https://alleell.channel.io/home")
AVG_PRICE = 2000000  # "평균 ○○원 비상금을 받았어요" 노출 금액
SITE_DESCRIPTION = ("카톡 한 번으로 끝나는 간편 매입 서비스, 젠틀페이. 30초 시세 조회, 평균 7분 입금, "
                    "본인 명의 계좌 안전거래. 연중무휴 09:00~24:00 상담.")


@app.context_processor
def inject_constants():
    return {
        "CULTURE_100K_PRICE": AVG_PRICE,
        "SITE_URL": SITE_URL,
        "CHANNEL_TALK_URL": CHANNEL_TALK_URL,
        "CHANNELTALK_PLUGIN_KEY": os.environ.get("CHANNELTALK_PLUGIN_KEY", ""),
        "SITE_DESCRIPTION": SITE_DESCRIPTION,
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/robots.txt")
def robots():
    return Response(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap():
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           f'<url><loc>{SITE_URL}/</loc><priority>1.0</priority></url></urlset>')
    return Response(xml, mimetype="application/xml")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5080)))

from flask import Flask, request, send_file, jsonify
import requests
import random
import os
import re

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def search_tiktok_videos(keyword):
    # 使用 TikTok 快速搜索 API（简化模拟）
    search_url = f"https://www.tikwm.com/api/feed/search?keywords={keyword}&count=10"
    resp = requests.get(search_url, headers=headers)
    data = resp.json()
    if data.get("data"):
        videos = data["data"]
        random_video = random.choice(videos)
        return random_video["url"]
    return None

def parse_video(video_url):
    # 使用 TikVid.com 来解析 TikTok 链接
    api_url = "https://api.tikvid.io/api/download"
    payload = {"url": video_url}
    response = requests.post(api_url, json=payload, headers=headers)
    data = response.json()
    if data.get("video_no_watermark"):
        return data["video_no_watermark"]
    return None

@app.route("/")
def index():
    return "访问 /api/tiktok?q=关键词 来获取一个 TikTok 视频文件"

@app.route("/api/tiktok")
def get_video():
    keyword = request.args.get("q")
    if not keyword:
        return jsonify({"error": "请传入关键词参数 ?q="}), 400

    # 搜索视频
    video_url = search_tiktok_videos(keyword)
    if not video_url:
        return jsonify({"error": "未搜索到视频"}), 404

    # 解析视频直链
    direct_link = parse_video(video_url)
    if not direct_link:
        return jsonify({"error": "视频解析失败"}), 500

    # 下载视频
    video_resp = requests.get(direct_link, stream=True)
    with open("static/temp.mp4", "wb") as f:
        for chunk in video_resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    # 返回视频文件
    return send_file("static/temp.mp4", mimetype="video/mp4")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, send_file
import requests
import random
import io

app = Flask(__name__)

# 示例解析 API（支持无水印下载）
PARSE_API = "https://api.nn.ci/tiktok/parse?url="

def get_tiktok_urls(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.tiktok.com/search?q={keyword}"
    response = requests.get(search_url, headers=headers)
    video_ids = list(set([line.split('"/video/')[1].split('"')[0] for line in response.text.split('"') if '/video/' in line]))
    return [f"https://www.tiktok.com/@user/video/{vid}" for vid in video_ids]

def parse_tiktok(url):
    try:
        response = requests.get(PARSE_API + url)
        data = response.json()
        return data.get("video")  # 视频直链
    except:
        return None

@app.route('/')
def home():
    return "访问 /api/tiktok?q=关键词 获取 TikTok 视频"

@app.route('/api/tiktok')
def api_tiktok():
    keyword = request.args.get("q")
    if not keyword:
        return "请提供关键词参数 q"

    urls = get_tiktok_urls(keyword)
    if not urls:
        return "❌ 未找到视频"

    random.shuffle(urls)
    for url in urls:
        video_url = parse_tiktok(url)
        if video_url:
            video_response = requests.get(video_url)
            return send_file(io.BytesIO(video_response.content), mimetype='video/mp4', as_attachment=False, download_name="video.mp4")

    return "❌ 视频解析失败，请稍后再试"

if __name__ == '__main__':
    app.run(debug=True)

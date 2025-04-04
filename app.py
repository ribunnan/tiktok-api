from flask import Flask, request, Response
import requests
import random

app = Flask(__name__)

def get_tiktok_video_url(keyword):
    api_url = f"https://api.tt-dl.com/api/search?keywords={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(api_url, headers=headers, timeout=10)
        data = res.json()

        if data.get("data"):
            videos = data["data"]
            selected = random.choice(videos)
            video_url = selected["video_data"]["nwm_video_url_HQ"]
            return video_url
        else:
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

@app.route("/api/tiktok")
def serve_video():
    keyword = request.args.get("q")
    if not keyword:
        return {"error": "缺少关键词参数 ?q=xxx"}

    video_url = get_tiktok_video_url(keyword)
    if not video_url:
        return {"error": "未能获取视频链接"}

    try:
        # 以流方式请求视频链接并直接返回 Response
        video_stream = requests.get(video_url, stream=True)
        return Response(video_stream.iter_content(chunk_size=1024),
                        content_type="video/mp4")
    except Exception as e:
        return {"error": f"视频获取失败：{str(e)}"}

@app.route("/")
def home():
    return "🎬 访问 /api/tiktok?q=关键词 来获取一个可播放的 TikTok 视频"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

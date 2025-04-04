from flask import Flask, request, send_file
import requests
import random
from io import BytesIO
import os

app = Flask(__name__)

# ✅ 用测试视频链接（确保可访问）
dummy_video_links = [
    "https://filesamples.com/samples/video/mp4/sample_640x360.mp4",
    "https://filesamples.com/samples/video/mp4/sample_960x400.mp4"
]

def get_video_url(keyword):
    # 可以替换为真正的 TikTok 解析 API
    return random.choice(dummy_video_links)

@app.route("/")
def home():
    return "🎬 TikTok 视频下载 API（用法：/api/tiktok?q=关键词）"

@app.route("/api/tiktok")
def tiktok():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return "❌ 缺少关键词参数 q", 400

    video_url = get_video_url(keyword)

    try:
        resp = requests.get(video_url, stream=True, timeout=10)

        # 🧪 判断是否成功获取视频
        if resp.status_code != 200 or "video" not in resp.headers.get("Content-Type", ""):
            return f"❌ 视频请求失败，状态码：{resp.status_code}", 500

        video_stream = BytesIO(resp.content)

        return send_file(
            video_stream,
            mimetype="video/mp4",
            as_attachment=True,
            download_name=f"{keyword}.mp4"
        )

    except Exception as e:
        return f"❌ 下载失败：{str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, send_file
import requests
import random
from io import BytesIO
import os

app = Flask(__name__)

# 示例视频列表（真实使用时可改为解析 API 提供的地址）
dummy_video_links = [
    "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
    "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_5mb.mp4"
]

def get_video_url(keyword):
    # 👉 你可以改为：根据关键词调用真正的 TikTok 搜索 + 解析接口
    # 当前是模拟的：随机返回一个视频链接
    return random.choice(dummy_video_links)

@app.route("/")
def home():
    return "🎬 TikTok 视频下载 API（使用示例：/api/tiktok?q=关键词）"

@app.route("/api/tiktok")
def tiktok():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return "❌ 缺少关键词参数 `q`", 400

    try:
        video_url = get_video_url(keyword)
        resp = requests.get(video_url, stream=True)
        video_stream = BytesIO(resp.content)
        return send_file(
            video_stream,
            mimetype="video/mp4",
            as_attachment=True,
            download_name=f"{keyword}.mp4"
        )
    except Exception as e:
        return f"❌ 视频获取失败：{str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # for Render 部署
    app.run(host="0.0.0.0", port=port)

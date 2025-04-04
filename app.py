from flask import Flask, request, send_file, jsonify
import requests
import os
import random

app = Flask(__name__)
VIDEO_PATH = 'static/temp.mp4'

@app.route('/')
def home():
    return '✅ TikTok 视频 API：使用 /api/tiktok?q=关键词 获取随机视频。'

@app.route('/api/tiktok')
def get_video():
    keyword = request.args.get('q')
    if not keyword:
        return jsonify({"error": "请提供关键词参数 ?q="})

    try:
        # 使用 TiklyDown 的解析 API
        api_url = f'https://api.tiklydown.com/api/download/search?keywords={keyword}'
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(api_url, headers=headers)
        data = res.json()

        videos = data.get("video", [])
        if not videos:
            return jsonify({"error": f"❌ 没找到和『{keyword}』有关的视频，请换个关键词试试。"})

        # 随机选择视频
        random_video = random.choice(videos)
        video_url = random_video.get("no_watermark")
        if not video_url:
            return jsonify({"error": "未获取到无水印链接。"})

        # 下载并保存视频
        video_data = requests.get(video_url).content
        with open(VIDEO_PATH, 'wb') as f:
            f.write(video_data)

        # 返回 mp4 文件
        return send_file(VIDEO_PATH, mimetype='video/mp4', as_attachment=False)

    except Exception as e:
        return jsonify({"error": f"服务器异常：{str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

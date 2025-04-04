from flask import Flask, request, send_file, jsonify
import requests
import tempfile
import random

app = Flask(__name__)

# 示例 API（你要替换成真实能返回视频下载地址的 API）
PARSE_API = "https://api.tikwm.com/video/search?keywords={}"

@app.route('/')
def home():
    return "🎬 TikTok 视频下载 API"

@app.route('/api/tiktok')
def tiktok_video():
    keyword = request.args.get("q")
    if not keyword:
        return jsonify({"error": "请提供关键词参数 q"})

    try:
        # 解析关键词，获取视频链接
        api_url = PARSE_API.format(keyword)
        res = requests.get(api_url)
        data = res.json()
        video_list = data.get("data", {}).get("videos", [])

        if not video_list:
            return jsonify({"error": "未找到视频"})

        video_url = random.choice(video_list).get("play")  # 注意替换字段名
        if not video_url:
            return jsonify({"error": "视频链接无效"})

        # 下载视频文件
        video_res = requests.get(video_url, stream=True)
        if video_res.status_code != 200:
            return jsonify({"error": "视频下载失败"})

        # 使用临时文件保存视频
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        for chunk in video_res.iter_content(chunk_size=8192):
            tmp_file.write(chunk)
        tmp_file.close()

        # 返回视频文件
        return send_file(tmp_file.name, mimetype='video/mp4', as_attachment=True, download_name='video.mp4')

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

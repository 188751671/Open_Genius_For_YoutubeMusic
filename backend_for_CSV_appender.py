from urllib.parse import urlparse, parse_qs
import base64
import time
import logging

# Third-party libraries: pipenv intall
import requests
from flask import Flask, request, jsonify

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# GitHub配置
GITHUB_TOKEN = '..........'
REPO_OWNER = '188751671'
REPO_NAME = 'Open_Genius_For_YoutubeMusic'
CSV_FILE_PATH = 'videoID_To_GeniusURL.csv'

# 创建Flask应用
app = Flask(__name__)

def validate_youtube_url(url):
    """验证YouTube URL并返回元组 (is_valid, video_id, video_title)"""
    try:
        parsed = urlparse(url)
        if parsed.netloc not in ['www.youtube.com', 'youtube.com']:
            return False, None, None
            
        query = parse_qs(parsed.query)    
        video_id = query.get('v', [None])[0]
        
        if not video_id:
            return False, None, None
            
        # 通过oEmbed API检查
        oembed_url = f'https://www.youtube.com/oembed?url={url}&format=json'
        response = requests.get(oembed_url)
        
        if response.status_code == 200:
            # 从oEmbed响应中提取标题
            data = response.json()
            video_title = data.get('title', '')
            return True, video_id, video_title
        else:
            return False, None, None
        
    except Exception as e:
        logger.error(f"YouTube validation error: {e}")
        return False, None, None

def validate_genius_url(url, youtube_title):
    """验证Genius URL并返回slug（如果有效）"""
    try:
        if not url.startswith('https://genius.com/'):
            return False, None
            
        parsed = urlparse(url)
        slug = parsed.path.strip('/')

        # 路径总是以'-lyrics'结尾
        if not slug.endswith('-lyrics'):
            return False, None

        # 如果可以成功获取页面 (有时候Genius会拒绝 机器请求, 所以暂时关闭这个检查)
        # response = requests.get(
        #     url,
        #     # 模拟用户浏览器 给Genius发请求, 避免被检测为脚本 而拒绝
        #     headers={"User-Agent": "Mozilla/5.0"},
        #     timeout=10
        # )
        # if response.status_code != 200:
        #     return False, None
        
        # Genius slug的倒数第二或第三部分必须在Youtube标题中
        slug_parts = slug.split('-')
        if len(slug_parts) < 2:
            return False, None
        if slug_parts[-2].lower() not in youtube_title.lower():
            if len(slug_parts) < 3:
                return False, None
            if slug_parts[-3].lower() not in youtube_title.lower():
                return False, None
        
        return True, slug
    
    except Exception as e:
        logger.error(f"Genius validation error: {e}")
        return False, None

def update_github_csv(video_id, genius_slug):
    """更新GitHub上的CSV文件，添加新条目"""
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    api_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{CSV_FILE_PATH}'

    # 获取现有文件数据
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        return False, 'cannot fetch CSV file'
    
    file_data = response.json()
    content = base64.b64decode(file_data['content']).decode('utf-8')
    sha = file_data['sha']

    # 检查video_id是否已存在
    if video_id in content:
        return False, 'video already exists'

    # 添加新条目
    new_entry = f'{video_id},{genius_slug}\n'
    new_content = content + new_entry
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    # 提交更改
    data = {
        'message': 'Added New Entry',
        'content': encoded_content,
        'sha': sha
    }
    
    response = requests.put(api_url, headers=headers, json=data)
    return response.status_code in (200, 201), f"added: {genius_slug}"

def cors_json(payload, status=200):
    resp = jsonify(payload)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp, status

@app.route('/', methods=['POST', 'OPTIONS'])
def open_genius():
    # 处理预检请求
    if request.method == "OPTIONS":
        return cors_json({'message': 'success'}, 200)

    # 获取JSON格式的表单数据
    try:
        form = request.get_json()
        youtube_url = form.get('youtube_url')
        genius_url = form.get('genius_url')
    except Exception as e:
        logger.error(f"request parse error: {e}")
        return cors_json({'message': 'invalid request data'}, 400)

    if not youtube_url or not genius_url:
        logger.warning("missing URL")
        return cors_json({'message': 'missing URL'}, 400)

    start_time = time.time()
    yt_valid, video_id, youtube_title = validate_youtube_url(youtube_url)
    logger.info(f"YouTube URL validation time: {(time.time() - start_time):.3f}s")
    
    if not yt_valid:
        logger.warning(f"invalid YouTube URL: {youtube_url}")
        return cors_json({'message': 'invalid YouTube URL'}, 400)

    start_time = time.time()
    genius_valid, genius_slug = validate_genius_url(genius_url, youtube_title)
    logger.info(f"Genius URL validation time: {(time.time() - start_time):.3f}s")
    
    if not genius_valid:
        logger.warning(f"invalid Genius URL: {genius_url}")
        return cors_json({'message': 'invalid Genius URL'}, 400)

    start_time = time.time()
    success, msg = update_github_csv(video_id, genius_slug)
    logger.info(f"GitHub CSV update time: {(time.time() - start_time):.3f}s")
    
    if not success:
        logger.error(f"CSV update failed: {msg}")
        return cors_json({'message': f'CSV update failed: {msg}'}, 500)

    # 返回成功响应
    return cors_json({'message': msg}, 200)


# 添加健康检查路由 (直接打开API地址  spomatching.com/api/Open_Genius_For_YoutubeMusic  出现以下状态信息)
@app.route('/', methods=['GET'])
def health_check():
    return cors_json({
        'status': 'online',
        'service': 'Open_Genius_For_YoutubeMusic',
        'version': '1.0'
    }, 200)


if __name__ == '__main__':
    logger.info("Starting Open Genius For YoutubeMusic service on port 8000...")
    app.run(host='0.0.0.0', port=8000)

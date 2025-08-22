from flask import Flask, render_template, request, Response, jsonify, url_for
from main import download_chapter, get_chapter_list, sanitize_filename, validate_novel_url
import io
import os
import json
import uuid
from urllib.parse import quote as url_quote

# Create a directory for temporary files if it doesn't exist
if not os.path.exists('temp_files'):
    os.makedirs('temp_files')

app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:8080'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate-url', methods=['POST'])
def validate_url_endpoint():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "message": "URL is required"}), 400

    result = validate_novel_url(url)
    return jsonify(result)

@app.route('/download_stream')
def download_stream():
    url = request.args.get('url')
    token = request.args.get('token')
    download_type = request.args.get('download_type')
    start_chapter_str = request.args.get('start_chapter', '1')
    end_chapter_str = request.args.get('end_chapter', '1')

    def generate():
        try:
            novel_name, chapters = get_chapter_list(url, token=token)
            total_chapters = len(chapters)

            if download_type == '下载范围':
                start_chapter = int(start_chapter_str)
                end_chapter = int(end_chapter_str)
                chapters_to_download = chapters[start_chapter - 1:end_chapter]
                filename = f"{novel_name}_Chapters_{start_chapter}-{end_chapter}.txt"
            else: # '下载全部'
                chapters_to_download = chapters
                filename = f"{novel_name}_All_Chapters.txt"

            safe_filename = sanitize_filename(filename)
            
            # Using io.StringIO to build the file in memory
            string_io = io.StringIO()
            count = 0
            total_to_download = len(chapters_to_download)

            for chapter in chapters_to_download:
                count += 1
                progress_data = {
                    "current": count,
                    "total": total_to_download,
                    "message": f"正在下载: {chapter['title']}"
                }
                yield f"data: {json.dumps(progress_data)}\n\n"

                title, content = download_chapter(chapter['url'], url, token=token)

                if content == "CAPTCHA":
                    captcha_url = chapter['url']
                    error_data = {
                        "error": "CAPTCHA", 
                        "message": "检测到验证码，请在新标签页中完成验证后重试。",
                        "url": captcha_url
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                    return

                string_io.write(f"Title: {title}\n\n")
                string_io.write(content)
                string_io.write("\n\n---\n\n")

            # Save the final content to a temporary file
            full_content = string_io.getvalue()
            temp_filename = f"{uuid.uuid4()}.txt"
            temp_filepath = os.path.join('temp_files', temp_filename)
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            # Send completion message with download link
            with app.app_context():
                download_url = url_for('download_file', filename=temp_filename, _external=True, original_filename=safe_filename)
                completion_data = {"status": "completed", "url": download_url}
                yield f"data: {json.dumps(completion_data)}\n\n"

        except Exception as e:
            error_data = {"error": "Exception", "message": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/download_file/<filename>')
def download_file(filename):
    original_filename = request.args.get('original_filename', 'download.txt')
    temp_filepath = os.path.join('temp_files', filename)
    
    if not os.path.exists(temp_filepath):
        return "File not found.", 404

    def generate_file():
        with open(temp_filepath, 'rb') as f:
            yield from f
        # Clean up the file after sending
        os.remove(temp_filepath)

    safe_filename_quoted = url_quote(original_filename)

    headers = {
        'Content-Disposition': f"attachment; filename*=UTF-8''{safe_filename_quoted}"
    }
    return Response(generate_file(), mimetype='text/plain', headers=headers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

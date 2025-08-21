from flask import Flask, render_template, request, Response
from main import download_chapter, get_chapter_list, sanitize_filename
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['download_type']

    novel_name, chapters = get_chapter_list(url)

    if download_type == 'Download Range':
        start_chapter = int(request.form['start_chapter'])
        end_chapter = int(request.form['end_chapter'])
        # Adjust for 0-based indexing and inclusive end
        chapters_to_download = chapters[start_chapter - 1:end_chapter]
        filename = f"{novel_name}_Chapters_{start_chapter}-{end_chapter}.txt"
    else: # Download All
        chapters_to_download = chapters
        filename = f"{novel_name}_All_Chapters.txt"

    # Using io.StringIO to build the file in memory
    string_io = io.StringIO()

    for chapter in chapters_to_download:
        title, content = download_chapter(chapter['url'])
        string_io.write(f"Title: {title}\n\n")
        string_io.write(content)
        string_io.write("\n\n---\n\n")

    # Get the content from the StringIO object
    full_content = string_io.getvalue()

    safe_filename = sanitize_filename(filename)

    return Response(
        full_content,
        mimetype="text/plain",
        headers={"Content-disposition":
                 f"attachment; filename=\"{safe_filename}\""}
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

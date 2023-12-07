from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
from validate import validate_request, validate_request_download
from flask_cors import CORS
import random
import string



app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/youtubemediainfo', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        success, error_message = validate_request(request.args)
        if not success:
            return jsonify({'error': error_message}), 400

        videourl = request.args.get('videourl')
        mediatype = request.args.get('mediatype')
        type = 'mp4' if mediatype == 'video' else 'mp3'

        # Traitement pour les requêtes GET avec videourl
        media = YouTube(videourl)
        title = media.title
        description = media.description
        thumbnail = media.thumbnail_url

        if mediatype == 'video':
            streams = [{'resolution': stream.resolution,
                        'filetype': stream.subtype,
                        'itag': stream.itag,
                        'url': stream.url}
                       for stream in media.streams.filter(file_extension=type)]
        else:
            streams = [{'filetype': stream.subtype,
                        'url': stream.url}
                       for stream in media.streams.filter(only_audio=True)]

        response_data = {'title': title,
                         'description': description,
                         'thumbnail': thumbnail,
                         'streams': streams,
                         'videourl': videourl}

        return jsonify(response_data)
    elif request.method == 'POST':
        success, error_message = validate_request(request.json)
        if not success:
            return jsonify({'error': error_message}), 400

        data = request.json
        videourl = data['videourl']
        # Faites quelque chose avec les données reçues
        return jsonify({'message': 'POST request received', 'videourl': videourl})
    else:
        return jsonify({'error': 'Method not allowed'}), 405
    
 # add code to download video from youtube link

@app.route('/api/download', methods=['GET'])
def download_video_from_youtube():
     success, error_message = validate_request_download(request.args)
     if not success:
        return jsonify({'error': error_message}), 400
     print('ok')
     link = request.args.get('videourl')
     itag = request.args.get('itag')
     print(f'link: {link}, itag: {itag}') #print(link)
     yt = YouTube(link)
     
     stream = yt.streams.get_by_itag(itag)
     #generate random filename 
     
     letters = string.ascii_lowercase
     result_str = ''.join(random.choice(letters) for i in range(10))
     filename = f"{result_str}.{stream.subtype}"
     stream.download(filename='downloads/' + filename) 
     
     #return the link to dowload video from api
     return jsonify({'file': filename})


@app.route('/api/downloads/<filename>')
def get_image(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(debug=True)

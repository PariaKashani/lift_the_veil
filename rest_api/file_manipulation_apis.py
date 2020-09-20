import scripts.gpx_cleaner as gpx_cleaner
import scripts.download_dataset as download_dataset
import scripts.compress_files as compress_files
from flask import Flask, request
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)


@app.route('/prepare_data',methods=['GET'])
def prepare():
    # track_name example: Filisur_Thusis_20200821
    # save_dir : local dir to save downloaded data
    # track_data_file : name of track data file to be downloaded
    # data: a movie, a gpx file, a track_side_data file
    # first prepare local folder to save data
    track_name = request.args.get('track_name')
    save_dir = request.args.get('save_dir')
    track_data_file = request.args.get('track_data_file')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    track_data_dir = os.path.join(save_dir, 'Trackdata')
    track_movies_dir = os.path.join(save_dir, 'Trackmovies',track_name)
    if not os.path.exists(track_data_dir):
        os.makedirs(track_data_dir)
    if not os.path.exists(track_movies_dir):
        os.makedirs(track_movies_dir)
    # download track_date
    result1 = download_dataset.download_file(track_data_file,
                                             os.path.join('Trackdata', track_data_file),
                                             track_data_dir)
    print('file',result1, 'successfully downloaded and saved!')
    # download track_gpx
    result2 = download_dataset.download_file('movie.gpx',
                                             os.path.join('Trackmovies',track_name, 'movie.gpx'),
                                             track_movies_dir)
    print('file', result2, 'successfully downloaded and saved!')
    # clean track_data
    result3 = gpx_cleaner.clean_gpx_file(result2)
    print('file', result3, 'successfully cleaned!')
    # download track_movie
    result4 = download_dataset.download_file('movie.mp4',
                                             os.path.join('Trackmovies',track_name, 'movie.mp4'),
                                             track_movies_dir)
    print('file', result4, 'successfully downloaded and saved!')
    # compress track_movie
    result5 = compress_files.compress_video(result4)
    print('file', result5, 'successfully compressed!')


if __name__ == '__main__':
     app.run()
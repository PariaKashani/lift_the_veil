import sys
import os
import ffmpy


def compress_video(file_name):
    # file name with complete path
    ff = ffmpy.FFmpeg(executable='F:\\ffmpeg\\bin\\ffmpeg.exe',
                      inputs={file_name: None},
                      outputs={file_name[:-4]+'_compress.mp4': None})
    ff.run()
    #     remove last video
    os.remove(file_name)
    return file_name[:-4]+'_compress.mp4'


if __name__=='__main__':
    compress_video(sys.argv[1])

import sys
import os
import boto3


def download_file(file_name, server_file_name, save_dir):
    s3 = boto3.client('s3')
    result_file = os.path.join(save_dir, file_name)
    with open(result_file, 'wb') as f:
        s3.download_fileobj('hackzurich', server_file_name, f)
    return result_file


if __name__ == "__main__":
    download_file(sys.argv[1], sys.argv[2], sys.argv[3])
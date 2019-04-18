from google.cloud import storage
import subprocess
import sys

def formatCmd(file, config):
    cmd = "gsutil cp "+"gs://"+config["bucketName"]
    cmd += "/"+file
    cmd += " /tmp"
    return cmd

def copyFiles(config):
    ''' We store the Enhanced MNIST data on GCloud Storage. Copy it to /tmp to be processed '''
    client = storage.Client()
    bucket = client.get_bucket(config["bucketName"])
    for file in config["fileNames"]:
        cmd = formatCmd(file, config)
        result = subprocess.call(cmd, shell=True)
        if result != 0:
            print("CMD failed...aborting")
            print(cmd)
            sys.exit()
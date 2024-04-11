
import boto3
import base64
import uuid
import pickle
import numpy as np
from PIL import Image
import os
import io
import json
import xgboost
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

model_bucket = "---" # your bucket name
os.environ['TZ'] = 'Asia/Tokyo' # your time zone
SRC_MAIL = '---' # mail sender address
DST_MAIL = '---' # mail resiver address
SES_REGION = "ap-northeast-1" # your region
ses = boto3.client('ses', region_name=SES_REGION)

def send_raw_email(source, to, subject, body, img_absolute_path):
    
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = SRC_MAIL
    msg['To'] = DST_MAIL
    body_msg = MIMEText(body, 'plain')
    msg.attach(body_msg)

    att = MIMEApplication(open(img_absolute_path, 'rb').read())
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(img_absolute_path))
    msg.attach(att)
    
    response = ses.send_raw_email(
    Source=source,
    Destinations=[to],
    RawMessage={
    'Data':msg.as_string()
    }
    )
    return response

def download_pickle_from_s3(file) -> object:
    with io.BytesIO() as data:
        s3 = boto3.client('s3')
        s3.download_fileobj(model_bucket, file, data)
        data.seek(0)
        return pickle.load(data)

def handler(event, context):
    s3 = boto3.client('s3')
    key = "image.jpg" # image name
    imagePath = "/tmp/" + os.path.basename(key)
    
    # S3のバケットからファイルをダウンロード
    s3.download_file(Bucket=model_bucket, Key=key, Filename=imagePath)

    img1 = Image.open(imagePath)
    img2 = img1.resize((64,64))
    img = np.array(img2)
    im_array = np.ravel(np.asarray(img)) # 画像を配列に変換
    im_regularized = im_array/255. #正規化
    im_regularized = im_regularized.reshape(1, -1)
    model = download_pickle_from_s3("finalized_model.pkl") # sklearn saved model name
    
    predict = int(model.predict(im_regularized))

    subject = "phoxから郵便受けについてのお知らせです"
    if predict == 0 :
        message = "郵便受けが開閉されました。\n現在郵便受けの中身は空です。 \n画像をご確認ください。\n \n-------------------- \nteam phantom \nE-mail : team.phantom.community@gmail.com \n--------------------\n"
    elif predict == 1 :
        message = "郵便受けが開閉されました。\n現在郵便受けには書類が入っています。 \n画像をご確認ください。\n \n-------------------- \nteam phantom \nE-mail : team.phantom.community@gmail.com \n--------------------\n"
    elif predict == 2:
        message = "郵便受けが開閉されました。\n現在郵便受けには荷物が入っています。 \n画像をご確認ください。\n \n-------------------- \nteam phantom \nE-mail : team.phantom.community@gmail.com \n--------------------\n"
    else :
        message = "このメールは誤報です。\n 無視してください。 \n \n-------------------- \nteam phantom \nE-mail : team.phantom.community@gmail.com \n--------------------\n"
    # メール送信
    ans = send_raw_email(SRC_MAIL, DST_MAIL, subject, message, imagePath)
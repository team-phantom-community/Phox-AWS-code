
import boto3
import base64
import json

def convert_b64_string_to_bynary(s):
    """base64をデコードする"""
    return base64.b64decode(s.encode("UTF-8"))

def lambda_handler(event, context):
    # eventの部分にAPIから受け取ったjsonが入る
    # event['xxx']と記述して受け取ったjsonの要素xxxを取り出す
    base_64ed_image = event['myjpg'] # この部分でbase_64ed_imageにAPIに投げられたバイナリの画像データを格納している
    position = event['position'] # この部分でpositionにphoxで読み取った測距センサの真偽値を格納している
    json_data = {"position": position} # AWS S3に保存するためにpositionデータをjsonとしてまとめている

    s3 = boto3.resource('s3') # AWS S3読み込む(実行ロールにS3操作権限必須)
    bucket = s3.Bucket('phox-bucket') # 保存先のバケットを開く
    # バイナリから変換されたjpgファイルをファイル名を「image.jpg」として保存(この場合、保存されるたびにファイルが上書きされる)
    bucket.put_object(
                    Key='image.jpg',
                    Body=convert_b64_string_to_bynary(base_64ed_image))
    # positionデータをjsonファイルとしてバケット上に保存
    bucket.put_object(
                    Key='position.json',
                    Body=json.dumps(json_data))
    # 適切に実行されたことをAPIで返却
    return {'statusCode': 200}
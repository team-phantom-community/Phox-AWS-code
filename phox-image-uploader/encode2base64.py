
from google.colab import files
import base64
def convert_file_to_b64_string(file_path):
    """base64にエンコードする"""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("UTF-8")


image = files.upload() # ファイルアップロード
print(convert_file_to_b64_string(image)) #エンコードしたデータを返す
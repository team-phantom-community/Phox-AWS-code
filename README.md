# Phox-AWS-code
iCAN24、Plus AlphantomのPhoxに用いられたAWSのコードおよびその使い方について

### 準備
- [AWS(Amazon Web Service)](https://aws.amazon.com/jp/)にアクセス
- アカウントを作成
- コードを作成する際にはセキュリティ対策のためルートユーザーとは別にIAM(Identity and Access Management)ユーザーを作成し、作成したIAMユーザーの中で作業を行う
- [IAMユーザーの作り方](https://qiita.com/uskayyyyy/items/395bbe670a33f87c35de)
- IAMユーザーのアクセス権限
  - 一般にはIAMユーザーには必要以上の権限を与えないようにユーザー独自のポリシーを作成する
  - また、複数人にユーザーを与える場合にはユーザーグループを作成し、そのユーザーグループにポリシーをアタッチすることも可能
  - 試験運用で必要となるポリシーが明確でない場合には「Administator Access」(ルートユーザーと同じ権限を持つ)か「Power User」(IAMの設定のみ弄ることができない)にしても良い
- 実行ロールの設定
  - AWSで高頻度に用いられる[lambda](https://aws.amazon.com/jp/lambda/)などでは、関数にロールをアタッチすることでlambdaからs3やSESといったAWSの別のリソースにアクセスすることが可能となる
  - 実行ロールの作成はルートユーザーまたはAdministator Accessを持つユーザーしか基本的にできない
  - 上記のユーザーでないユーザーはあらかじめ作られたロールを用いることになる
  - ロール作成の際は「IAM」->「ロール」->「ロールを作成」->「AWSのサービス、ユースケース：lambda」を選択し、次の画面でそのロールで許可したいサービスを追加する
  - ロールについても必要以上多くの権限を与えてしまうとセキュリティ上の問題になるので最低限の権限にとどめることが推奨される
  - 開発段階においてはアクセスしたいサービスの「……FullAccess」を追加しても良い
 
### システム構成
- phox-image-uploader(lambda) : Base64変換された画像データをAPIで受け取りAWS S3へ当該の画像をアップロードする
- phox-bucket(AWS S3 bucket)  : アップロードされた画像を保存するバケット(フォルダ)
- phox-mail-sender(lambda)    : phox-bucketに画像がアップロードされたことをトリガーにして動くlambda関数
- phox-container(AWS ECR)     : phox-mail-senderのdockerイメージを実行するリポジトリ
- Google Colablatory          : 画像認識モデルデータ作成に用いる

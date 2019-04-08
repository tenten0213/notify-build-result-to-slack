# Notify build result to Slack

CodeBuildの結果をSlackに通知する。

## 事前準備

ServerlessとAWS CLIがインストールされていること。

* [Serverlessをインストールする](https://serverless.com/framework/docs/getting-started/)
* [AWS Command Line Interface をインストールする](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-install.html)

## デプロイの準備

### AWS Credentialsの登録

| 項目 |概要|
|--------|--------|
| `${awsAccessKey}` | 利用するIAMのaccess_keyを設定する。|
| `${awsSecretAccessKey}` | 利用するIAMのsecret_access_keyを設定する。|

```bash
$ sls config credentials --provider aws --key ${awsAccessKey} --secret ${awsSecretAccessKey}
```

### SlackのIncoming WebhookのWebhook URLを取得する

以下にアクセスし、取得する。

* https://slack.com/services/new/incoming-webhook

### SlackのWebHook URLを暗号化

| 項目 |概要|
|--------|--------|
| `${kmsKeyId}` | 利用するKMSの鍵のキーIDを設定する。|
| `${webHookUrl}` | SlackのWebHook URLは `https://` を除いた値で置き換える。|

```bash
$ aws kms encrypt --key-id ${kmsKeyId} --plaintext ${webHookUrl} --output text --query CiphertextBlob
```

上記コマンドを実行すると、KMSの暗号鍵によって暗号されたSlackのWebHook URLが出力される。

* 例

```
AQIBAHivAwH1CMP7mLDyxFp58OcpPu7pseBTDpThY/wO7bIm0wEWaAWkIUKUr/6+Sq86+sg3AABCpzCBpAYJKoZIhvcNAQcGoIGWMIGTAgEAMIGNBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDFFABgqlOFIS/mznSQLIDIBgsAfMCR99tCCN91BLRW9SmQ2/Wh88hhPGzQDJf8nzUVfb+Jn3asHLRRUCuDQAX74zGZW+5n/yqmOmKsgjXZ8yhEz5sIQPR0OsFvyViImQnpwlJFf2wqFEXAMPLE/a
```

## デプロイ

| 項目 |概要|
|--------|--------|
| `${stage}` | デプロイする環境面を設定する。|
| `${projectName}` | 監視対象のCodeBuildプロジェクト名を設定する。|
| `${kmsKeyArn}` | 利用するKMSの鍵のARNを設定する。|
| `${channel}` |通知先のSlackのチャンネルを設定する。|
| `${encryptedHookUrl}` |SlackのWebHook URLを暗号化した値を設定する。|

```bash
$ sls deploy --stage "${stage}" --projectName "${projectName}" --kmsKeyArn "${kmsKeyArn}" --channel "${channel}" --encryptedHookUrl "${encryptedHookUrl}"
```

* 例

```bash
$ sls deploy --stage "production" --projectName "SampleProject" --kmsKeyArn "arn:aws:kms:ap-northeast-1:9999999:key/99999999-AAAA-aaaa-ffff-999999999" --channel "#general" --encryptedHookUrl "AQIBAHivAwH1CMP7mLDyxFp58OcpPu7pseBTDpThY/wO7bIm0wEWaAWkIUKUr/6+Sq86+sg3AABCpzCBpAYJKoZIhvcNAQcGoIGWMIGTAgEAMIGNBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDFFABgqlOFIS/mznSQLIDIBgsAfMCR99tCCN91BLRW9SmQ2/Wh88hhPGzQDJf8nzUVfb+Jn3asHLRRUCuDQAX74zGZW+5n/yqmOmKsgjXZ8yhEz5sIQPR0OsFvyViImQnpwlJFf2wqFEXAMPLE/a"
```

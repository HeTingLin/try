from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage,ImageSendMessage
)

app = Flask(__name__)

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    msg = event.message.text
    if "貼圖" in msg or "sticker" in msg:
        message=StickerSendMessage(
            package_id=random.randint(0, len(package_ids) - 1),
            sticker_id=random.randint(0, len(sticker_ids) - 1))
        line_bot_api.reply_message(event.reply_token,message)
    if "圖片" in msg or "picture" in msg:
        message=ImageSendMessage(
           original_content_url='https://www.google.com/search?biw=1280&bih=529&tbm=isch&sa=1&ei=tfQrXZKbEpuGoATh7LbACg&q=%E5%A4%AA%E9%99%BD&oq=%E5%A4%AA&gs_l=img.1.0.0l10.8164.12558..14308...0.0..1.906.1170.4j6-1......0....1..gws-wiz-img.....0.r3S2wCE8cAY#imgrc=Vj-PdRiIWZyZXM:',
           preview_image_url='https://www.google.com/search?biw=1280&bih=529&tbm=isch&sa=1&ei=tfQrXZKbEpuGoATh7LbACg&q=%E5%A4%AA%E9%99%BD&oq=%E5%A4%AA&gs_l=img.1.0.0l10.8164.12558..14308...0.0..1.906.1170.4j6-1......0....1..gws-wiz-img.....0.r3S2wCE8cAY#imgrc=Vj-PdRiIWZyZXM:')
        line_bot_api.reply_message(event.reply_token,message)
    # 回應使用者輸入的話
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=event.message.text))
          


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)

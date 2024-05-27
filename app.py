from flask import Flask, request, send_file, render_template_string, jsonify

app = Flask(__name__)

# HTML 模板，用於顯示圖片
html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>AIoT 控制</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript">
      $(document).ready(function(){
        setInterval(function(){
          $("#house-image").attr("src", "/image?" + new Date().getTime());
        }, 1000);
      });
    </script>
  </head>
  <body>
    <h1>房子狀態</h1>
    <img id="house-image" src="/image" alt="House Image">
  </body>
</html>
"""

# 狀態變量，初始值為 0（off）
status = 0

@app.route('/aiot', methods=['GET'])
def aiot():
    global status
    # 獲取 status 參數
    new_status = request.args.get('status')
    if new_status is not None:
        # 更新狀態
        status = int(new_status)
    # 返回 JSON 回應
    return jsonify({"status": "OK"})

@app.route('/image')
def get_image():
   # 根據當前狀態返回對應的圖片
   if status == 1:
       return send_file('on.png', mimetype='image/png')
   else:
       return send_file('off.png', mimetype='image/png')

@app.route('/status', methods=['GET'])
def get_status():
    # 返回當前狀態的 JSON 回應
    resp = "off"
    if (status == 1):
        resp = "on"

    return jsonify({"status": resp})

@app.route('/')
def index():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4443)


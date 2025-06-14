from flask import Flask, request, jsonify
import mysql.connector
import re

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Enter password here",
    database="QLBH"
)
cursor = db.cursor(dictionary=True)

#Define username characters
USERNAME_REGEX = re.compile(r'^[A-Za-z0-9@_-]{1,20}$')

#Func: Register account
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not username or len(username) == 0:
        return jsonify({"error": "Username không được để trống"}), 400

    if not password or len(password) == 0:
        return jsonify({"error": "Password không được để trống"}), 400

    if not confirm_password or len(confirm_password) == 0:
        return jsonify({"error": "confirm Password không được để trống"}), 400

    if not username or not USERNAME_REGEX.match(username):
        return jsonify({"error": "Username không hợp lệ."}), 400

    if not username or len(username) < 3:
        return jsonify({"error": "Username quá ngắn."}), 400

    if not password or len(password) < 3:
        return jsonify({"error": "Password quá ngắn."}), 400

    if password != confirm_password:
        return jsonify({"error": "Confirm password không khớp."}), 400

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"error": "❌ Username đã được sử dụng. Vui lòng chọn tên khác."}), 409

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"error": "Username đã tồn tại."}), 400

    #Add new users
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    return jsonify({"message": "Đăng ký thành công!"})

#Func: Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Đăng nhập thành công!"})
    else:
        return jsonify({"error": "Sai username hoặc password."}), 401

#Func: Forgot password and set up new password
@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    username = data.get("username")
    new_password = data.get("new_password")
    confirm_new_password = data.get("confirm_new_password")

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Username không tồn tại."}), 404

    if not new_password or len(new_password) < 3:
        return jsonify({"error": "Password mới quá ngắn."}), 400

    if new_password != confirm_new_password:
        return jsonify({"error": "Password xác nhận không khớp."}), 400

    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    db.commit()
    return jsonify({"message": "Đặt lại mật khẩu thành công!"})

if __name__ == "__main__":
    app.run(debug=True)


# testcases
if __name__ == "__main__":
    print(register("test_user", "abc123", "abc123"))         # ✅ Tạo thành công
    print(register("test_user", "abc123", "abc123"))         # ❌ trùng
    print(register("user@", "12", "12"))                     # ❌ password quá ngắn
    print(register("test?", "abc123", "abc123"))             # ❌ username không hợp lệ
    print(register("validuser", "password", "wrong"))        # ❌ confirm password sai
    print(register("", "test", "test"))                      # ❌ Để trống username
    print(register("test", "", "test"))                      # ❌ Để trống password
    print(register("test", "test", ""))                      # ❌ Để trống confirm password


    print(login("test_user", "abc123"))                      # ✅ Login thành công
    print(login("test_user", "wrongpass"))                   # ❌ sai password - đúng username
    print(login("account", "abc123"))                        # ❌ đúng password - sai username

    print(forgot_password("test_user", "newpass", "newpass"))       # ✅ Đặt lại mật khẩu thành công
    print(login("test_user", "newpass"))                            # ✅ mật khẩu mới
    print(forgot_password("unknown_user", "abc", "abc"))            # ❌ không tồn tại
    print(forgot_password("test_user", "ab", "ab"))                 # ❌ quá ngắn
    print(forgot_password("test_user", "abc123", "abc321"))         # ❌ không khớp

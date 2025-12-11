# Flask应用主入口
from flask import Flask, render_template
from routes.room_routes import room_bp
from routes.customer_routes import customer_bp
from routes.booking_routes import booking_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# 注册蓝图
app.register_blueprint(room_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(booking_bp)

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("🚀 启动酒店客房预订系统...")
        print("=" * 60)
        print(f"访问地址: http://localhost:5000")
        print(f"或访问: http://127.0.0.1:5000")
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except OSError as e:
        if "address already in use" in str(e).lower() or "10048" in str(e):
            print("\n❌ 端口5000已被占用！")
            print("\n解决方法：")
            print("1. 关闭占用端口的程序")
            print("2. 或修改端口号，在app.py中将5000改为其他端口（如5001）")
            print("\n查找占用端口的程序：")
            print("netstat -ano | findstr :5000")
        else:
            print(f"\n❌ 启动失败: {e}")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

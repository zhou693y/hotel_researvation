# 数据库配置
class Config:
    # KingbaseES数据库连接配置（兼容PostgreSQL）
    DB_HOST = 'localhost'
    DB_PORT = 54321  # KingbaseES默认端口
    DB_NAME = 'HOTEL_DB'
    DB_USER = 'SYSTEM'  # KingbaseES用户名大写
    DB_PASSWORD = '060903zhou'  # 修改为你的密码
    
    # Flask配置
    SECRET_KEY = '8b33c0ac7fd68d8d03c7705d75d648365d6269cb5484447624f88e1e5aeb400d'
    DEBUG = True

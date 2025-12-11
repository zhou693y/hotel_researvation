# 酒店客房预订系统

## 项目简介
基于KingbaseES数据库和Python Flask框架的酒店客房预订管理系统

## 技术栈
- 数据库: KingbaseES
- 后端: Python 3 + Flask
- 前端: HTML + CSS + JavaScript
- 数据库驱动: psycopg2

## 功能模块
1. 客房管理（增删改查）
2. 客户信息管理
3. 预订管理
4. 入住/退房管理
5. 查询统计

## 安装依赖
```bash
pip install -r requirements.txt
```

## 数据库配置
修改 `config.py` 中的数据库连接信息

## 运行项目
```bash
python app.py
```

访问: http://localhost:5000

## 项目结构
```
hotel-booking-system/
├── app.py              # 主应用入口
├── config.py           # 配置文件
├── requirements.txt    # 依赖包
├── database/
│   ├── init_db.py     # 数据库初始化
│   └── schema.sql     # 数据库表结构
├── models/
│   ├── room.py        # 客房模型
│   ├── customer.py    # 客户模型
│   └── booking.py     # 预订模型
├── routes/
│   ├── room_routes.py     # 客房路由
│   ├── customer_routes.py # 客户路由
│   └── booking_routes.py  # 预订路由
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    ├── index.html
    ├── rooms.html
    ├── customers.html
    └── bookings.html
```

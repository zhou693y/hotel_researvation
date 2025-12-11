# 客房模型
import psycopg2
from config import Config

class Room:
    @staticmethod
    def get_connection():
        """获取数据库连接"""
        return psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
    
    @staticmethod
    def get_all():
        """获取所有客房"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "ROOMS" ORDER BY "ROOM_NUMBER"')
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return rooms
    
    @staticmethod
    def get_by_id(room_id):
        """根据ID获取客房"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "ROOMS" WHERE "ROOM_ID" = %s', (room_id,))
        room = cursor.fetchone()
        cursor.close()
        conn.close()
        return room
    
    @staticmethod
    def create(room_number, room_type, price, floor_number, description):
        """创建新客房"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO "ROOMS" ("ROOM_NUMBER", "ROOM_TYPE", "PRICE", "FLOOR_NUMBER", "DESCRIPTION") VALUES (%s, %s, %s, %s, %s)',
            (room_number, room_type, price, floor_number, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def update(room_id, room_number, room_type, price, status, floor_number, description):
        """更新客房信息"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE "ROOMS" SET "ROOM_NUMBER"=%s, "ROOM_TYPE"=%s, "PRICE"=%s, "STATUS"=%s, "FLOOR_NUMBER"=%s, "DESCRIPTION"=%s WHERE "ROOM_ID"=%s',
            (room_number, room_type, price, status, floor_number, description, room_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(room_id):
        """删除客房"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "ROOMS" WHERE "ROOM_ID" = %s', (room_id,))
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def get_available_rooms():
        """获取空闲客房"""
        conn = Room.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "ROOMS" WHERE "STATUS" = \'空闲\' ORDER BY "ROOM_NUMBER"')
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return rooms

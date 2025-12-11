# 预订模型
import psycopg2
from config import Config

class Booking:
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
        """获取所有预订记录"""
        conn = Booking.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b."BOOKING_ID", c."NAME", r."ROOM_NUMBER", b."CHECK_IN_DATE", 
                   b."CHECK_OUT_DATE", b."STATUS", b."TOTAL_PRICE"
            FROM "BOOKINGS" b
            JOIN "CUSTOMERS" c ON b."CUSTOMER_ID" = c."CUSTOMER_ID"
            JOIN "ROOMS" r ON b."ROOM_ID" = r."ROOM_ID"
            ORDER BY b."BOOKING_ID" DESC
        """)
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
        return bookings
    
    @staticmethod
    def create(customer_id, room_id, check_in_date, check_out_date, total_price, remarks):
        """创建新预订"""
        conn = Booking.get_connection()
        cursor = conn.cursor()
        
        # 插入预订记录
        cursor.execute(
            'INSERT INTO "BOOKINGS" ("CUSTOMER_ID", "ROOM_ID", "CHECK_IN_DATE", "CHECK_OUT_DATE", "TOTAL_PRICE", "REMARKS") VALUES (%s, %s, %s, %s, %s, %s)',
            (customer_id, room_id, check_in_date, check_out_date, total_price, remarks)
        )
        
        # 更新房间状态
        cursor.execute('UPDATE "ROOMS" SET "STATUS" = \'已预订\' WHERE "ROOM_ID" = %s', (room_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def check_in(booking_id):
        """办理入住"""
        conn = Booking.get_connection()
        cursor = conn.cursor()
        
        # 更新预订状态
        cursor.execute('UPDATE "BOOKINGS" SET "STATUS" = \'已入住\' WHERE "BOOKING_ID" = %s', (booking_id,))
        
        # 获取房间ID并更新房间状态
        cursor.execute('SELECT "ROOM_ID" FROM "BOOKINGS" WHERE "BOOKING_ID" = %s', (booking_id,))
        room_id = cursor.fetchone()[0]
        cursor.execute('UPDATE "ROOMS" SET "STATUS" = \'已入住\' WHERE "ROOM_ID" = %s', (room_id,))
        
        # 插入入住记录
        cursor.execute(
            'INSERT INTO "CHECK_IN_RECORDS" ("BOOKING_ID", "ACTUAL_CHECK_IN") VALUES (%s, CURRENT_TIMESTAMP)',
            (booking_id,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def check_out(booking_id, actual_amount, payment_method):
        """办理退房"""
        conn = Booking.get_connection()
        cursor = conn.cursor()
        
        # 更新预订状态
        cursor.execute('UPDATE "BOOKINGS" SET "STATUS" = \'已退房\' WHERE "BOOKING_ID" = %s', (booking_id,))
        
        # 获取房间ID并更新房间状态
        cursor.execute('SELECT "ROOM_ID" FROM "BOOKINGS" WHERE "BOOKING_ID" = %s', (booking_id,))
        room_id = cursor.fetchone()[0]
        cursor.execute('UPDATE "ROOMS" SET "STATUS" = \'空闲\' WHERE "ROOM_ID" = %s', (room_id,))
        
        # 更新入住记录
        cursor.execute(
            'UPDATE "CHECK_IN_RECORDS" SET "ACTUAL_CHECK_OUT" = CURRENT_TIMESTAMP, "ACTUAL_AMOUNT" = %s, "PAYMENT_METHOD" = %s WHERE "BOOKING_ID" = %s',
            (actual_amount, payment_method, booking_id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def cancel(booking_id):
        """取消预订"""
        conn = Booking.get_connection()
        cursor = conn.cursor()
        
        # 更新预订状态
        cursor.execute('UPDATE "BOOKINGS" SET "STATUS" = \'已取消\' WHERE "BOOKING_ID" = %s', (booking_id,))
        
        # 获取房间ID并更新房间状态
        cursor.execute('SELECT "ROOM_ID" FROM "BOOKINGS" WHERE "BOOKING_ID" = %s', (booking_id,))
        room_id = cursor.fetchone()[0]
        cursor.execute('UPDATE "ROOMS" SET "STATUS" = \'空闲\' WHERE "ROOM_ID" = %s', (room_id,))
        
        conn.commit()
        cursor.close()
        conn.close()

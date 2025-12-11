# 客户模型
import psycopg2
from config import Config

class Customer:
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
        """获取所有客户"""
        conn = Customer.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "CUSTOMERS" ORDER BY "CUSTOMER_ID" DESC')
        customers = cursor.fetchall()
        cursor.close()
        conn.close()
        return customers
    
    @staticmethod
    def get_by_id(customer_id):
        """根据ID获取客户"""
        conn = Customer.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "CUSTOMERS" WHERE "CUSTOMER_ID" = %s', (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        return customer
    
    @staticmethod
    def create(name, id_card, phone, email, gender):
        """创建新客户"""
        conn = Customer.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO "CUSTOMERS" ("NAME", "ID_CARD", "PHONE", "EMAIL", "GENDER") VALUES (%s, %s, %s, %s, %s)',
            (name, id_card, phone, email, gender)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def update(customer_id, name, id_card, phone, email, gender):
        """更新客户信息"""
        conn = Customer.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE "CUSTOMERS" SET "NAME"=%s, "ID_CARD"=%s, "PHONE"=%s, "EMAIL"=%s, "GENDER"=%s WHERE "CUSTOMER_ID"=%s',
            (name, id_card, phone, email, gender, customer_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete(customer_id):
        """删除客户"""
        conn = Customer.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "CUSTOMERS" WHERE "CUSTOMER_ID" = %s', (customer_id,))
        conn.commit()
        cursor.close()
        conn.close()

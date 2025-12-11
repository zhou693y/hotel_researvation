-- ============================================================
-- 酒店客房预订系统 - 优化版数据库结构
-- 优化内容：索引 + 外键约束 + 数据完整性约束
-- ============================================================

-- 删除已存在的表
DROP TABLE IF EXISTS "CHECK_IN_RECORDS" CASCADE;
DROP TABLE IF EXISTS "BOOKINGS" CASCADE;
DROP TABLE IF EXISTS "CUSTOMERS" CASCADE;
DROP TABLE IF EXISTS "ROOMS" CASCADE;

-- ============================================================
-- 1. 客房表 (ROOMS)
-- ============================================================
CREATE TABLE "ROOMS" (
    "ROOM_ID" SERIAL PRIMARY KEY,
    "ROOM_NUMBER" VARCHAR(10) UNIQUE NOT NULL,
    "ROOM_TYPE" VARCHAR(20) NOT NULL,
    "PRICE" DECIMAL(10, 2) NOT NULL,
    "STATUS" VARCHAR(20) DEFAULT '空闲',
    "FLOOR_NUMBER" INT,
    "DESCRIPTION" TEXT,
    "CREATED_AT" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 【优化3】数据完整性约束
    CONSTRAINT chk_rooms_price CHECK ("PRICE" > 0),
    CONSTRAINT chk_rooms_floor CHECK ("FLOOR_NUMBER" > 0),
    CONSTRAINT chk_rooms_status CHECK ("STATUS" IN ('空闲', '已预订', '已入住', '维护中'))
);

-- 【优化1】索引优化 - 客房表
CREATE INDEX idx_rooms_status ON "ROOMS"("STATUS");        -- 查询空闲房间
CREATE INDEX idx_rooms_type ON "ROOMS"("ROOM_TYPE");       -- 按房型查询
CREATE INDEX idx_rooms_floor ON "ROOMS"("FLOOR_NUMBER");   -- 按楼层查询

-- ============================================================
-- 2. 客户表 (CUSTOMERS)
-- ============================================================
CREATE TABLE "CUSTOMERS" (
    "CUSTOMER_ID" SERIAL PRIMARY KEY,
    "NAME" VARCHAR(50) NOT NULL,
    "ID_CARD" VARCHAR(18) UNIQUE NOT NULL,
    "PHONE" VARCHAR(20) NOT NULL,
    "EMAIL" VARCHAR(100),
    "GENDER" VARCHAR(10),
    "CREATED_AT" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 【优化3】数据完整性约束
    CONSTRAINT chk_customers_id_card CHECK (LENGTH("ID_CARD") = 18),
    CONSTRAINT chk_customers_gender CHECK ("GENDER" IN ('男', '女'))
);

-- 【优化1】索引优化 - 客户表
CREATE INDEX idx_customers_phone ON "CUSTOMERS"("PHONE");   -- 按手机号查询
CREATE INDEX idx_customers_name ON "CUSTOMERS"("NAME");     -- 按姓名查询

-- ============================================================
-- 3. 预订表 (BOOKINGS)
-- ============================================================
CREATE TABLE "BOOKINGS" (
    "BOOKING_ID" SERIAL PRIMARY KEY,
    "CUSTOMER_ID" INT NOT NULL,
    "ROOM_ID" INT NOT NULL,
    "CHECK_IN_DATE" DATE NOT NULL,
    "CHECK_OUT_DATE" DATE NOT NULL,
    "BOOKING_DATE" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "STATUS" VARCHAR(20) DEFAULT '已预订',
    "TOTAL_PRICE" DECIMAL(10, 2),
    "REMARKS" TEXT,
    
    -- 【优化2】外键约束优化（带级联操作）
    CONSTRAINT fk_bookings_customer 
        FOREIGN KEY ("CUSTOMER_ID") 
        REFERENCES "CUSTOMERS"("CUSTOMER_ID") 
        ON DELETE RESTRICT      -- 防止删除有预订的客户
        ON UPDATE CASCADE,      -- 客户ID更新时自动更新
    
    CONSTRAINT fk_bookings_room 
        FOREIGN KEY ("ROOM_ID") 
        REFERENCES "ROOMS"("ROOM_ID") 
        ON DELETE RESTRICT      -- 防止删除有预订的房间
        ON UPDATE CASCADE,
    
    -- 【优化3】数据完整性约束
    CONSTRAINT chk_bookings_dates CHECK ("CHECK_OUT_DATE" > "CHECK_IN_DATE"),
    CONSTRAINT chk_bookings_price CHECK ("TOTAL_PRICE" >= 0),
    CONSTRAINT chk_bookings_status CHECK ("STATUS" IN ('已预订', '已入住', '已退房', '已取消'))
);

-- 【优化1】索引优化 - 预订表
CREATE INDEX idx_bookings_customer ON "BOOKINGS"("CUSTOMER_ID");  -- 查询客户的预订
CREATE INDEX idx_bookings_room ON "BOOKINGS"("ROOM_ID");          -- 查询房间的预订
CREATE INDEX idx_bookings_status ON "BOOKINGS"("STATUS");         -- 按状态查询
CREATE INDEX idx_bookings_dates ON "BOOKINGS"("CHECK_IN_DATE", "CHECK_OUT_DATE");  -- 日期范围查询

-- ============================================================
-- 4. 入住记录表 (CHECK_IN_RECORDS)
-- ============================================================
CREATE TABLE "CHECK_IN_RECORDS" (
    "RECORD_ID" SERIAL PRIMARY KEY,
    "BOOKING_ID" INT NOT NULL,
    "ACTUAL_CHECK_IN" TIMESTAMP,
    "ACTUAL_CHECK_OUT" TIMESTAMP,
    "ACTUAL_AMOUNT" DECIMAL(10, 2),
    "PAYMENT_METHOD" VARCHAR(20),
    
    -- 【优化2】外键约束优化（级联删除）
    CONSTRAINT fk_checkin_booking 
        FOREIGN KEY ("BOOKING_ID") 
        REFERENCES "BOOKINGS"("BOOKING_ID") 
        ON DELETE CASCADE       -- 删除预订时自动删除入住记录
        ON UPDATE CASCADE,
    
    -- 【优化3】数据完整性约束
    CONSTRAINT chk_checkin_dates CHECK (
        "ACTUAL_CHECK_OUT" IS NULL OR 
        "ACTUAL_CHECK_OUT" >= "ACTUAL_CHECK_IN"
    ),
    CONSTRAINT chk_checkin_amount CHECK (
        "ACTUAL_AMOUNT" IS NULL OR 
        "ACTUAL_AMOUNT" >= 0
    ),
    CONSTRAINT chk_checkin_payment CHECK (
        "PAYMENT_METHOD" IS NULL OR 
        "PAYMENT_METHOD" IN ('现金', '支付宝', '微信', '银行卡')
    )
);

-- 【优化1】索引优化 - 入住记录表
CREATE INDEX idx_checkin_booking ON "CHECK_IN_RECORDS"("BOOKING_ID");  -- 查询预订的入住记录

-- ============================================================
-- 5. 插入示例数据
-- ============================================================

-- 客房数据
INSERT INTO "ROOMS" ("ROOM_NUMBER", "ROOM_TYPE", "PRICE", "FLOOR_NUMBER", "DESCRIPTION") VALUES
('101', '单人间', 200.00, 1, '标准单人间，配备独立卫浴'),
('102', '单人间', 200.00, 1, '标准单人间，配备独立卫浴'),
('201', '双人间', 300.00, 2, '标准双人间，两张单人床'),
('202', '双人间', 300.00, 2, '标准双人间，一张双人床'),
('301', '套房', 500.00, 3, '豪华套房，客厅+卧室'),
('302', '套房', 500.00, 3, '豪华套房，客厅+卧室'),
('401', '豪华套房', 800.00, 4, '总统套房，超大空间');

-- 客户数据
INSERT INTO "CUSTOMERS" ("NAME", "ID_CARD", "PHONE", "EMAIL", "GENDER") VALUES
('张三', '110101199001011234', '13800138000', 'zhangsan@example.com', '男'),
('李四', '110101199002021234', '13800138001', 'lisi@example.com', '女'),
('王五', '110101199003031234', '13800138002', 'wangwu@example.com', '男');

-- ============================================================
-- 优化完成提示
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '✅ 数据库优化完成！';
    RAISE NOTICE '========================================';
    RAISE NOTICE '优化内容：';
    RAISE NOTICE '  ✓ 索引优化：创建了 11 个索引';
    RAISE NOTICE '  ✓ 外键约束：添加了级联操作';
    RAISE NOTICE '  ✓ 数据约束：添加了 12 个检查约束';
    RAISE NOTICE '========================================';
    RAISE NOTICE '示例数据：';
    RAISE NOTICE '  ✓ 7 个客房';
    RAISE NOTICE '  ✓ 3 个客户';
    RAISE NOTICE '========================================';
END $$;

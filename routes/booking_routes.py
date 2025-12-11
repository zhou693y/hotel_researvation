# 预订路由
from flask import Blueprint, render_template, request, jsonify
from models.booking import Booking
from models.room import Room
from models.customer import Customer

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/bookings')
def bookings():
    """预订管理页面"""
    return render_template('bookings.html')

@booking_bp.route('/api/bookings', methods=['GET'])
def get_bookings():
    """获取所有预订"""
    try:
        bookings = Booking.get_all()
        bookings_list = []
        for booking in bookings:
            bookings_list.append({
                'booking_id': booking[0],
                'customer_name': booking[1],
                'room_number': booking[2],
                'check_in_date': str(booking[3]),
                'check_out_date': str(booking[4]),
                'status': booking[5],
                'total_price': float(booking[6]) if booking[6] else 0
            })
        return jsonify({'success': True, 'data': bookings_list})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/bookings', methods=['POST'])
def create_booking():
    """创建预订"""
    try:
        data = request.json
        print(f"收到预订数据: {data}")  # 调试日志
        Booking.create(
            data['customer_id'],
            data['room_id'],
            data['check_in_date'],
            data['check_out_date'],
            data['total_price'],
            data.get('remarks', '')
        )
        return jsonify({'success': True, 'message': '预订创建成功'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/bookings/<int:booking_id>/checkin', methods=['POST'])
def check_in(booking_id):
    """办理入住"""
    try:
        Booking.check_in(booking_id)
        return jsonify({'success': True, 'message': '入住办理成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/bookings/<int:booking_id>/checkout', methods=['POST'])
def check_out(booking_id):
    """办理退房"""
    try:
        data = request.json
        Booking.check_out(
            booking_id,
            data['actual_amount'],
            data['payment_method']
        )
        return jsonify({'success': True, 'message': '退房办理成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """取消预订"""
    try:
        Booking.cancel(booking_id)
        return jsonify({'success': True, 'message': '预订取消成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/available-rooms', methods=['GET'])
def get_available_rooms():
    """获取空闲客房"""
    try:
        rooms = Room.get_available_rooms()
        rooms_list = []
        for room in rooms:
            rooms_list.append({
                'room_id': room[0],
                'room_number': room[1],
                'room_type': room[2],
                'price': float(room[3])
            })
        return jsonify({'success': True, 'data': rooms_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@booking_bp.route('/api/all-customers', methods=['GET'])
def get_all_customers():
    """获取所有客户（用于下拉选择）"""
    try:
        customers = Customer.get_all()
        customers_list = []
        for customer in customers:
            customers_list.append({
                'customer_id': customer[0],
                'name': customer[1],
                'phone': customer[3]
            })
        return jsonify({'success': True, 'data': customers_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

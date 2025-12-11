# 客户路由
from flask import Blueprint, render_template, request, jsonify
from models.customer import Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers')
def customers():
    """客户管理页面"""
    return render_template('customers.html')

@customer_bp.route('/api/customers', methods=['GET'])
def get_customers():
    """获取所有客户"""
    try:
        customers = Customer.get_all()
        customers_list = []
        for customer in customers:
            customers_list.append({
                'customer_id': customer[0],
                'name': customer[1],
                'id_card': customer[2],
                'phone': customer[3],
                'email': customer[4],
                'gender': customer[5]
            })
        return jsonify({'success': True, 'data': customers_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@customer_bp.route('/api/customers', methods=['POST'])
def create_customer():
    """创建客户"""
    try:
        data = request.json
        Customer.create(
            data['name'],
            data['id_card'],
            data['phone'],
            data.get('email', ''),
            data.get('gender', '')
        )
        return jsonify({'success': True, 'message': '客户创建成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@customer_bp.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """更新客户"""
    try:
        data = request.json
        Customer.update(
            customer_id,
            data['name'],
            data['id_card'],
            data['phone'],
            data.get('email', ''),
            data.get('gender', '')
        )
        return jsonify({'success': True, 'message': '客户更新成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@customer_bp.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """删除客户"""
    try:
        Customer.delete(customer_id)
        return jsonify({'success': True, 'message': '客户删除成功'})
    except Exception as e:
        error_msg = str(e)
        if 'BOOKINGS_CUSTOMER_ID_FKEY' in error_msg or '外键约束' in error_msg:
            return jsonify({'success': False, 'message': '无法删除：该客户有预订记录，请先删除相关预订'})
        return jsonify({'success': False, 'message': f'删除失败：{error_msg}'})

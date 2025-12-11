# 客房路由
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models.room import Room

room_bp = Blueprint('room', __name__)

@room_bp.route('/rooms')
def rooms():
    """客房管理页面"""
    return render_template('rooms.html')

@room_bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    """获取所有客房"""
    try:
        rooms = Room.get_all()
        rooms_list = []
        for room in rooms:
            rooms_list.append({
                'room_id': room[0],
                'room_number': room[1],
                'room_type': room[2],
                'price': float(room[3]),
                'status': room[4],
                'floor_number': room[5],
                'description': room[6]
            })
        return jsonify({'success': True, 'data': rooms_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@room_bp.route('/api/rooms', methods=['POST'])
def create_room():
    """创建客房"""
    try:
        data = request.json
        Room.create(
            data['room_number'],
            data['room_type'],
            data['price'],
            data['floor_number'],
            data.get('description', '')
        )
        return jsonify({'success': True, 'message': '客房创建成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@room_bp.route('/api/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    """更新客房"""
    try:
        data = request.json
        Room.update(
            room_id,
            data['room_number'],
            data['room_type'],
            data['price'],
            data['status'],
            data['floor_number'],
            data.get('description', '')
        )
        return jsonify({'success': True, 'message': '客房更新成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@room_bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    """删除客房"""
    try:
        Room.delete(room_id)
        return jsonify({'success': True, 'message': '客房删除成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

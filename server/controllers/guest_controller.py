from flask import Blueprint, jsonify, request
from ..models.guest import Guest
from ..app import db
from sqlalchemy import or_

guest_bp = Blueprint('guests', __name__)

@guest_bp.route('/guests', methods=['GET'])
def get_guests():
    try:
        # Get query parameters
        search = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'name')
        order = request.args.get('order', 'asc')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Validate parameters
        if per_page > 100:
            return jsonify({'error': 'Maximum per_page is 100'}), 400
        
        if sort_by not in ['name', 'occupation']:
            return jsonify({'error': 'Invalid sort_by parameter'}), 400
        
        if order not in ['asc', 'desc']:
            return jsonify({'error': 'Invalid order parameter'}), 400

        # Build query
        query = Guest.query

        # Apply search if provided
        if search:
            query = query.filter(
                or_(
                    Guest.name.ilike(f'%{search}%'),
                    Guest.occupation.ilike(f'%{search}%')
                )
            )

        # Apply sorting
        if order == 'asc':
            query = query.order_by(getattr(Guest, sort_by).asc())
        else:
            query = query.order_by(getattr(Guest, sort_by).desc())

        # Paginate results
        guests = query.paginate(page=page, per_page=per_page, error_out=False)

        if not guests.items and page != 1:
            return jsonify({'error': 'Page not found'}), 404

        return jsonify({
            'guests': [
                {'id': g.id, 'name': g.name, 'occupation': g.occupation}
                for g in guests.items
            ],
            'pagination': {
                'total': guests.total,
                'pages': guests.pages,
                'current_page': guests.page,
                'per_page': guests.per_page
            }
        })

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 
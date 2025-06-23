from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..models.episode import Episode
from ..models.appearance import Appearance
from ..app import db
from sqlalchemy.exc import SQLAlchemyError

episode_bp = Blueprint('episodes', __name__)

@episode_bp.route('/episodes', methods=['GET'])
def get_episodes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if per_page > 100:
            return jsonify({'error': 'Maximum per_page is 100'}), 400

        episodes = Episode.query.paginate(page=page, per_page=per_page, error_out=False)
        
        if not episodes.items and page != 1:
            return jsonify({'error': 'Page not found'}), 404

        return jsonify({
            'episodes': [
                {'id': e.id, 'date': e.date.isoformat(), 'number': e.number}
                for e in episodes.items
            ],
            'pagination': {
                'total': episodes.total,
                'pages': episodes.pages,
                'current_page': episodes.page,
                'per_page': episodes.per_page
            }
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@episode_bp.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    try:
        episode = Episode.query.get_or_404(id)
        appearances = [
            {
                'id': a.id,
                'rating': a.rating,
                'guest': {
                    'id': a.guest.id,
                    'name': a.guest.name,
                    'occupation': a.guest.occupation
                }
            } for a in episode.appearances
        ]
        return jsonify({
            'id': episode.id,
            'date': episode.date.isoformat(),
            'number': episode.number,
            'appearances': appearances
        })
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@episode_bp.route('/episodes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_episode(id):
    try:
        episode = Episode.query.get_or_404(id)
        db.session.delete(episode)
        db.session.commit()
        return jsonify({
            'message': 'Episode deleted successfully',
            'deleted_episode': {
                'id': episode.id,
                'date': episode.date.isoformat(),
                'number': episode.number
            }
        })
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 
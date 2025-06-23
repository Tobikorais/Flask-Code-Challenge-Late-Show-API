from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.appearance import Appearance
from ..models.guest import Guest
from ..models.episode import Episode
from ..app import db
from sqlalchemy.exc import SQLAlchemyError

appearance_bp = Blueprint('appearances', __name__)

@appearance_bp.route('/appearances', methods=['POST'])
@jwt_required()
def create_appearance():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        # Validate required fields
        required_fields = ['rating', 'guest_id', 'episode_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        rating = data['rating']
        guest_id = data['guest_id']
        episode_id = data['episode_id']

        # Validate rating
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Rating must be a valid integer'}), 400

        # Check if guest exists
        guest = Guest.query.get(guest_id)
        if not guest:
            return jsonify({'error': 'Guest not found'}), 404

        # Check if episode exists
        episode = Episode.query.get(episode_id)
        if not episode:
            return jsonify({'error': 'Episode not found'}), 404

        # Check if appearance already exists
        existing_appearance = Appearance.query.filter_by(
            guest_id=guest_id,
            episode_id=episode_id
        ).first()
        if existing_appearance:
            return jsonify({'error': 'Guest already has an appearance in this episode'}), 409

        try:
            appearance = Appearance(
                rating=rating,
                guest_id=guest_id,
                episode_id=episode_id
            )
            db.session.add(appearance)
            db.session.commit()

            return jsonify({
                'message': 'Appearance created successfully',
                'appearance': {
                    'id': appearance.id,
                    'rating': appearance.rating,
                    'guest_id': appearance.guest_id,
                    'episode_id': appearance.episode_id,
                    'guest': {
                        'id': guest.id,
                        'name': guest.name,
                        'occupation': guest.occupation
                    }
                }
            }), 201

        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500 
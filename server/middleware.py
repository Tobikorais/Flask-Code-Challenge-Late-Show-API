from functools import wraps
from flask import request, jsonify
import json

def validate_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415
        
        try:
            if request.data:
                json.loads(request.data)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format'}), 400
            
        return f(*args, **kwargs)
    return decorated_function

def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No JSON data provided'}), 400

                missing_fields = [field for field in schema if field not in data]
                if missing_fields:
                    return jsonify({
                        'error': 'Missing required fields',
                        'fields': missing_fields
                    }), 400

                extra_fields = [field for field in data if field not in schema]
                if extra_fields:
                    return jsonify({
                        'error': 'Unknown fields provided',
                        'fields': extra_fields
                    }), 400

                for field, field_type in schema.items():
                    if not isinstance(data[field], field_type):
                        return jsonify({
                            'error': f'Invalid type for field {field}',
                            'expected': field_type.__name__,
                            'received': type(data[field]).__name__
                        }), 400

            except Exception as e:
                return jsonify({'error': str(e)}), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            data = request.get_json()
            if isinstance(data, dict):
                sanitized = {
                    k: v.strip() if isinstance(v, str) else v
                    for k, v in data.items()
                }
                request._cached_json = (sanitized, request._cached_json[1])
        return f(*args, **kwargs)
    return decorated_function 
from flask import Blueprint
from app.api import auth, donations, organizations, admin

def register_routes(app):
    """Register all application routes"""
    
    # API routes
    api = Blueprint('api', __name__, url_prefix='/api')
    
    # Register individual API blueprints
    api.register_blueprint(auth.bp, url_prefix='/auth')
    api.register_blueprint(donations.bp, url_prefix='/donations')
    api.register_blueprint(organizations.bp, url_prefix='/organizations')
    api.register_blueprint(admin.bp, url_prefix='/admin')
    
    # Register the main API blueprint
    app.register_blueprint(api)
    
    # Register error handlers
    register_error_handlers(app)

def register_error_handlers(app):
    """Register error handlers for common HTTP errors"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return {'error': 'Bad Request', 'message': str(error)}, 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return {'error': 'Unauthorized', 'message': 'Authentication required'}, 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Forbidden', 'message': 'Insufficient permissions'}, 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Not Found', 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return {'error': 'Internal Server Error', 'message': 'An unexpected error occurred'}, 500
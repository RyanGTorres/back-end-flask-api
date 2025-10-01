from flask import Flask, jsonify


def register_errors(app):

    @app.errorhandler(Exception)
    def handle_custom_error(e):
        response = {
            "status": "error",
            "message": str(e)
        }
        return response, 400

    @app.errorhandler(404)
    def handle_404_error(e):
        response = {
            "status": "error",
            "message": "Resource not found"
        }
        return response, 404

    @app.errorhandler(500)
    def handle_500_error(e):
        response = {
            "status": "error",
            "message": "Internal server error"
        }
        return response, 500

    
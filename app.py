from flask import Flask, jsonify, request
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

# Store build status
builds = {}
build_counter = 0

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "IPA Build Server",
        "version": "1.0.0"
    })

@app.route("/api/test")
def test():
    return jsonify({
        "message": "hello",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/builds", methods=["GET"])
def list_builds():
    """List all builds"""
    return jsonify({
        "builds": builds,
        "total": len(builds)
    })

@app.route("/api/build/<build_id>", methods=["GET"])
def get_build(build_id):
    """Get specific build status"""
    if build_id not in builds:
        return jsonify({"error": "Build not found"}), 404
    return jsonify(builds[build_id])

@app.route("/api/build/trigger", methods=["POST"])
def trigger_build():
    """Trigger a new IPA build"""
    global build_counter
    
    try:
        data = request.json or {}
        scheme = data.get("scheme", "YourAppScheme")
        configuration = data.get("configuration", "Release")
        
        build_counter += 1
        build_id = f"build-{build_counter}"
        
        builds[build_id] = {
            "id": build_id,
            "status": "pending",
            "scheme": scheme,
            "configuration": configuration,
            "created_at": datetime.now().isoformat(),
            "log": []
        }
        
        # In production, this would trigger GitHub Actions via API
        # For now, we'll simulate the build
        builds[build_id]["status"] = "running"
        builds[build_id]["log"].append("Build started...")
        
        return jsonify({
            "message": "Build triggered",
            "build_id": build_id,
            "status": builds[build_id]["status"]
        }), 202
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/build/<build_id>/cancel", methods=["POST"])
def cancel_build(build_id):
    """Cancel a running build"""
    if build_id not in builds:
        return jsonify({"error": "Build not found"}), 404
    
    if builds[build_id]["status"] in ["completed", "failed", "cancelled"]:
        return jsonify({"error": "Cannot cancel completed build"}), 400
    
    builds[build_id]["status"] = "cancelled"
    builds[build_id]["log"].append("Build cancelled by user")
    
    return jsonify({
        "message": "Build cancelled",
        "build_id": build_id
    })

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_builds": len([b for b in builds.values() if b["status"] == "running"])
    })

@app.route("/api/config", methods=["GET"])
def get_config():
    """Get build configuration"""
    return jsonify({
        "schemes": ["YourAppScheme"],
        "configurations": ["Debug", "Release"],
        "export_methods": ["app-store", "ad-hoc", "enterprise", "development"]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

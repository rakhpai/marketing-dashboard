#!/usr/bin/env python3
"""
Simple webhook server for GitHub webhooks.
This server listens for push events from GitHub and triggers the deployment script.
"""

import http.server
import socketserver
import json
import subprocess
import os
import hmac
import hashlib
import logging
from datetime import datetime

# Configuration
PORT = 9876  # Custom port for webhook server
DEPLOY_SCRIPT = "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/deploy.sh"
LOG_FILE = "/var/www/vhosts/fgtwelve.ltd/httpdocs/marketing/deploy/webhook.log"
SECRET_TOKEN = os.environ.get("WEBHOOK_SECRET", "")  # Set this to match your GitHub webhook secret
BRANCH = "master"  # The branch to deploy

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("webhook")

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="text/plain"):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests - just return a simple message"""
        self._set_response()
        self.wfile.write("Webhook server is running".encode('utf-8'))

    def do_POST(self):
        """Handle POST requests from GitHub"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Verify GitHub signature if a secret token is set
        if SECRET_TOKEN:
            signature = self.headers.get('X-Hub-Signature-256')
            if not signature:
                logger.warning("No signature provided")
                self._set_response(403)
                self.wfile.write("No signature provided".encode('utf-8'))
                return

            if not self._verify_signature(post_data, signature):
                logger.warning("Invalid signature")
                self._set_response(403)
                self.wfile.write("Invalid signature".encode('utf-8'))
                return

        # Parse the JSON payload
        try:
            payload = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            self._set_response(400)
            self.wfile.write("Invalid JSON payload".encode('utf-8'))
            return

        # Check if this is a push event
        event_type = self.headers.get('X-GitHub-Event')
        if event_type != 'push':
            logger.info(f"Received non-push event: {event_type}")
            self._set_response()
            self.wfile.write(f"Received {event_type} event, ignoring".encode('utf-8'))
            return

        # Check if this is for the branch we want to deploy
        ref = payload.get('ref')
        if ref != f"refs/heads/{BRANCH}":
            logger.info(f"Received push event for {ref}, ignoring")
            self._set_response()
            self.wfile.write(f"Received push event for {ref}, ignoring".encode('utf-8'))
            return

        # All checks passed, trigger deployment
        logger.info(f"Received push event for {BRANCH}, triggering deployment")
        self._set_response()
        self.wfile.write(f"Received push event for {BRANCH}, triggering deployment".encode('utf-8'))

        # Run the deployment script
        try:
            subprocess.Popen([DEPLOY_SCRIPT], shell=True)
            logger.info("Deployment script started")
        except Exception as e:
            logger.error(f"Error running deployment script: {e}")

    def _verify_signature(self, payload, signature):
        """Verify the GitHub signature"""
        if not signature.startswith('sha256='):
            return False

        received_signature = signature[7:]  # Remove 'sha256=' prefix
        computed_signature = hmac.new(
            SECRET_TOKEN.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(received_signature, computed_signature)

def run_server():
    """Run the webhook server"""
    with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
        logger.info(f"Starting webhook server on port {PORT}")
        print(f"Starting webhook server on port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
            print("Server stopped by user")
        finally:
            httpd.server_close()
            logger.info("Server closed")
            print("Server closed")

if __name__ == "__main__":
    # Create log directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    run_server()

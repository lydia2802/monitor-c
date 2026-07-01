"""
Entry point for the Unified Monitoring Dashboard.

Starts the Flask REST API together with the web dashboard (served at /dashboard)
on a single host/port. Search results are written to the local SQLite database
under data/, so the dashboard keeps working offline once data has been collected.

Usage:
    python run_dashboard.py [--host 0.0.0.0] [--port 5000] [--debug]
"""

import argparse

from pegasus.api.server import start_api_server


def main():
    parser = argparse.ArgumentParser(description="Run the unified monitoring dashboard")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Run Flask in debug/reload mode")
    args = parser.parse_args()

    start_api_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()

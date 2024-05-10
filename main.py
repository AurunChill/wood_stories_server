# Third-party
import uvicorn

# Project
from server import app

# Standard
import argparse

def main():
    """Main function that runs the app on specified port in debug mode"""
    parser = argparse.ArgumentParser(description="Run the app on a specified port")
    parser.add_argument("--port", '-p', type=int, default=5051, help="Port number to run the app on")
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == '__main__':
    main()
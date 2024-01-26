from .server import server

if __name__ == "__main__":
    server.run(debug=True, port=5000, host="0.0.0.0")

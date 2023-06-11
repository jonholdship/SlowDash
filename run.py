from app.app import app
import yaml


# Run the app
if __name__ == "__main__":
    app.run(dev_tools_hot_reload=False)

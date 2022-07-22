from flask import Blueprint
from flask import send_from_directory

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def main():
    return send_from_directory('../todoist-frontend/build', 'index.html')


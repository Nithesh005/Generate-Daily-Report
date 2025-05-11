import sys
sys.path.append(r'D:\Domain\Automate\py')

from git_data import send_report
from git_data import app  # Make sure `app = Flask(__name__)` exists

with app.app_context():
    send_report()
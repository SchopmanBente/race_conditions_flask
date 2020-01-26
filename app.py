from flask import Flask, make_response, send_file, Response, render_template
from flask_bootstrap import Bootstrap
from app.models import MyResponse



def page_not_found(e):
  return render_template('404.html'), 404

def create_app(config_filename):
    app = Flask(__name__, template_folder='../templates')
    app.response_class = MyResponse

    app.debug = True
    app.register_error_handler(404, page_not_found)

    bootstrap = Bootstrap(app)
    return bootstrap

__name__ == "__main__":
 app = create_app(None)
 app.run()
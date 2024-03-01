from flask import Flask,render_template,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.user import bp as user_bp
from blueprints.segmentation import bp as seg_bp
from flask_migrate import Migrate


app = Flask(__name__)
#绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(user_bp)
app.register_blueprint(seg_bp)

#flask db init 转化为数据库表
#flask db migrate
#flask db upgrade


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = db.session.get(UserModel,user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)


@app.context_processor
def my_context_processor():
    return {"user":g.user}



if __name__ == '__main__':
    app.run(debug=True)

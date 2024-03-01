#配置相关


SECRET_KEY = "ASDASVBNKJZVBNKZXJ"#随便设置

#连接数据库
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = '#'#数据库名
USERNAME = '#'#用户名
PASSWORD = '#'#密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

#邮箱配置

MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "#"#发送验证码邮件邮箱
MAIL_PASSWORD = "#"#smtp码
MAIL_DEFAULT_SENDER = "#"#邮箱地址相同
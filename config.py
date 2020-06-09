class Config:
    SECRET_KEY = '4iko42k24pk'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///eda.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'sha512_crypt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False


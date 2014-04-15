SQLALCHEMY_BINDS = \
    {
        "blog": "sqlite:///db/blog.db",
        "spells": "sqlite:///db/spells.db"
    }

CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-key'
class RedmineRouter(object):
    """A router to control all database operations on models in
    the redmine application"""

    def db_for_read(self, model, **hints):
        "Point all operations on redmine models to 'redmine'"
        if model._meta.app_label == 'redmine':
            return 'redmine'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on redmine models to 'redmine'"
        if model._meta.app_label == 'redmine':
            return 'redmine'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in Redmine is involved"
        if obj1._meta.app_label == 'redmine' or \
           obj2._meta.app_label == 'redmine':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the redmine app only appears on the 'redmine' db"
        if db == 'redmine':
            return model._meta.app_label == 'redmine'
        elif model._meta.app_label == 'redmine':
            return False
        return None

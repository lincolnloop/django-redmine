from django.contrib import databrowse
from django.conf.urls.defaults import *
from django.db.models import get_models

from redmine import models as redmine_models

m2m_through_models = (
    'CustomFieldsProject',
    'CustomFieldsTracker',
    'ProjectTracker',
    'ChangesetIssue',
)

for model in get_models(redmine_models):
    # register all but M2M through models
    if model.__name__ not in m2m_through_models:
        databrowse.site.register(model)

urlpatterns = patterns('',
    (r'^(.*)', databrowse.site.root),
)

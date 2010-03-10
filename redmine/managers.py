from django.db import models

class IssueManager(models.Manager):
    def open(self):
        return self.filter(status__is_closed=False)
    
    def closed(self):
        return self.filter(status__is_closed=True)
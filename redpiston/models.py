from django.db import models

from redpiston.utils import load_generic_object

class Attachment(models.Model):
    id = models.IntegerField(primary_key=True)
    container_id = models.IntegerField()
    container_type = models.CharField(max_length=30)
    filename = models.CharField(max_length=255)
    disk_filename = models.CharField(max_length=255)
    filesize = models.IntegerField()
    content_type = models.CharField(max_length=255)
    digest = models.CharField(max_length=40)
    downloads = models.IntegerField()
    author = models.ForeignKey("User")
    created_on = models.DateTimeField()
    description = models.CharField(max_length=255)
    class Meta:
        db_table = u'attachments'

    @property
    def container(self):
        return load_generic_object(self.container_type, self.container_id)

class AuthSource(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    host = models.CharField(max_length=60)
    port = models.IntegerField()
    account = models.CharField(max_length=255)
    account_password = models.CharField(max_length=60)
    base_dn = models.CharField(max_length=255)
    attr_login = models.CharField(max_length=30)
    attr_firstname = models.CharField(max_length=30)
    attr_lastname = models.CharField(max_length=30)
    attr_mail = models.CharField(max_length=30)
    onthefly_register = models.BooleanField()
    tls = models.BooleanField()
    class Meta:
        db_table = u'auth_sources'

class BacklogChartData(models.Model):
    id = models.IntegerField(primary_key=True)
    scope = models.IntegerField()
    done = models.IntegerField()
    wip = models.IntegerField()
    backlog = models.ForeignKey("Backlog")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = u'backlog_chart_data'
        

class Backlog(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey("Version")
    start_date = models.DateTimeField()
    is_closed = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    velocity = models.IntegerField()
    class Meta:
        db_table = u'backlogs'
        
    def __unicode__(self):
        return 'Backlog for %s' % (self.version)

class Board(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    position = models.IntegerField()
    topics_count = models.IntegerField()
    messages_count = models.IntegerField()
    last_message = models.ForeignKey("Message", related_name="last_message_on_board")
    class Meta:
        db_table = u'boards'

class Change(models.Model):
    id = models.IntegerField(primary_key=True)
    changeset = models.ForeignKey("Changeset")
    action = models.CharField(max_length=1)
    path = models.CharField(max_length=255)
    from_path = models.CharField(max_length=255)
    from_revision = models.CharField(max_length=255)
    revision = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    class Meta:
        db_table = u'changes'
        
    def __unicode__(self):
        return '%s: %s' % (self.action, self.path)

class Changeset(models.Model):
    id = models.IntegerField(primary_key=True)
    repository = models.ForeignKey("Repository")
    revision = models.CharField(max_length=255)
    committer = models.CharField(max_length=255)
    committed_on = models.DateTimeField()
    comments = models.TextField()
    commit_date = models.DateField()
    scmid = models.CharField(max_length=255)
    user = models.ForeignKey("User")
    issues = models.ManyToManyField("Issue", through="ChangesetIssue")
    class Meta:
        db_table = u'changesets'
        
    def __unicode__(self):
        return 'Revision %s on %s' % (self.revision, self.repository)
        
class ChangesetIssue(models.Model):
    changeset = models.ForeignKey("Changeset")
    issue = models.ForeignKey("Issue")
    class Meta:
        db_table = u'changesets_issues'


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    commented_type = models.CharField(max_length=30)
    commented_id = models.IntegerField()
    author = models.ForeignKey("User")
    comments = models.TextField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    class Meta:
        db_table = u'comments'

    @property
    def commented(self):
        return load_generic_object(self.commented_type, self.commented_id)


class CustomField(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    field_format = models.CharField(max_length=30)
    possible_values = models.TextField()
    regexp = models.CharField(max_length=255)
    min_length = models.IntegerField()
    max_length = models.IntegerField()
    is_required = models.BooleanField()
    is_for_all = models.BooleanField()
    is_filter = models.BooleanField()
    position = models.IntegerField()
    searchable = models.BooleanField()
    default_value = models.TextField()
    editable = models.BooleanField()
    projects = models.ManyToManyField("Project", through="CustomFieldsProject")
    trackers = models.ManyToManyField("Tracker", through="CustomFieldsTracker")
    class Meta:
        db_table = u'custom_fields'

class CustomFieldsProject(models.Model):
    custom_field = models.ForeignKey("CustomField")
    project = models.ForeignKey("Project")
    class Meta:
        db_table = u'custom_fields_projects'

class CustomFieldsTracker(models.Model):
    custom_field = models.ForeignKey("CustomField")
    tracker = models.ForeignKey("Tracker")
    class Meta:
        db_table = u'custom_fields_trackers'

class CustomValue(models.Model):
    id = models.IntegerField(primary_key=True)
    customized_type = models.CharField(max_length=30)
    customized_id = models.IntegerField()
    custom_field = models.ForeignKey("CustomField")
    value = models.TextField()
    class Meta:
        db_table = u'custom_values'

    @property
    def customized(self):
        return load_generic_object(self.customized_type, self.customized_id)


class Deliverable(models.Model):
    id = models.IntegerField(primary_key=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255)
    project_manager_signoff = models.BooleanField()
    client_signoff = models.BooleanField()
    project = models.ForeignKey("Project")
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    overhead = models.DecimalField(max_digits=15, decimal_places=2)
    materials = models.DecimalField(max_digits=15, decimal_places=2)
    profit = models.DecimalField(max_digits=15, decimal_places=2)
    cost_per_hour = models.DecimalField(max_digits=15, decimal_places=2)
    total_hours = models.DecimalField(max_digits=15, decimal_places=2)
    fixed_cost = models.DecimalField(max_digits=15, decimal_places=2)
    overhead_percent = models.IntegerField()
    materials_percent = models.IntegerField()
    profit_percent = models.IntegerField()
    due = models.DateField()
    class Meta:
        db_table = u'deliverables'

class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    category_id = models.IntegerField()
    title = models.CharField(max_length=60)
    description = models.TextField()
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'documents'

class EnabledModule(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'enabled_modules'

class Enumeration(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    position = models.IntegerField()
    is_default = models.BooleanField()
    type = models.CharField(max_length=255)
    active = models.BooleanField()
    project = models.ForeignKey("Project")
    parent = models.ForeignKey("self")
    class Meta:
        db_table = u'enumerations'

"""
# where is the group table?
class GroupsUsers(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    class Meta:
        db_table = u'groups_users'
"""

class Issue(models.Model):
    id = models.IntegerField(primary_key=True)
    tracker = models.ForeignKey("Tracker")
    project = models.ForeignKey("Project")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    category = models.ForeignKey("IssueCategory")
    status = models.ForeignKey("IssueStatus")
    assigned_to = models.ForeignKey("User", related_name="assigned_issues")
    priority_id = models.IntegerField()
    fixed_version_id = models.IntegerField()
    author = models.ForeignKey("User", related_name="created_issues")
    lock_version = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    start_date = models.DateField()
    done_ratio = models.IntegerField()
    estimated_hours = models.FloatField()
    deliverable = models.ForeignKey("Deliverable")
    parent = models.ForeignKey("self")
    lft = models.IntegerField()
    rgt = models.IntegerField()
    class Meta:
        db_table = u'issues'
        
    def __unicode__(self):
        return '%s: %s' % (self.tracker, self.subject)


class IssueCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    name = models.CharField(max_length=30)
    assigned_to = models.ForeignKey("User")
    class Meta:
        db_table = u'issue_categories'
        verbose_name_plural = "issue categories"
    
    def __unicode__(self):
        return self.name

class IssueRelation(models.Model):
    id = models.IntegerField(primary_key=True)
    issue_from_id = models.IntegerField()
    issue_to_id = models.IntegerField()
    relation_type = models.CharField(max_length=255)
    delay = models.IntegerField()
    class Meta:
        db_table = u'issue_relations'

class IssueStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    is_closed = models.BooleanField()
    is_default = models.BooleanField()
    position = models.IntegerField()
    default_done_ratio = models.IntegerField()
    class Meta:
        db_table = u'issue_statuses'
        verbose_name_plural = "issue statuses"
        ordering = ['position']
    
    def __unicode__(self):
        return self.name


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    issue = models.ForeignKey("Issue")
    backlog = models.ForeignKey("Backlog")
    position = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parent = models.ForeignKey("self")
    points = models.IntegerField()
    class Meta:
        db_table = u'items'
        
    def __unicode__(self):
        return 'Backlog Issue: %s' % (self.issue)

class JournalDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    journal = models.ForeignKey("Journal")
    property = models.CharField(max_length=30)
    prop_key = models.CharField(max_length=30)
    old_value = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    class Meta:
        db_table = u'journal_details'

class Journal(models.Model):
    id = models.IntegerField(primary_key=True)
    journalized_id = models.IntegerField()
    journalized_type = models.CharField(max_length=30)
    user = models.ForeignKey("User")
    notes = models.TextField()
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'journals'

    @property
    def journalized(self):
        return load_generic_object(self.journalized_type, self.journalized_id)


class MemberRole(models.Model):
    id = models.IntegerField(primary_key=True)
    member = models.ForeignKey("User")
    role = models.ForeignKey("Role")
    inherited_from = models.IntegerField()
    class Meta:
        db_table = u'member_roles'

class Member(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    project = models.ForeignKey("Project")
    created_on = models.DateTimeField()
    mail_notification = models.BooleanField()
    class Meta:
        db_table = u'members'

class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    board = models.ForeignKey("Board")
    parent = models.ForeignKey("self", related_name="children")
    subject = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey("User")
    replies_count = models.IntegerField()
    last_reply = models.ForeignKey("self", related_name="last_reply_on")
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    locked = models.BooleanField()
    sticky = models.IntegerField()
    class Meta:
        db_table = u'messages'

class NewsItem(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    title = models.CharField(max_length=60)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey("User")
    created_on = models.DateTimeField()
    comments_count = models.IntegerField()
    class Meta:
        db_table = u'news'

class OpenIdAuthenticationAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    handle = models.CharField(max_length=255)
    assoc_type = models.CharField(max_length=255)
    server_url = models.TextField() # This field type is a guess.
    secret = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'open_id_authentication_associations'

class OpenIdAuthenticationNonce(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.IntegerField()
    server_url = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    class Meta:
        db_table = u'open_id_authentication_nonces'
"""
class PluginSchemaInfo(models.Model):
    plugin_name = models.CharField(max_length=255)
    version = models.IntegerField()
    class Meta:
        db_table = u'plugin_schema_info'
"""
class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    homepage = models.CharField(max_length=255)
    is_public = models.BooleanField()
    parent = models.ForeignKey("self")
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    identifier = models.CharField(max_length=20)
    status = models.IntegerField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    trackers = models.ManyToManyField("Tracker", through="ProjectTracker") 
    class Meta:
        db_table = u'projects'
        
    def __unicode__(self):
        return self.name

class ProjectTracker(models.Model):
    project = models.ForeignKey("Project")
    tracker = models.ForeignKey("Tracker")
    class Meta:
        db_table = u'projects_trackers'

class Query(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    name = models.CharField(max_length=255)
    filters = models.TextField()
    user = models.ForeignKey("User")
    is_public = models.BooleanField()
    column_names = models.TextField()
    sort_criteria = models.TextField()
    group_by = models.CharField(max_length=255)
    view_options = models.TextField()
    class Meta:
        db_table = u'queries'
        verbose_name_plural = u'queries'

class Rate(models.Model):
    id = models.IntegerField(primary_key=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey("User")
    project = models.ForeignKey("Project")
    date_in_effect = models.DateField()
    class Meta:
        db_table = u'rates'

class Repository(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    url = models.CharField(max_length=255)
    login = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    root_url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    class Meta:
        db_table = u'repositories'
        verbose_name_plural = u'repositories'
        
    def __unicode__(self):
        return '%s repository for %s' % (self.type, self.project)

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    position = models.IntegerField()
    assignable = models.BooleanField()
    builtin = models.IntegerField()
    permissions = models.TextField()
    class Meta:
        db_table = u'roles'

class ScheduleClosedEntry(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    date = models.DateField()
    hours = models.FloatField()
    comment = models.TextField()
    class Meta:
        db_table = u'schedule_closed_entries'
        verbose_name_plural = u'schedule closed entries'

class ScheduleDefault(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    weekday_hours = models.TextField()
    class Meta:
        db_table = u'schedule_defaults'

class ScheduleEntry(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    project = models.ForeignKey("Project")
    date = models.DateField()
    hours = models.FloatField()
    class Meta:
        db_table = u'schedule_entries'
        verbose_name_plural = u'schedule entries'
"""
class SchemaMigrations(models.Model):
    version = models.CharField(unique=True, max_length=255)
    class Meta:
        db_table = u'schema_migrations'
"""

class Setting(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.TextField()
    updated_on = models.DateTimeField()
    class Meta:
        db_table = u'settings'

class StuffToDo(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    position = models.IntegerField()
    stuff_id = models.IntegerField()
    stuff_type = models.CharField(max_length=255)
    class Meta:
        db_table = u'stuff_to_dos'

    @property
    def stuff(self):
        return load_generic_object(self.stuff_type, self.stuff_id)


class TimeEntry(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    user = models.ForeignKey("User")
    issue = models.ForeignKey("Issue")
    hours = models.FloatField()
    comments = models.CharField(max_length=255)
    activity_id = models.IntegerField()
    spent_on = models.DateField()
    tyear = models.IntegerField()
    tmonth = models.IntegerField()
    tweek = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    rate = models.ForeignKey("Rate")
    class Meta:
        db_table = u'time_entries'
        verbose_name_plural = u'time entries'

class Token(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    action = models.CharField(max_length=30)
    value = models.CharField(max_length=40)
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'tokens'

class Tracker(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    is_in_chlog = models.BooleanField()
    position = models.IntegerField()
    is_in_roadmap = models.BooleanField()
    class Meta:
        db_table = u'trackers'
        ordering = ['position']
        
    def __unicode__(self):
        return self.name

class UserPreference(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey("User")
    others = models.TextField()
    hide_mail = models.BooleanField()
    time_zone = models.CharField(max_length=255)
    class Meta:
        db_table = u'user_preferences'

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=30)
    hashed_password = models.CharField(max_length=40)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    mail = models.CharField(max_length=60)
    mail_notification = models.BooleanField()
    admin = models.BooleanField()
    status = models.IntegerField()
    last_login_on = models.DateTimeField()
    language = models.CharField(max_length=5)
    auth_source_id = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    type = models.CharField(max_length=255)
    identity_url = models.CharField(max_length=255)
    class Meta:
        db_table = u'users'
    
    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname)

class Version(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    effective_date = models.DateField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    wiki_page_title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    sharing = models.CharField(max_length=255)
    class Meta:
        db_table = u'versions'
    
    def __unicode__(self):
        return '%s: %s' % (self.project, self.name)

class Watcher(models.Model):
    id = models.IntegerField(primary_key=True)
    watchable_type = models.CharField(max_length=255)
    watchable_id = models.IntegerField()
    user = models.ForeignKey("User")
    class Meta:
        db_table = u'watchers'

    @property
    def watchable(self):
        return load_generic_object(self.watchable_type, self.watchable_id)


class WikiContentVersion(models.Model):
    id = models.IntegerField(primary_key=True)
    wiki_content = models.ForeignKey("WikiContent")
    page = models.ForeignKey("WikiPage")
    author = models.ForeignKey("User")
    data = models.TextField() # This field type is a guess.
    compression = models.CharField(max_length=6)
    comments = models.CharField(max_length=255)
    updated_on = models.DateTimeField()
    version = models.IntegerField()
    class Meta:
        db_table = u'wiki_content_versions'

class WikiContent(models.Model):
    id = models.IntegerField(primary_key=True)
    page = models.ForeignKey("WikiPage")
    author = models.ForeignKey("User")
    text = models.TextField()
    comments = models.CharField(max_length=255)
    updated_on = models.DateTimeField()
    version = models.IntegerField()
    class Meta:
        db_table = u'wiki_contents'

class WikiPage(models.Model):
    id = models.IntegerField(primary_key=True)
    wiki = models.ForeignKey("Wiki")
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField()
    protected = models.BooleanField()
    parent = models.ForeignKey("self")
    class Meta:
        db_table = u'wiki_pages'

class WikiRedirect(models.Model):
    id = models.IntegerField(primary_key=True)
    wiki = models.ForeignKey("Wiki")
    title = models.CharField(max_length=255)
    redirects_to = models.CharField(max_length=255)
    created_on = models.DateTimeField()
    class Meta:
        db_table = u'wiki_redirects'

class Wiki(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey("Project")
    start_page = models.CharField(max_length=255)
    status = models.IntegerField()
    class Meta:
        db_table = u'wikis'

class Workflow(models.Model):
    id = models.IntegerField(primary_key=True)
    tracker = models.ForeignKey("Tracker")
    old_status = models.ForeignKey("IssueStatus", related_name="old_workflows")
    new_status = models.ForeignKey("IssueStatus", related_name="new_workflows")
    role = models.ForeignKey("Role")
    class Meta:
        db_table = u'workflows'


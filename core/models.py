from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    class Meta:
        permissions = [
            ('can_staff', 'Can staff'),
        ]
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="core_user_set",
        related_query_name="core_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="core_user_set",
        related_query_name="core_user",
    )
        
    GENDER_CHOICES = (
        ('male',   'Male'),
        ('female', 'Female'),
    )
    
    role_choice = (
    ('admin', 'Admin'),
    ('manager', 'Project Manager'),
    ('developer', 'Developer'),
    ('tester', 'Tester'),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20,choices=role_choice,default='developer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    objects = UserManager()

    #override userName filed
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else self.email
    
class Project(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    manager = models.ForeignKey(User,on_delete=models.CASCADE,related_name='managed_projects',db_column="manager_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name


class Module(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='modules',db_column="project_id")
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "modules"

    def __str__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]

    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='tasks',db_column="module_id")
    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True,related_name='assigned_tasks',db_column="assigned_to")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return self.title


class Bug(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]

    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='bugs',db_column="task_id")
    description = models.TextField()
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reported_bugs',db_column="reported_by")
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True,related_name='assigned_bugs',db_column="assigned_to")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    reported_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "bugs"

    def __str__(self):
        return f"Bug #{self.pk} - {self.description[:30]}"


class TimeLog(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='timelogs',db_column="task_id")
    developer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='time_logs',db_column="developer_id")
    hours_spent = models.FloatField()
    date = models.DateField()

    class Meta:
        db_table = "time_logs"

    def __str__(self):
        return f"{self.developer} - {self.hours_spent} hrs"

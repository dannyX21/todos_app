from django.db import models

class Todo(models.Model):
    class Meta:
        db_table = 'todos'
        managed = True

    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    completed_at = models.DateTimeField(null=True, blank=True, default=None)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.name} (user: {self.user.id})'

    def is_done(self):
        return self.completed_at != None

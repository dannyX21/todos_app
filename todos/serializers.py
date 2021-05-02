from rest_framework import serializers
from todos.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id',
            'name',
            'description',
            'due_date',
            'created_at',
            'updated_at',
            'completed_at',
        )

    def validate(self, data):
        if self.context.get('user') is not None:
            data['user'] = self.context['user']

        return super(TodoSerializer, self).validate(data)

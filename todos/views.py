import pytz
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from todos.models import Todo
from todos.serializers import TodoSerializer
from todos.permissions import TodoPermission


class TodoView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):

    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, TodoPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    queryset = Todo.objects.all()

    def get_serializer_context(self):
        context = super(TodoView, self).get_serializer_context()
        context['user_pk'] = self.request.user.id
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        context = self.get_serializer_context()
        queryset = self.queryset.filter(deleted_at__isnull=True)
        if context.get('user') is not None:
            queryset = queryset.filter(user=context['user'])

        return queryset

    def destroy(self, request, *args, **kwargs):
        self.perform_authentication(request)
        instance = self.get_object()
        instance.deleted_at = datetime.utcnow().replace(tzinfo=pytz.utc)
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('put',), url_path='check', permission_classes=(TodoPermission,))
    def check(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.is_done():
            return Response({'error': f'TODO with id {todo.id} is already done!'}, status.HTTP_400_BAD_REQUEST)

        todo.completed_at = datetime.utcnow().replace(tzinfo=pytz.utc)
        todo.save()
        serializer = TodoSerializer(todo, many=False, context=self.get_serializer_context())
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=('put',), url_path='uncheck', permission_classes=(TodoPermission,))
    def uncheck(self, request, *args, **kwargs):
        todo = self.get_object()
        if not todo.is_done():
            return Response({'error': f'TODO with id {todo.id} is not complete yet!'}, status.HTTP_400_BAD_REQUEST)

        todo.completed_at = None
        todo.save()
        serializer = TodoSerializer(todo, many=False, context=self.get_serializer_context())
        return Response(serializer.data, status.HTTP_200_OK)


    
    


    
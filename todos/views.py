from .models import Todo

todo = Todo.objects.create(
    task="할 일",
)

todos = Todo.objects.all()
todo = Todo.objects.get()

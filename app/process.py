from app.models import Info, Task


def process_task(task_id, parameters):
    """Process the task asynchronously"""
    try:
        task = Task.objects.get(id=task_id)
        task.status = "processing"
        task.save()

        start_date = parameters["start_date"]
        end_date = parameters["end_date"]

        # Get info for the user within the date range
        queryset = Info.objects.filter(
            user=task.user,
            date__range=[start_date, end_date]
        ).order_by('-date', '-id')

        # Build concatenated text
        concatenated_text = "".join([info.info for info in queryset])

        # Update task with result
        task.result = concatenated_text
        task.status = 'completed'
        task.save()

    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.save()

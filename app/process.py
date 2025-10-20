from app.models import Info


class QueueProcess:
    def _get_queryset(self, user, start_date, end_date):
        info = Info.objects.filter(user=user, date__range=[start_date, end_date])
        return info.order_by('-date', '-id')

    def process(self, user, parameters):
        start_date, end_date = parameters["start_date"], parameters["end_date"]
        queryset = self._get_queryset(user, start_date, end_date)
        return "".join([info.info for info in queryset])

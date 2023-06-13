import datetime as dt


def year(request):
    """Добавляет переменную с текущим годом."""
    now = dt.datetime.today().year
    return {
        'year': now,
    }

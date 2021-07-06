import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_today_limit(self):
        """Остаток дня."""
        limit_today = self.limit - self.get_today_stats()
        return limit_today

    def add_record(self, record):
        """Добавляет новую запись в список."""
        self.records.append(record)

    def get_today_stats(self):
        """Кол-во съеденных калорий/потраченных денег за 1 день."""
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)

    def get_week_stats(self):
        """Кол-во съеденных калорий/потраченных денег за 7 дней."""
        date_today = dt.date.today()
        week_delta = date_today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if week_delta <= record.date <= date_today)


class CaloriesCalculator(Calculator):
    CALORIES = (
        "Сегодня можно съесть что-нибудь ещё, "
        "но с общей калорийностью не более {value} кКал"
    )
    STOP_CALORIES = "Хватит есть!"

    def get_calories_remained(self):
        """Выводит кол-во калорий, которые можно потребить."""
        limit_today = self.get_today_limit()
        if limit_today > 0:
            return self.CALORIES.format(value=limit_today)
        else:
            return self.STOP_CALORIES


class CashCalculator(Calculator):
    USD_RATE = 73.0
    EURO_RATE = 87.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency='rub'):
        """Определяет сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро."""
        currencies = {'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE),
                      'rub': ('руб', CashCalculator.RUB_RATE)}
        cash_remained = self.get_today_limit()
        if cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return f'Валюта {currency} не поддерживается'
        name, rate = currencies[currency]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            message = f'На сегодня осталось {cash_remained} {name}'
        else:
            cash_remained = abs(cash_remained)
            message = (f'Денег нет, держись: твой долг - {cash_remained} '
                       f'{name}')
        return message


class Record:
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()

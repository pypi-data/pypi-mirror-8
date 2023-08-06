import calendar

class DefaultLocale(object):
    '''Default calendar.

    In english language, Sunday as first day, no holidays.
    '''
    @property
    def month_names(self):
        return (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        )

    def month_title(self, year, month):
        return "%s %d" % (self.month_names[month - 1], year)

    @property
    def first_day_of_week(self):
        return calendar.SUNDAY

    @property
    def weekend(self):
        return [ calendar.SATURDAY, calendar.SUNDAY ]

    def holidays(self, year):
        return []
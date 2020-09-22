from datetime import datetime


class Base(object):
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    datetime_format = date_format + 'T%s' % time_format
    full_datetime_format = date_format + 'T' + time_format + '.%f'
    iso_format = date_format + 'T%sZ' % time_format
    standard_datetime_format = date_format + ' ' + time_format
    extended_datetime_format = date_format + 'T' + time_format +'.%fZ'

    @classmethod
    def parse_date_time(cls, text):
        instance = None
        formats = [cls.extended_datetime_format, cls.full_datetime_format, cls.datetime_format, cls.standard_datetime_format, cls.iso_format, cls.date_format]
        for format in formats:
            try:
                instance = datetime.strptime(text, format)
            except Exception:
                pass
            else:
                break
        return instance

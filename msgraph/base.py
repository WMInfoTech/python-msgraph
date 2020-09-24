from datetime import datetime


class Base(object):
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    datetime_format = date_format + 'T%s' % time_format
    full_datetime_format = date_format + 'T' + time_format + '.%f'
    iso_format = date_format + 'T%sZ' % time_format
    standard_datetime_format = date_format + ' ' + time_format
    extended_datetime_format = date_format + 'T' + time_format +'.%fZ'

    tz_datetime_format = date_format + 'T' + time_format + '%z'

    @classmethod
    def parse_date_time(cls, text):
        instance = None
        instance = cls.parse_raw_date_time(text)
        if not instance:
            instance = cls.parse_tz_date_time(text)
        return instance

    @classmethod
    def parse_raw_date_time(cls, text):
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

    @classmethod
    def parse_tz_date_time(cls, text):
        instance = None
        formats = [cls.tz_datetime_format]
        # if colon in timezone, remove it
        if ":" == text[-3:-2]:
            text = text[:-3] + text[-2:]
        for format in formats:
            try:
                instance = datetime.strptime(text, format)
            except Exception:
                pass
            else:
                break
        return instance

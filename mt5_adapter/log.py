from loguru import logger

my_logger = logger

try:
    import ujson as json
except ImportError:
    import json

class LogJson(dict):
    def __init__(self, short_message_=None, dictionary_=None, **kwargs):
        self.default_short_message = 'JSON ENTRY'
        if dictionary_ is None and isinstance(short_message_, dict):
            dictionary_, short_message_ = short_message_, None
        is_dict = isinstance(dictionary_, dict)
        self.short_message = str(short_message_)
        if is_dict:
            super().__init__(dictionary_)
        else:
            super().__init__(**kwargs)

    def __str__(self):
        type_ = self['type']
        msg = self.short_message or type_ or self.default_short_message
        res = f"{msg}\t{json.dumps(self)}"
        return res

import re


re1 = re.compile(r'(.)([A-Z][a-z]+)')
re2 = re.compile(r'([a-z0-9])([A-Z])')


def arg(*args, **kwargs):
    return (args, kwargs or {})


class Command(object):

    def _get_args(self):
        if hasattr(self, 'args'):
            return self.args
        else:
            return []

    def _get_help(self):
        if hasattr(self, 'help'):
            return self.help
        elif self.__doc__:
            return self.__doc__.strip().split('\n')[0]
        else:
            return None

    def _get_name(self):
        if hasattr(self, 'name'):
            return self.name

        name = self.__class__.__name__.replace('Command', '')

        if name == '':
            raise NotImplementedError()
        else:
            s1 = re.sub(re1, r'\1-\2', name)
            return re.sub(re2, r'\1-\2', s1).lower()

    def _get_description(self):
        if hasattr(self, 'description'):
            return self.description
        elif self.__doc__:
            doc_string = self.__doc__.strip().split('\n')
            if len(doc_string) > 2:
                return '\n'.join(doc_string[2:])
        return None

    def _get_subparser_kwargs(self):
        return {
            'help': self._get_help(),
            'description': self._get_description()
        }

    def run(self, args, parser):
        raise NotImplementedError()

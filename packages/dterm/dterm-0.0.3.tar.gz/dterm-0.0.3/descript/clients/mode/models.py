class Collection:
    def __init__(self, **kwargs):
        self.restricted = kwargs.get('restricted')
        self.state = kwargs.get('state')
        self.space_type = kwargs.get('space_type')
        self.name = kwargs.get('name')
        self.token = kwargs.get('token')

    def __repr__(self):
        return f"Collection: {self.name}"

class Query:
    def __init__(self, **kwargs):
        self.sql = kwargs.get("raw_query", kwargs.get('query', ''))
        self.name = kwargs.get('name')

    def __repr__(self):
        return f"Query: {self.name}"


class Schedule:
    def __init__(self, last_run_at=None, last_succeeded_at=None,
                 frequency=None, destroy=None, **kwargs):
        self.last_run_at = date.parse(last_run_at)
        self.last_succeeded_at = date.parse(last_succeeded_at)
        self.frequency = frequency
        self.destroy = None
        if destroy:
            self.destroy = destroy['action']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        attrs = "\t".join(map(str, [
           self.destroy,
           self.last_run_at,
           self.last_succeeded_at,
           str(self.last_succeeded_at - self.last_run_at),
           self.frequency
        ]))
        return f"Schedule: {attrs}"


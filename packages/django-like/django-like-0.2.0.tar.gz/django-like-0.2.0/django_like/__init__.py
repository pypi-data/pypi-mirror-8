import django

from django.db import backend


if django.VERSION[0] == 1 and django.VERSION[1] >= 7:

    from django.db.models.lookups import Contains, IContains
    from django.db.models import Field

    class Like(Contains):
        lookup_name = 'like'

        def get_rhs_op(self, connection, rhs):
            return connection.operators['contains'] % rhs

        def as_sql(self, qn, connection):
            return super(Like, self).as_sql(qn, connection)

    class ILike(IContains):
        lookup_name = 'ilike'

        def process_lhs(self, qn, connection):
            lhs_sql, params = super(ILike, self).process_lhs(qn, connection)
            backend_name = backend.__name__
            if 'postgres' in backend_name or \
               'oracle' in backend_name:
                lhs_sql = 'UPPER(%s)' % lhs_sql
            return (lhs_sql, params)

        def get_rhs_op(self, connection, rhs):
            return connection.operators['icontains'] % rhs

        def as_sql(self, qn, connection):
            return super(ILike, self).as_sql(qn, connection)

    Field.register_lookup(Like)
    Field.register_lookup(ILike)

else:
    from django.db import connection
    from django.db.models.fields import Field, subclassing
    from django.db.models.sql.constants import QUERY_TERMS

    if isinstance(QUERY_TERMS, set):
        QUERY_TERMS.add('like')
        QUERY_TERMS.add('ilike')
    else:
        QUERY_TERMS['like'] = None
        QUERY_TERMS['ilike'] = None

    connection.operators['like'] = connection.operators['contains']
    connection.operators['ilike'] = connection.operators['icontains']
    NEW_LOOKUP_TYPE = ('like', 'ilike')

    def get_prep_lookup(self, lookup_type, value):
        try:
            return self.get_prep_lookup_origin(lookup_type, value)
        except TypeError as e:
            if lookup_type in NEW_LOOKUP_TYPE:
                return value
            raise e

    def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
        try:
            value_returned = self.get_db_prep_lookup_origin(lookup_type,
                                                            value,
                                                            *args, **kwargs)
        except TypeError as e:  # Django 1.1
            if lookup_type in NEW_LOOKUP_TYPE:
                return [value]
            raise e
        if value_returned is None and lookup_type in NEW_LOOKUP_TYPE:  # Dj > 1.1
            return [value]
        return value_returned

    def monkey_get_db_prep_lookup(cls):
        cls.get_db_prep_lookup_origin = cls.get_db_prep_lookup
        cls.get_db_prep_lookup = get_db_prep_lookup
        if hasattr(subclassing, 'call_with_connection_and_prepared'):  # Dj > 1.1
            setattr(cls, 'get_db_prep_lookup',
                    subclassing.call_with_connection_and_prepared(cls.get_db_prep_lookup))
            for new_cls in cls.__subclasses__():
                monkey_get_db_prep_lookup(new_cls)

    def lookup_cast(self, lookup_type):
        lookup = '%s'
        if lookup_type == 'ilike':
            return 'UPPER(%s)' % lookup
        return self.lookup_cast_origin(lookup_type)

    def monkey_ilike():
        backend_name = backend.__name__
        if 'postgres' in backend_name or \
           'oracle' in backend_name:
            connection.ops.__class__.lookup_cast_origin = connection.ops.lookup_cast
            connection.ops.__class__.lookup_cast = lookup_cast

    monkey_get_db_prep_lookup(Field)
    monkey_ilike()
    if hasattr(Field, 'get_prep_lookup'):
        Field.get_prep_lookup_origin = Field.get_prep_lookup
        Field.get_prep_lookup = get_prep_lookup

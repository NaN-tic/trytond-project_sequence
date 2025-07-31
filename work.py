# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields, Unique
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    code = fields.Char('Code', states={
            'readonly': Eval('code_readonly', True),
            })
    code_readonly = fields.Function(fields.Boolean('Code Readonly'),
        'get_code_readonly')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._order.insert(0, ('code', 'ASC'))
        cls._order.insert(1, ('id', 'ASC'))
        t = cls.__table__()
        cls._sql_constraints += [
            ('code_unique', Unique(t, t.code, t.company),
                'project_sequence.msg_code_unique'),
            ]

    @classmethod
    def default_code_readonly(cls, **pattern):
        Configuration = Pool().get('work.configuration')
        config = Configuration(1)
        return bool(config.get_multivalue('work_sequence', **pattern))

    def get_code_readonly(self, name):
        return self.default_code_readonly()

    def get_rec_name(self, name):
        transaction = Transaction()
        with transaction.set_context(rec_name_without_code=True):
            res = super().get_rec_name(name)
        if (self.code and self.type == 'task' and
                not transaction.context.get('rec_name_without_code', False)):
            return '[%s] %s' % (self.code, res)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super().search_rec_name(name, clause)
        return ['OR',
            domain,
            ('code',) + tuple(clause[1:]),
            ]

    @classmethod
    def create(cls, vlist):
        Configuration = Pool().get('work.configuration')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('code'):
                config = Configuration(1)
                if not config.work_sequence:
                    continue
                values['code'] = config.work_sequence.get()
        return super().create(vlist)

    @classmethod
    def copy(cls, works, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default.setdefault('code')
        return super().copy(works, default)

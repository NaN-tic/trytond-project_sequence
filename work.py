# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    code = fields.Char('Code', readonly=True, select=True)

    def get_rec_name(self, name):
        res = super(Work, self).get_rec_name(name)
        if self.parent:
            return '[%s] %s' % (self.code, res)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('code',) + tuple(clause[1:]),
            ('work',) + tuple(clause[1:]),
            ]

    @classmethod
    def create(cls, vlist):
        Sequence = Pool().get('ir.sequence')
        Configuration = Pool().get('work.configuration')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('code'):
                config = Configuration(1)
                values['code'] = Sequence.get_id(config.work_sequence.id)
        return super(Work, cls).create(vlist)

    @classmethod
    def copy(cls, works, default=None):
        if default is None:
            default = {}
        if 'code' not in default:
            default['code'] = None
        return super(Work, cls).copy(works, default)

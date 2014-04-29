# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'

    code = fields.Char('Code', readonly=True, select=True)

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

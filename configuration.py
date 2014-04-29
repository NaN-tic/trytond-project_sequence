#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

__all__ = ['Configuration']


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Work Configuration'
    __name__ = 'work.configuration'

    work_sequence = fields.Property(fields.Many2One('ir.sequence',
            'Work Sequence', domain=[
                ('code', '=', 'project.work'),
                ]))

# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool
from trytond.pyson import Eval, Id
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)


class Configuration(
        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
    'Work Configuration'
    __name__ = 'work.configuration'

    work_sequence = fields.MultiValue(fields.Many2One('ir.sequence',
            'Work Sequence', domain=[
                ('sequence_type', '=', Id('project_sequence',
                        'sequence_type_work')),
                ('company', 'in',
                    [Eval('context', {}).get('company', -1), None]),
                ]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'work_sequence'}:
            return pool.get('work.configuration.work_sequence')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationWorkSequence(ModelSQL, CompanyValueMixin):
    "Work Sequence Value"
    __name__ = 'work.configuration.work_sequence'

    work_sequence = fields.Many2One('ir.sequence',
            'Work Sequence', domain=[
                ('sequence_type', '=', Id('project_sequence',
                        'sequence_type_work')),
                ('company', 'in',
                    [Eval('company', -1), None]),
                ], depends=['company'])

    @classmethod
    def default_work_sequence(cls):
        pool = Pool()
        Sequence = pool.get('ir.sequence')
        ModelData = pool.get('ir.model.data')

        sequence_type_id = ModelData.get_id('project_sequence',
            'sequence_type_work')
        sequences = Sequence.search([('sequence_type', '=', sequence_type_id)])
        if sequences:
            return sequences[0]

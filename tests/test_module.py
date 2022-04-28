
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import (CompanyTestMixin, create_company,
    set_company)


class ProjectSequenceTestCase(CompanyTestMixin, ModuleTestCase):
    'Test ProjectSequence module'
    module = 'project_sequence'

    @with_transaction()
    def test_project_sequence(self):
        "Test Project Sequence"
        pool = Pool()
        ProjectWork = pool.get('project.work')
        Config = pool.get('work.configuration')
        Sequence = pool.get('ir.sequence')

        sequence, = Sequence.search([('name', '=', 'Work')])
        company = create_company()
        with set_company(company):
            config = Config(1)
            config.work_sequence = sequence
            config.save()
            p_work = ProjectWork()
            p_work.name = 'Work'
            p_work.company = company
            p_work.save()
            self.assertEqual(p_work.code, '1')
            p_work2, = ProjectWork.copy([p_work])
            self.assertEqual(p_work2.code, '2')


del ModuleTestCase

# This file is part project_sequence module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool
from trytond.modules.company.tests import create_company, set_company


class ProjectSequenceTestCase(ModuleTestCase):
    'Test Project Sequence module'
    module = 'project_sequence'

    @with_transaction()
    def test_project_sequence(self):
        "Test Project Sequence"
        pool = Pool()
        ProjectWork = pool.get('project.work')

        company = create_company()
        with set_company(company):
            p_work, = ProjectWork.create([{
                        'name': 'Work',
                        'company': company.id,
                        }])
            self.assertEqual(p_work.code, '1')
            p_work2, = ProjectWork.copy([p_work])
            self.assertEqual(p_work2.code, '2')

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProjectSequenceTestCase))
    return suite

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .work import *
from .configuration import *


def register():
    Pool.register(
        Work,
        Configuration,
        module='project_sequence', type_='model')

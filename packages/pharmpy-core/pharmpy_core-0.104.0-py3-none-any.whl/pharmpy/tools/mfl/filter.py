from pharmpy.tools.mfl.statement.definition import Let
from pharmpy.tools.mfl.statement.feature.absorption import Absorption
from pharmpy.tools.mfl.statement.feature.covariate import Covariate
from pharmpy.tools.mfl.statement.feature.direct_effect import DirectEffect
from pharmpy.tools.mfl.statement.feature.effect_comp import EffectComp
from pharmpy.tools.mfl.statement.feature.elimination import Elimination
from pharmpy.tools.mfl.statement.feature.indirect_effect import IndirectEffect
from pharmpy.tools.mfl.statement.feature.lagtime import LagTime
from pharmpy.tools.mfl.statement.feature.peripherals import Peripherals
from pharmpy.tools.mfl.statement.feature.transits import Transits

modelsearch_statement_types = (
    Absorption,
    Elimination,
    LagTime,
    Peripherals,
    Transits,
)

covsearch_statement_types = (
    Let,
    Covariate,
)


structsearch_statement_types = (DirectEffect, EffectComp, IndirectEffect)

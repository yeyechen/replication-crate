"""
Wrapper to run src/tables.py despite the utils/calendar.py shadow of stdlib calendar.

Loads utils.calendar explicitly via importlib before pandas imports _strptime, so
pandas's import of stdlib calendar succeeds. Then exec's tables.py.
"""
import sys
import importlib.util as iu

# Step 1: pre-load utils.calendar before utils/ is on sys.path
utils_cal_spec = iu.spec_from_file_location(
    'utils.calendar', '/home/ra_alan_mike_share/rep-it-up/utils/calendar.py'
)
utils_cal_mod = iu.module_from_spec(utils_cal_spec)
sys.modules['utils.calendar'] = utils_cal_mod
utils_cal_spec.loader.exec_module(utils_cal_mod)

# Step 2: pre-load utils package
utils_spec = iu.spec_from_file_location(
    'utils',
    '/home/ra_alan_mike_share/rep-it-up/utils/__init__.py',
    submodule_search_locations=['/home/ra_alan_mike_share/rep-it-up/utils'],
)
utils_pkg = iu.module_from_spec(utils_spec)
sys.modules['utils'] = utils_pkg
utils_spec.loader.exec_module(utils_pkg)

# Step 3: now safe to add to path and import pandas (which loads stdlib calendar via _strptime)
sys.path.insert(0, '/home/ra_alan_mike_share/rep-it-up/replications/belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability/src')
sys.path.insert(0, '/home/ra_alan_mike_share/rep-it-up/utils')

# Step 4: exec tables.py
TABLES_PATH = '/home/ra_alan_mike_share/rep-it-up/replications/belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability/src/tables.py'
with open(TABLES_PATH) as f:
    src = f.read()

# Replace pandas import to ensure stdlib calendar is loaded before pandas
ns = {'__name__': '__main__', '__file__': TABLES_PATH}
exec(src, ns)
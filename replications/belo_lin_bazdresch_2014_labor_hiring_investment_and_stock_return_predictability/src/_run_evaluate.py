"""
Wrapper to run src/evaluate.py with utils.calendar pre-loaded.
"""
import sys
import importlib.util as iu

# Step 1: pre-load utils.calendar
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

# Step 3: add paths
sys.path.insert(0, '/home/ra_alan_mike_share/rep-it-up/replications/belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability/src')
sys.path.insert(0, '/home/ra_alan_mike_share/rep-it-up/utils')

# Step 4: exec evaluate.py
EVAL_PATH = '/home/ra_alan_mike_share/rep-it-up/replications/belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability/src/evaluate.py'
with open(EVAL_PATH) as f:
    src = f.read()

ns = {'__name__': '__main__', '__file__': EVAL_PATH}
exec(src, ns)

from ompr.runner import RunningWorker
from torchness.devices import DevicesTorchness
from pypaq.pms.base import POINT, get_params
from typing import Callable, Optional, Any



# hpmser RunningWorker (process run by OMP in hpmser)
class HRW(RunningWorker):

    def __init__(
            self,
            func: Callable,
            func_const: Optional[POINT],
            device: DevicesTorchness=   None,
    ):

        self.func = func
        self.func_const = func_const if func_const else {}
        self.device = device

        # manage 'device'/'devices' & 'hpmser_mode' param in func >> set it in func if needed
        func_args = get_params(self.func)
        func_args = list(func_args['with_defaults'].keys()) + func_args['without_defaults']
        for k in ['device','devices']:
            if k in func_args:
                self.func_const[k] = self.device
        if 'hpmser_mode' in func_args: self.func_const['hpmser_mode'] = True

    # processes given point - computes value
    def process(
            self,
            point: POINT,
            **kwargs) -> Any:

        point_with_defaults = {}
        point_with_defaults.update(self.func_const)
        point_with_defaults.update(point)

        res = self.func(**point_with_defaults)
        if type(res) is dict: value = res['value']
        else:                 value = res

        msg = {'point':point, 'value':value}
        msg.update(kwargs)
        return msg
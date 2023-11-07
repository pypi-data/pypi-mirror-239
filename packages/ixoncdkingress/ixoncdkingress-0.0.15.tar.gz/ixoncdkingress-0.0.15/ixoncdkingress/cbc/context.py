import warnings

warnings.warn("ixoncdkingress.cbc had been deprecated, please use ixoncdkingress.function", DeprecationWarning)

from ixoncdkingress.function.context import FunctionContext, FunctionResource

CbcContext = FunctionContext
CbcResource = FunctionResource

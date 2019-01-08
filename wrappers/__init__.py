import ast
from .RFFlatWrapper import RFFlatWrapper
from .RFAssignFlatWrapper import RFAssignFlatWrapper
from .RFReturnFlatWrapper import RFReturnFlatWrapper
from .RFMethodFlatWrapper import RFMethodFlatWrapper
from .RFCFlowFlatWrapper import RFCFlowFlatWrapper
from .RFCompareFlatWrapper import RFCompareFlatWrapper
from .RFLiteralFlatWrapper import RFLiteralFlatWrapper
from .RFExprFlatWrapper import RFExprFlatWrapper
from .RFCallFlatWrapper import RFCallFlatWrapper


flat_wrappers = {
    ast.Assign: RFAssignFlatWrapper,
    ast.Return: RFReturnFlatWrapper,
    ast.Module: RFMethodFlatWrapper,
    ast.If: RFCFlowFlatWrapper,
    ast.While: RFCFlowFlatWrapper,
    ast.For: RFCFlowFlatWrapper,
    ast.Compare: RFCompareFlatWrapper,
    ast.Num: RFLiteralFlatWrapper,
    ast.Str: RFLiteralFlatWrapper,
    ast.Name: RFLiteralFlatWrapper,
    ast.Expr: RFExprFlatWrapper,
    ast.Call: RFCallFlatWrapper,
    'generic': RFFlatWrapper
}


__all__ = ['RFAssignFlatWrapper', 'RFReturnFlatWrapper', 'RFMethodFlatWrapper',
           'RFCFlowFlatWrapper', 'RFCompareFlatWrapper', 'RFLiteralFlatWrapper',
           'RFExprFlatWrapper', 'RFCallFlatWrapper', 'RFFlatWrapper']

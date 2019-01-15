import ast
from .flatwrapper import FlatWrapper
from .assign_flatwrapper import AssignFlatWrapper
from .return_flatwrapper import ReturnFlatWrapper
from .method_flatwrapper import MethodFlatWrapper
from .cflow_flatwrapper import CFlowFlatWrapper
from .compare_flatwrapper import CompareFlatWrapper
from .literal_flatwrapper import LiteralFlatWrapper
from .expr_flatwrapper import ExprFlatWrapper
from .call_flatwrapper import CallFlatWrapper


flat_wrappers = {
    ast.Assign: AssignFlatWrapper,
    ast.Return: ReturnFlatWrapper,
    ast.Module: MethodFlatWrapper,
    ast.If: CFlowFlatWrapper,
    ast.While: CFlowFlatWrapper,
    ast.For: CFlowFlatWrapper,
    ast.Compare: CompareFlatWrapper,
    ast.Num: LiteralFlatWrapper,
    ast.Str: LiteralFlatWrapper,
    ast.Name: LiteralFlatWrapper,
    ast.Expr: ExprFlatWrapper,
    ast.Call: CallFlatWrapper,
    "generic": FlatWrapper,
}


__all__ = [
    "AssignFlatWrapper",
    "ReturnFlatWrapper",
    "MethodFlatWrapper",
    "CFlowFlatWrapper",
    "CompareFlatWrapper",
    "LiteralFlatWrapper",
    "ExprFlatWrapper",
    "CallFlatWrapper",
    "FlatWrapper",
]

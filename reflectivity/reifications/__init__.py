from .reifications import ClassReification, NodeReification, \
                          ObjectReification, MethodReification, \
                          SenderReification, ReceiverReification, \
                          SelectorReification, NameReification, \
                          ValueReification, OldValueReification, \
                          NewValueReification, ArgumentReification, \
                          ConstReification


__all__ = ['ClassReification', 'NodeReification', 'ObjectReification',
           'MethodReification', 'SenderReification',
           'ReceiverReification', 'SelectorReification',
           'NameReification', 'ValueReification', 'OldValueReification',
           'NewValueReification', 'ArgumentReification']


reifications_dict = {
    'class': ClassReification,
    'node': NodeReification,
    'object': ObjectReification,
    'method': MethodReification,
    'sender': SenderReification,
    'receiver': ReceiverReification,
    'selector': SelectorReification,
    'name': NameReification,
    'value': ValueReification,
    'old_value': OldValueReification,
    'new_value': NewValueReification,
    'arguments': ArgumentReification
}


def reification_for(key, metalink):
    if key in reifications_dict:
        return reifications_dict[key]()
    if key == 'link':
        return ConstReification(metalink)
    return ConstReification(key)

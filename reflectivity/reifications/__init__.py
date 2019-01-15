from .RFReification import RFClassReification, RFNodeReification, \
                           RFObjectReification, RFMethodReification, \
                           RFSenderReification, RFReceiverReification, \
                           RFSelectorReification, RFNameReification, \
                           RFValueReification, RFOldValueReification, \
                           RFNewValueReification, RFArgumentReification


__all__ = ['RFClassReification', 'RFNodeReification', 'RFObjectReification',
           'RFMethodReification', 'RFSenderReification',
           'RFReceiverReification', 'RFSelectorReification',
           'RFNameReification', 'RFValueReification', 'RFOldValueReification',
           'RFNewValueReification', 'RFArgumentReification']


reifications = {
    'class': RFClassReification,
    'node': RFNodeReification,
    'object': RFObjectReification,
    'method': RFMethodReification,
    'sender': RFSenderReification,
    'receiver': RFReceiverReification,
    'selector': RFSelectorReification,
    'name': RFNameReification,
    'value': RFValueReification,
    'old_value': RFOldValueReification,
    'new_value': RFNewValueReification,
    'arguments': RFArgumentReification
}


def reification_for(key, metalink):
    if key in reifications:
        return reifications[key]()
    if key == 'link':
        return RFConstReification(metalink)
    return RFConstReification(key)

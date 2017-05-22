from collections import defaultdict, namedtuple

Event = namedtuple('Event', ('name', 'old_value', 'new_value'))


class Module(object):
    possible_events = set()

    def __init__(self,
                 type, id, alias,
                 robot):
        self.id = id
        self._type = type
        self.alias = alias
        self._delegate = robot
        self._value = None
        self._cb = defaultdict(list)

    def __repr__(self):
        return ('<{self._type} '
                'alias="{self.alias}" '
                'id={self.id} '
                '{state}>'.format(self=self,
                                  state=self._state_repr()))

    def _state_repr(self):
        return ('state={}'.format(self._value)
                if self._value is not None else
                '')

    def _update(self, new_state):
        pass

    def _push_value(self, key, new_val):
        cmd = {
            self.alias: {
                key: new_val
            }
        }
        self._delegate._msg_stack.put(cmd)

    # Events cb handling

    def add_callback(self, event, cb):
        self._cb[event].append(cb)

    def remove_callback(self, event, cb):
        self._cb[event].remove(cb)

    def _pub_event(self, trigger, old_value, new_value):
        event = Event(trigger, old_value, new_value)

        for cb in self._cb[trigger]:
            cb(event)

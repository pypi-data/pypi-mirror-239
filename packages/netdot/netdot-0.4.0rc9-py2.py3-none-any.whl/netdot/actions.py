from dataclasses import dataclass
from enum import IntEnum
from typing import Iterable, Tuple, TypeVar, ClassVar

import netdot
from netdot import defaults
from netdot.csv_util import CSVDataclass
from netdot.dataclasses import NetdotAPIDataclass


U = TypeVar('U', bound='netdot.NetdotAPIDataclass')


class ActionTypes(IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


def diff_string(old: str, new: str) -> str:
    """Create a 'diff string' if a pair of strings have any differences.

    The intention is to be able to provide a useful text representation of a diff that
    fits well into a CSV format.

    Args:
        old (str): The old string
        new (str): The new string.

    Returns:
        str: If 'new' and 'old' are different, return "[-old-]+new+". (Otherwise, return the old string).
    """
    if new == old:
        return old
    elif old:
        return f'[-{old}-]+{new}+'
    else:
        return f'+{new}+'


@dataclass(frozen=True)
class NetdotAction(CSVDataclass):
    action_type: ActionTypes
    id: int
    new_data: NetdotAPIDataclass
    old_data: NetdotAPIDataclass

    def updated_with(self, other: 'NetdotAction', other_came_first=True) -> 'NetdotAction':
        """Return a new action that is the combination of this action and the other action.

        Args:
            other (NetdotAction): The other action to combine with this one.
            other_came_first (bool): True if the other action came first.

        Returns:
            NetdotAction: A new action that is the combination of this action and the other action.
        """
        if self.action_type != ActionTypes.UPDATE or other.action_type != ActionTypes.UPDATE:
            raise ValueError('Both actions must be UPDATE actions.')
        if other_came_first:
            return other.consolidate_actions(self, other_came_first=False)
        else:
            ver1 = self.old_data.__dict__
            ver2 = self.new_data.__dict__
            ver3 = other.new_data.__dict__
            result1 = { k: ver2[k] for k in set(ver2.values()) - set(ver1.values()) }
            result2 = { k: ver3[k] for k in set(ver3.values()) - set(result1.values()) }
            return NetdotAction(
                action_type=ActionTypes.UPDATE,
                id=self.id,
                new_data=type(self.new_data)(**result2),
                old_data=self.old_data,
            )

    def table_header(self) -> Tuple[str, ...]:
        """Return a list of columns, to be used as a table header for objects of this class.

        > Works will with the as_table_row() method.

        Returns:
            Tuple[str,...]: A list of columns.
        """
        data = self.new_data if self.new_data else self.old_data
        header = ['action'] + list(data.table_header())
        return tuple(header)

    def as_table_row(self, select_columns: Iterable[str] = None, maxchars=defaults.TERSE_MAX_CHARS) -> Tuple[str, ...]:
        """Return a representation of this action as a table row (tuple).

        Args:
            select_columns (Iterable[str], optional): Which attributes of this object to be returned. Defaults to `table_header()` if None provided.

        Returns:
            Tuple[str, ...]: String representations of the attributes of this object.
        """
        return [self.action_type.name] + [str(datum)[:maxchars] for datum in self._as_table_row(select_columns)]

    def generate_log_for_action(self, truncate=None, completed=False) -> str:
        """Generate a log message for this action.

        Args:
            truncate (int, optional): Truncate the message to this many characters. Defaults to None.
            completed (bool, optional): Whether the action has been completed. Defaults to False.

        Returns:
            str: A log message indicating exactly what will change if this action is (was) completed.
        """
        take_action = self.action_type.name
        object_type = (
            self.old_data.__class__.__name__
            if self.action_type == ActionTypes.DELETE
            else self.new_data.__class__.__name__
        )
        data = (
            self.old_data if self.action_type == ActionTypes.DELETE else self.new_data
        )
        first_word = 'Will' if not completed else 'Finished'
        message = f'{first_word} {take_action} {object_type}: {data}'
        if self.action_type == ActionTypes.UPDATE:
            message += f" (replacing: {self.old_data})"
        if truncate:
            truncate = max(defaults.TRUNCATE_MIN_CHARS, truncate)
            truncate = truncate - len('...')
            if len(message) < truncate:
                return message
            else:
                return message[:truncate]+'...'

        else:
            return message

    def _as_table_row(self, fields=None) -> Tuple[str, ...]:
        """Represent this action as a table row, ordered per `table_header` property.

        > Works well with the table_header Class Property.

        If there is a difference, the 'diff' is represented according to the
        netdot.actions.diff_string() function.=

        Returns:
            Tuple: Representation of this action as a row of data.
        """
        as_table_row_methods = {
            ActionTypes.CREATE: self.as_table_row_CREATE,
            ActionTypes.DELETE: self.as_table_row_DELETE,
            ActionTypes.UPDATE: self.as_table_row_UPDATE,
        }
        return tuple(as_table_row_methods[self.action_type](fields))

    def as_table_row_DELETE(self, fields=None):
        if not fields:
            fields = self.old_data.table_header()
        ret = [getattr(self.old_data, field) for field in fields]
        return ret

    def as_table_row_UPDATE(self, fields=None):
        if not fields:
            fields = self.old_data.table_header()
        ret = [
            diff_string(getattr(self.old_data, field), getattr(self.new_data, field))
            for field in fields
        ]
        return ret

    def as_table_row_CREATE(self, fields=None):
        if not fields:
            fields = self.new_data.table_header()
        ret = [getattr(self.new_data, field) for field in fields]
        return ret

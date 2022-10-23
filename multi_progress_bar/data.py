"""
Module defining data structures used by the package.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ProgressBarUpdate:
    """
    Data class defining messages containing updates for client progress.
    """

    name: str
    """
    The name of the progress bar this update pertains to. This should be unique.
    """
    current_value: int
    """
    The integer value to update the progress bar to.
    """
    parent: Optional[str] = None
    """
    The parent of this progress bar. Used for cases of nested progress bars.
    """
    total: Optional[int] = None
    """
    The expected final, "full" value for this progress bar.
    """
    description: Optional[str] = None
    """
    The description to display for this progress bar.
    """


# Type aliases
ProgressBarUpdates = List[ProgressBarUpdate]

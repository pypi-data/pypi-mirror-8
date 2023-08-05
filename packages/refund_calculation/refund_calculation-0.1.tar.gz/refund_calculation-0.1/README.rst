refund_calculation
==================

https://pypi.python.org/pypi/refund_calculation/

Turns a chronological sequence of balance-adjustment events into a
timeline of periods during which particular balances were held.

.. pypi - Everything below this line goes into the description for PyPI.

For example, this sequence of events ...

- A: *$10*
- B: *$10*
- C: *($18)*
- D: *($2)*

... is turned into this timeline.

.. code::

    A             B             C             D
    |             |             |             |
    |_____________|_____________|             |
    |                           |             |
    |           $10             |             |
    |___________________________|             |
                  |             |             |
                  |     $8      |             |
                  |_____________|_____________|
                  |                           |
                  |            $2             |
                  |___________________________|

This lets you determine, for each balance reduction event, the events from
which the balance was added. In this example, we can see that:

- The $18 reduction in event C came from $10 of event A and $8 of B.
- The $2 reduction in event D came entirely from event B.

Code for this example:

.. code:: python

    from refund_calculation import *

    history_from_event_sequence([
        Event(time='A', delta='10'),
        Event(time='B', delta='10'),
        Event(time='C', delta='-18'),
        Event(time='D', delta='-2'),
    ])

    # Result:
    History(
        closed=(
            Closed(amount=Decimal('10'), start='A', end='C'),
            Closed(amount=Decimal('8'),  start='B', end='C'),
            Closed(amount=Decimal('2'),  start='B', end='D'),
        ),
        open=(),
        debt=Decimal('0'),
    )

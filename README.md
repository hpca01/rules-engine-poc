# Rules Engine Testing


## POC

This is all my personal musings to figure out how python can scale on my machine when it comes to task scheduling with millisecond precision and a rules engine. Feel free to fork and mess around with the code.

## Questions

1. With N tasks, when is the drift between time due and dequeue time?
    - Based on reference implementation there were different results, the function with logging slowed down to ~30 tasks before drift, and without logging was ~250 tasks before drift.
        - This kind of jives with my past experience working with python.
        - How does async logging help?

2. Rules implementation with yaml
    - Requirements
        - TBD




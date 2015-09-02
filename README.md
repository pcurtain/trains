**Hello ThoughtWorks Reviewers!!**

tl;dr:   Loved learning about graphs.  Run with ```python trainsproblem.py```

I just re-read the assignment email and saw the request for "design and
assumptions, along with your code, as well as detailed instructions to run your
application", so here's a brief bit of that.

I chose the 'Problem one: Trains' as a chance to play with graphs and graph
theory.  I've discussed their importance and application any number of times in
product discussions and team guidance but had yet to have a chance to dig into
them myself. Since it's a learning moment, I read a fair amount and drew on 
examples and posts about example implementations.

Once I started feeling my way through the example, I put everything into domain
terms (a big part of how i think through problems generally). I allowed myself,
for this phase, to sacrifice some performance (and inherent scalability) to use
abstractions I could narrate, share and pair on.  Hence RailSystem, Station,
Trip and TripStop.  Convenience in instantiating 'Trip' objects during the
recursion, for example, is a cost I wouldn't put into production, but helped me
wrap my head around things and separate sensible places for methods and data
that I though could survive into production.  In much the same way the
interesting elements of a large community activism graph could have very deep
abstractions, but for specific queries be pared down to efficient elements.

(sorry! might've been a bit long winded there.)

I try to think things through via tests that match user story elements.

In this case I just brought the problem test terms into a test module. So my
ideal path for the reviewer would be to read through the tests and, when clear,
run the unit tests with verbose output ```python -m unittest -v trainstest```
and that should be pretty clear.

To get precisely the output specified in the problem station, run 
```python trainsproblem.py```.  No surprises.

**Thanks for the fun and the learning!  Blessings!**
--p

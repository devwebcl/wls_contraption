# OQL queries

[http://blogs.oracle.com/sundararajan/permanent-generation-analysis-with-oql](http://blogs.oracle.com/sundararajan/permanent-generation-analysis-with-oql)


**How many classes loaded in my app?**

` select count(heap.classes())`

We use the classes method of heap object and used count built-in
to count the result of the same. The output was: 1950


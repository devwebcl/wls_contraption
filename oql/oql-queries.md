# OQL queries

[http://blogs.oracle.com/sundararajan/permanent-generation-analysis-with-oql](http://blogs.oracle.com/sundararajan/permanent-generation-analysis-with-oql)


**How many classes loaded in my app?**
(retrieving from a heapdump and queried thru eclipse-mat or visualvm)

` select count(heap.classes())`

`select count(heap.objects('sun.reflect.DelegatingClassLoader'))`

`select x from cl.ejemplo.foo.bar.Qux x`

We use the classes method of heap object and used count built-in
to count the result of the same. The output was: 1950


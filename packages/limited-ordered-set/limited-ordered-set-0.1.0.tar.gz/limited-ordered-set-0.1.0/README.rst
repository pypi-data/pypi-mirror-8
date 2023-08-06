Version 0.1.0

Limited Ordered Set
-------------------

Data type for storing sorted list of objects with sort order and list length limit. Useful for storing data like
history of user interactions on site.

Once added object to list overflow set length, it pop items from set beginning of set. You always have only last X
entries limited b `length` property.

Installation
------------

You can simple install library with `pip install limited-ordered-set`.

Example
-------

You can add as many as you want objects to LimitedOrderedSet, it will pop first items once items count hit limit.

For example you can go to tests.::

    limit = 10
    objcts = LimitedOrderedSet(limit)

    print 'Adding chars: ',
    for x in xrange(0, 50):
        c = choice(string.ascii_letters)
        print c,
        objcts.add(c)
    print

    print 'Resulting set items: %s' % ",".join(objcts)

Execution result

Adding chars:  B Z V N F k j j o v t M k j P v A Y O h E v f A g e F T Q b f r j t W q r C C S m P V m o B z a L w

Resulting set items: S,m,P,V,o,B,z,a,L,w

Contribution
------------

You always are welcome if you have any ideas. You can push request at github project page.

https://github.com/phpdude/limited-ordered-set
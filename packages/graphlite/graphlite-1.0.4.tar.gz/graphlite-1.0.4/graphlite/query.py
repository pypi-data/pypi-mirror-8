from contextlib import closing
from itertools import islice
import graphlite.sql as SQL


class V(object):
    __slots__ = ('src', 'rel', 'dst')

    """
    Create a new V object that represents an edge. This
    object is expected throughout the API where the
    parameter is named `edge`. All parameters are optional
    and default to None.

    :param src: The source node.
    :param rel: The relation.
    :param dst: The destination node.
    """
    def __init__(self, src=None, rel=None, dst=None):
        self.src = src
        self.rel = rel
        self.dst = dst

    def __getattr__(self, attr):
        """
        If the attribute being requested is found in the
        ``__slots__`` attribute, then return the actual
        thing, else assign the attribute as an internally
        stored relation.

        :param attr: The attribute.
        """
        self.rel = attr
        return self

    def __call__(self, dst):
        """
        Assign a destination node to the edge.

        :param dst: The destination node.
        """
        self.dst = dst
        return self

    def __repr__(self):
        return '(%s)-[%s]->(%s)' % (
            '*' if self.src is None else self.src,
            '*' if self.rel is None else ':%s' % self.rel,
            '*' if self.dst is None else self.dst,
        )

    def __eq__(self, other):
        """
        Checks for equality between the edge and
        another edge.

        :param other: The other thing.
        """
        if not isinstance(other, V):
            return NotImplemented
        return (self.src == other.src and
                self.rel == other.rel and
                self.dst == other.dst)

    def __hash__(self):
        """
        Uses Python's tuple hashing algorithm to
        hash the ``id`` integer, internal source,
        relation, and destination nodes.
        """
        return hash((self.src, self.rel, self.dst))


class Query(object):
    __slots__ = ('db', 'sql', 'params')

    """
    Create a new query object that acts on a particular
    SQLite connection instance.

    :param db: The SQLite connection.
    """
    def __init__(self, db, sql=tuple(), params=tuple()):
        self.db = db
        self.sql = sql
        self.params = params

    @property
    def statement(self):
        """
        Joins all of the SQL queries together and then
        returns the result. It is the query to be ran.
        """
        return '\n'.join(self.sql)

    def __iter__(self):
        """
        Execute the internally stored SQL query and then
        yield every result to the caller. You can reuse
        this function as many times as you want but it
        is not deterministic.
        """
        with closing(self.db.cursor()) as cursor:
            cursor.execute(self.statement, self.params)
            for row in cursor:
                yield row[0]

    def derived(self, statement, params=()):
        """
        Returns a new query object set up correctly with
        the *statement* and *params* appended to the end
        of the new instance's internal query and params,
        along with the current instance's data.

        :param statement: The SQL statements to append.
        :param params: The parameters to append.
        """
        return Query(
            db=self.db,
            sql=self.sql + (statement,),
            params=self.params + params,
        )

    def __call__(self, edge):
        """
        Selects either destination nodes or source nodes
        based on the edge query provided. If source node
        is specified, then destination nodes are selected,
        and vice versa.

        :param edge: The edge query.
        """
        src, rel, dst = edge.src, edge.rel, edge.dst
        statement, params = (
            SQL.forwards_relation(src, rel) if dst is None else
            SQL.inverse_relation(dst, rel)
        )
        return self.derived(statement, params)

    def traverse(self, edge):
        """
        Traverse the graph, and selecting the destination
        nodes for a particular relation that the selected
        nodes are a source of, i.e. select the friends of
        my friends.

        :param edge: The edge object. If the edge's
            destination node is specified then the source
            nodes will be selected.
        """
        query = self.statement
        rel, dst = edge.rel, edge.dst
        statement, params = (
            SQL.compound_fwd_query(query, rel) if dst is None else
            SQL.compound_inv_query(query, rel, dst)
        )
        return Query(db=self.db,
                     sql=(statement,),
                     params=self.params + params)

    @property
    def intersection(self):
        """
        Intersect the current query with another one.
        The method doesn't process the objects in a
        loop/set but uses an SQL query.
        """
        return self.derived(SQL.intersection)

    @property
    def difference(self):
        """
        Compute the difference between the current
        selected nodes and the another query, and
        explicitly not a `symmetric difference`.
        Similar in concept to
        :meth:`graphlite.query.Query.intersection`.
        """
        return self.derived(SQL.difference)

    @property
    def union(self):
        """
        Compute the union between the current selected
        nodes and another query. Similar to the
        :meth:`graphlite.query.Query.intersection`
        method.
        """
        return self.derived(SQL.union)

    def count(self):
        """
        Counts the objects returned by the query.
        You will not be able to iterate through this
        query again (with deterministic results,
        anyway).
        """
        return sum(1 for __ in self)

    def __getitem__(self, sl):
        """
        Only supports slicing operations, and returns
        an iterable with the slice taken into account.

        :param sl: The slice object.
        """
        return islice(self, sl.start, sl.stop, sl.step)

    def to(self, datatype):
        """
        Converts this iterable into another *datatype*
        by calling the provided datatype with the
        instance as the sole argument.

        :param datatype: The datatype.
        """
        return datatype(self)

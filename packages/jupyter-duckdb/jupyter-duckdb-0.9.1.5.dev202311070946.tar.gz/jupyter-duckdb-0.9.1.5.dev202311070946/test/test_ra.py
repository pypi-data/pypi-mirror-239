import duckdb_kernel.parser.elements.binary as BinaryOperators
import duckdb_kernel.parser.elements.unary as UnaryOperators
from duckdb_kernel.parser import RAParser
from duckdb_kernel.parser.elements import RAOperand, LogicElement
from . import Connection


def test_binary_operator_cross():
    root = RAParser.parse_query(r'shows x seasons')

    assert isinstance(root, BinaryOperators.Cross)
    assert isinstance(root.left, RAOperand) and root.left.name == 'shows'
    assert isinstance(root.right, RAOperand) and root.right.name == 'seasons'

    with Connection() as con:
        assert con.execute_ra(root) == [
            (1, 'Show 1', 1, 1, 'Show 1 / Season 1'),
            (1, 'Show 1', 1, 2, 'Show 2 / Season 1'),
            (1, 'Show 1', 2, 1, 'Show 1 / Season 2'),
            (1, 'Show 1', 2, 2, 'Show 2 / Season 2'),
            (2, 'Show 2', 1, 1, 'Show 1 / Season 1'),
            (2, 'Show 2', 1, 2, 'Show 2 / Season 1'),
            (2, 'Show 2', 2, 1, 'Show 1 / Season 2'),
            (2, 'Show 2', 2, 2, 'Show 2 / Season 2')
        ]


def test_binary_operator_difference():
    root = RAParser.parse_query(r'users \ banned_users')

    assert isinstance(root, BinaryOperators.Difference)
    assert isinstance(root.left, RAOperand) and root.left.name == 'users'
    assert isinstance(root.right, RAOperand) and root.right.name == 'banned_users'

    with Connection() as con:
        assert con.execute_ra(root) == [
            (1, 'Alice'),
            (3, 'Charlie')
        ]


def test_binary_operator_intersection():
    root = RAParser.parse_query(r'users ∩ banned_users')

    assert isinstance(root, BinaryOperators.Intersection)
    assert isinstance(root.left, RAOperand) and root.left.name == 'users'
    assert isinstance(root.right, RAOperand) and root.right.name == 'banned_users'

    with Connection() as con:
        assert con.execute_ra(root) == [
            (2, 'Bob')
        ]


def test_binary_operator_join():
    root = RAParser.parse_query(r'shows ⋈ seasons')

    assert isinstance(root, BinaryOperators.Join)
    assert isinstance(root.left, RAOperand) and root.left.name == 'shows'
    assert isinstance(root.right, RAOperand) and root.right.name == 'seasons'

    with Connection() as con:
        assert con.execute_ra(root) == [
            (1, 'Show 1', 1, 'Show 1 / Season 1'),
            (1, 'Show 1', 2, 'Show 1 / Season 2'),
            (2, 'Show 2', 1, 'Show 2 / Season 1'),
            (2, 'Show 2', 2, 'Show 2 / Season 2')
        ]


def test_binary_operator_union():
    root = RAParser.parse_query(r'users ∪ banned_users')

    assert isinstance(root, BinaryOperators.Union)
    assert isinstance(root.left, RAOperand) and root.left.name == 'users'
    assert isinstance(root.right, RAOperand) and root.right.name == 'banned_users'

    with Connection() as con:
        assert con.execute_ra(root) == [
            (1, 'Alice'),
            (2, 'Bob'),
            (3, 'Charlie'),
            (4, 'David')
        ]


def test_unary_operator_projection():
    with Connection() as con:
        for query in (
                r'π id users',
                r'π [ id ] users',
                r'π [ id ] ( users )',
                r'π[id](users)'
        ):
            root = RAParser.parse_query(query)

            assert isinstance(root, UnaryOperators.Projection)
            assert isinstance(root.arg, LogicElement)
            assert isinstance(root.target, RAOperand) and root.target.name == 'users'

            assert con.execute_ra(root) == [
                (1,),
                (2,),
                (3,)
            ]

        for query in (
                r'π id π id, username users',
                r'π [ id ] (π [ id, username ] (users))',
                r'π[id]π[id,username]users'
        ):
            root = RAParser.parse_query(query)

            assert isinstance(root, UnaryOperators.Projection)
            assert isinstance(root.arg, LogicElement)
            assert isinstance(root.target, UnaryOperators.Projection)
            assert isinstance(root.target.arg, LogicElement)
            assert isinstance(root.target.target, RAOperand) and root.target.target.name == 'users'

            assert con.execute_ra(root) == [
                (1,),
                (2,),
                (3,)
            ]


def test_unary_operator_rename():
    for query in (
            r'β id2 ← id users',
            r'β [ id2 ← id ] users',
            r'β [ id2 ← id ] ( users )',
            r'β[id2←id](users)'
    ):
        root = RAParser.parse_query(query)

        assert isinstance(root, UnaryOperators.Rename)
        assert isinstance(root.arg, LogicElement)
        assert isinstance(root.target, RAOperand) and root.target.name == 'users'

    for query in (
            r'β id ← id2 β id2 ← id users',
            r'β [id ← id2] (β [id2 ← id] (users))',
            r'βid←id2βid2←id users'
    ):
        root = RAParser.parse_query(query)

        assert isinstance(root, UnaryOperators.Rename)
        assert isinstance(root.arg, LogicElement)
        assert isinstance(root.target, UnaryOperators.Rename)
        assert isinstance(root.target.arg, LogicElement)
        assert isinstance(root.target.target, RAOperand) and root.target.target.name == 'users'


def test_unary_operator_selection():
    with Connection() as con:
        for query in (
                r'σ id > 1 users',
                r'σ [ id > 1 ] users',
                r'σ [ id > 1 ] ( users )',
                r'σ[id>1](users)'
        ):
            root = RAParser.parse_query(query)

            assert isinstance(root, UnaryOperators.Selection)
            assert isinstance(root.target, RAOperand) and root.target.name == 'users'
            assert isinstance(root.arg, LogicElement)

            assert con.execute_ra(root) == [
                (2, 'Bob'),
                (3, 'Charlie')
            ]

        for query in (
                r'σ id > 1 σ id > 0 users',
                r'σ [ id > 1 ] (σ [id > 1] (users))',
                r'σ[id>1]σ[id>1]users'
        ):
            root = RAParser.parse_query(query)

            assert isinstance(root, UnaryOperators.Selection)
            assert isinstance(root.arg, LogicElement)
            assert isinstance(root.target, UnaryOperators.Selection)
            assert isinstance(root.target.arg, LogicElement)
            assert isinstance(root.target.target, RAOperand) and root.target.target.name == 'users'

            assert con.execute_ra(root) == [
                (2, 'Bob'),
                (3, 'Charlie')
            ]


# TODO test evaluation order
# TODO test latin names

def test_special_queries():
    with Connection() as con:
        # Enclosing parentheses are removed. In the following case
        # the parentheses may only be removed from each subquery
        # independently after the cross join is applied. Otherwise,
        # the result is a parsing error.
        root = RAParser.parse_query(r'''
            (
              Sigma [ id > 1 ] Pi [ username, id ] (users)
            ) x (
              Beta [ username2 <- username ] Beta [ id2 <- id ] (banned_users)
            )
        ''')

        assert isinstance(root, BinaryOperators.Cross)
        assert isinstance(root.left, UnaryOperators.Selection)
        assert isinstance(root.left.target, UnaryOperators.Projection)
        assert isinstance(root.left.target.target, RAOperand) and root.left.target.target.name == 'users'
        assert isinstance(root.right, UnaryOperators.Rename)
        assert isinstance(root.right.target, UnaryOperators.Rename)
        assert isinstance(root.right.target.target, RAOperand) and root.right.target.target.name == 'banned_users'

        assert con.execute_ra(root) == [
            ('Bob', 2, 2, 'Bob'),
            ('Bob', 2, 4, 'David'),
            ('Charlie', 3, 2, 'Bob'),
            ('Charlie', 3, 4, 'David')
        ]

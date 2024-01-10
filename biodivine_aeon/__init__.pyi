from typing import TypeAlias, Literal, Callable, Sequence, TypedDict, NotRequired

class BddVariable:
    def __init__(self, value: int = 0) -> None:
        """
        Construct a new `BddVariable` using an `int` index of the variable.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __lt__(self, other) -> bool:
        ...
    def __le__(self, other) -> bool:
        ...
    def __gt__(self, other) -> bool:
        ...
    def __ge__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __getnewargs__(self) -> tuple[int]:
        ...

class BddPointer:

    def __init__(self, value: bool | int | None = None) -> None:
        """
        Construct a new `BddPointer` using either a `bool` value, or an exact `int` index.

        If no value is given, defaults to `BddPointer.zero`.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __lt__(self, other) -> bool:
        ...
    def __le__(self, other) -> bool:
        ...
    def __gt__(self, other) -> bool:
        ...
    def __ge__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __getnewargs__(self) -> tuple[int]:
        ...
    @staticmethod
    def zero() -> BddPointer:
        ...
    @staticmethod
    def one() -> BddPointer:
        ...
    def is_zero(self) -> bool:
        ...
    def is_one(self) -> bool:
        ...
    def is_terminal(self) -> bool:
        ...
    def as_bool(self) -> bool | None:
        ...

class BddVariableSetBuilder:
    def __init__(self, variables: list[str] | None = None) -> None:
        """
        Create a new `BddVariableSetBuilder`, optionally initialized with the given list of variables.
        """
    def __eq__(self, other) -> bool:
            ...
    def __ne__(self, other) -> bool:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getstate__(self) -> list[str]:
        ...
    def __setstate__(self, state: list[str]):
        ...
    def add(self, name: str) -> BddVariable:
        ...
    def add_all(self, names: list[str]) -> list[BddVariable]:
        ...
    def build(self) -> BddVariableSet:
        ...


class BddVariableSet:
    def __init__(self, variables: int | list[str]):
        """
        A `BddVariableSet` is typically created using a list of variable names. However, you can also create
        an "anonymous" `BddVariableSet` using a variable count `n`. In such a case, the variables are automatically
        named $(x_0, \ldots, x_{n-1})$.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __len__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> tuple[list[str]]:
        ...
    def variable_count(self) -> int:
        ...
    def variable_ids(self) -> list[BddVariable]:
        ...
    def variable_names(self) -> list[str]:
        ...
    def find_variable(self, variable: BddVariableType) -> BddVariable | None:
        ...
    def get_variable_name(self, variable: BddVariableType) -> str:
        ...
    def mk_false(self) -> Bdd:
        ...
    def mk_true(self) -> Bdd:
        ...
    def mk_const(self, value: BoolType) -> Bdd:
        ...
    def mk_literal(self, variable: BddVariableType, value: BoolType) -> Bdd:
        ...
    def mk_conjunctive_clause(self, clause: BoolClauseType) -> Bdd:
        ...
    def mk_disjunctive_clause(self, clause: BoolClauseType) -> Bdd:
        ...
    def mk_cnf(self, clauses: Sequence[BoolClauseType]) -> Bdd:
        ...
    def mk_dnf(self, clauses: Sequence[BoolClauseType]) -> Bdd:
        ...
    def mk_sat_exactly_k(self, k: int, variables: list[BddVariableType] | None) -> Bdd:
        ...
    def mk_sat_up_to_k(self, k: int, variables: list[BddVariableType] | None) -> Bdd:
        ...
    def eval_expression(self, expression: BoolExpressionType) -> Bdd:
        ...
    def transfer_from(self, value: Bdd, original_ctx: BddVariableSet) -> Bdd | None:
        ...


class Bdd:
    def __init__(self,
         ctx: Bdd | BddValuation | BddPartialValuation | BddVariableSet,
         data: None | bytes | str = None
    ) -> Bdd:
        """
        A `Bdd` can be created as:
         - A copy of a different `Bdd`.
         - A conjunction of literals defined by a `BddValuation` or a `BddPartialValuation`.
         - Deserialization of a string created with `Bdd.data_string()`.
         - Deserialization of bytes created with `Bdd.data_bytes()`.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __lt__(self, other) -> bool:
        ...
    def __le__(self, other) -> bool:
        ...
    def __gt__(self, other) -> bool:
        ...
    def __ge__(self, other) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> tuple[BddVariableSet, bytes]:
        ...
    def __ctx__(self) -> BddVariableSet:
        ...
    def __call__(self, valuation: BddValuation | list[BoolType]) -> bool:
        ...
    def __len__(self) -> int:
        ...
    def data_string(self) -> str:
        ...
    def data_bytes(self) -> bytes:
        ...
    def to_dot(self, zero_pruned: bool = True) -> str:
        ...
    def to_expression(self) -> BooleanExpression:
        ...
    def to_dnf(self) -> list[BddPartialValuation]:
        ...
    def to_cnf(self) -> list[BddPartialValuation]:
        ...
    def node_count(self) -> int:
        ...
    def node_count_per_variable(self) -> dict[BddVariable, int]:
        ...
    def structural_eq(self, other: Bdd) -> bool:
        ...
    def semantic_eq(self, other: Bdd) -> bool:
        ...
    def implies(self, other: Bdd) -> bool:
        ...
    def root(self) -> BddPointer:
        ...
    def node_links(self, pointer: BddPointer) -> tuple[BddPointer, BddPointer]:
        ...
    def node_variable(self, pointer: BddPointer) -> None | BddVariable:
        ...
    def variable_count(self) -> int:
        ...
    def support_set(self) -> set[BddVariable]:
        ...
    def is_false(self) -> bool:
        ...
    def is_true(self) -> bool:
        ...
    def is_clause(self) -> bool:
        ...
    def is_valuation(self) -> bool:
        ...
    def cardinality(self, exact: bool = True) -> int:
        ...
    def l_not(self) -> Bdd:
        ...
    def l_and(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    def l_or(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    def l_imp(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    def l_iff(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    def l_xor(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    def l_and_not(self, other: Bdd, limit: int | None = None) -> Bdd:
        ...
    @staticmethod
    def if_then_else(
            condition: Bdd,
            then: Bdd,
            other: Bdd,
    ) -> Bdd:
        ...
    @staticmethod
    def apply2(
        left: Bdd,
        right: Bdd,
        function: Callable[[None | bool, None | bool], None | bool],
        flip_left: None | BddVariable | str = None,
        flip_right: None | BddVariable | str = None,
        flip_output: None | BddVariable | str = None,
        limit: None | int = None
    ) -> Bdd:
        ...
    @staticmethod
    def apply3(
        a: Bdd,
        b: Bdd,
        c: Bdd,
        function: Callable[[None | bool, None | bool, None | bool], None | bool],
        flip_a: None | BddVariable | str = None,
        flip_b: None | BddVariable | str = None,
        flip_c: None | BddVariable | str = None,
        flip_out: None | BddVariable | str = None
    ) -> Bdd:
        ...
    @staticmethod
    def check2(
        left: Bdd,
        right: Bdd,
        function: Callable[[None | bool, None | bool], None | bool],
        flip_left: None | BddVariable | str = None,
        flip_right: None | BddVariable | str = None,
        flip_output: None | BddVariable | str = None
    ) -> tuple[bool, int]:
        ...
    @staticmethod
    def apply_nested(
        left: Bdd,
        right: Bdd,
        variables: list[BddVariableType],
        outer_function: Callable[[None | bool, None | bool], None | bool],
        inner_function: Callable[[None | bool, None | bool], None | bool],
    ) -> Bdd:
        ...
    @staticmethod
    def apply_with_exists(
            left: Bdd,
            right: Bdd,
            variables: list[BddVariableType],
            function: Callable[[None | bool, None | bool], None | bool],
    ) -> Bdd:
        ...
    @staticmethod
    def apply_with_for_all(
            left: Bdd,
            right: Bdd,
            variables: list[BddVariableType],
            function: Callable[[None | bool, None | bool], None | bool],
    ) -> Bdd:
        ...
    def r_pick(self, variables: BddVariableType | list[BddVariableType]) -> Bdd:
        ...
    def r_pick_random(self, variables: BddVariableType | list[BddVariableType], seed: int | None = None) -> Bdd:
        ...
    def r_exist(self, variables: BddVariableType | list[BddVariableType]) -> Bdd:
        ...
    def r_for_all(self, variables: BddVariableType | list[BddVariableType]) -> Bdd:
        ...
    def r_restrict(self, values: BoolClauseType) -> Bdd:
        ...
    def r_select(self, values: BoolClauseType) -> Bdd:
        ...
    def witness(self) -> BddValuation | None:
        ...
    def valuation_first(self) -> BddValuation | None:
        ...
    def valuation_last(self) -> BddValuation | None:
        ...
    def valuation_random(self, seed: int | None = None) -> BddValuation | None:
        ...
    def valuation_most_positive(self) -> BddValuation | None:
        ...
    def valuation_most_negative(self) -> BddValuation | None:
        ...
    def valuation_iterator(self) -> BddValuationIterator:
        ...
    def clause_first(self) -> BddPartialValuation | None:
        ...
    def clause_last(self) -> BddPartialValuation | None:
        ...
    def clause_random(self, seed: int | None = None) -> BddPartialValuation | None:
        ...
    def clause_necessary(self) -> BddPartialValuation | None:
        ...
    def clause_iterator(self) -> BddClauseIterator:
        ...
    def substitute(self, variable: BddVariableType, function: Bdd) -> Bdd:
        ...
    def rename(self, replace_with: list[tuple[BddVariableType, BddVariableType]]) -> Bdd:
        ...

class BddValuationIterator:
    def __init__(self, bdd: Bdd):
        """
        Create a new iterator over all satisfying `BddValuation` objects of a `Bdd`.
        """
    def __iter__(self) -> BddValuationIterator:
        ...
    def __next__(self) -> BddValuation:
        ...

class BddClauseIterator:
    def __init__(self, bdd: Bdd):
        """
        Create a new iterator over all DNF clauses (i.e. `BddPartialValuation` objects) of a `Bdd`.
        """
    def __iter__(self) -> BddClauseIterator:
        ...
    def __next__(self) -> BddPartialValuation:
        ...

class BddPartialValuation:
    def __init__(self,
        ctx: BddValuation | BddPartialValuation | BddVariableSet,
        values: None | dict[BddVariableType, BoolType] = None
    ) -> BddPartialValuation:
        """
        A `BddPartialValuation` can be created as:
         - A copy of a `BddValuation`.
         - A copy of a `BddPartialValuation`.
         - From a `BddVariableSet` "context" and a `dict[BddVariableType, BoolType]` dictionary, assuming the
         dictionary only contains variables that are valid in the provided context.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> tuple[BddVariableSet, dict[BddVariable, bool]]:
        ...
    def __ctx__(self) -> BddVariableSet:
        ...
    def __len__(self) -> int:
        ...
    def __getitem__(self, key: BddVariableType) -> bool | None:
        ...
    def __setitem__(self, key: BddVariableType, value: BoolType | None) -> None:
        ...
    def __delitem__(self, key: BddVariableType) -> None:
        ...
    def __contains__(self, key: BddVariableType) -> bool:
        ...
    def keys(self) -> list[BddVariable]:
        ...
    def values(self) -> list[bool]:
        ...
    def items(self) -> list[tuple[BddVariable, bool]]:
        ...
    def to_dict(self) -> dict[BddVariable, bool]:
        ...
    def extends(self, other: BddPartialValuation) -> bool:
        ...
    def support_set(self) -> set[BddVariable]:
        ...

class BddValuation:
    def __init__(self,
         ctx: BddValuation | BddPartialValuation | BddVariableSet,
         values: None | list[BoolType] = None,
    ):
        """
        A `BddValuation` can be created as:
         - A copy of a different `BddValuation`.
         - A copy of a `BddPartialValuation`, assuming it specifies the
           values of all relevant variables.
         - From a list of `BoolType` values, as long as its length is exactly
           the variable count.
        """
    def __hash__(self) -> int:
        ...
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> tuple[BddVariableSet, list[bool]]:
        ...
    def __ctx__(self) -> BddVariableSet:
        ...
    def __len__(self) -> int:
        ...
    def __getitem__(self, key: BddVariableType) -> bool:
        ...
    def __setitem__(self, key: BddVariableType, value: BoolType) -> None:
        ...
    def __contains__(self, key: BddVariableType) -> bool:
        ...
    def keys(self) -> list[BddVariable]:
        ...
    def values(self) -> list[bool]:
        ...
    def items(self) -> list[tuple[BddVariable, bool]]:
        ...
    def extends(self, valuation: BddPartialValuation) -> bool:
        ...

class BooleanExpression:
    def __init__(self, value: BooleanExpression | str):
        """
        Build a new `BooleanExpression`, either as a copy of an existing expression, or from a string representation.
        """
    def __hash__(self) -> int:
        ...
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> str:
        ...
    def __root__(self) -> BooleanExpression:
        ...
    def __call__(self,
                 valuation: None | dict[str, int] | dict[str, bool] = None,
                 **kwargs: int | bool
    ) -> bool:
        ...
    @staticmethod
    def mk_const(value: bool | int) -> BooleanExpression:
        ...
    @staticmethod
    def mk_var(name: str) -> BooleanExpression:
        ...
    @staticmethod
    def mk_not(value: BooleanExpression) -> BooleanExpression:
        ...
    @staticmethod
    def mk_and(left: BooleanExpression, right: BooleanExpression) -> BooleanExpression:
        ...
    @staticmethod
    def mk_or(left: BooleanExpression, right: BooleanExpression) -> BooleanExpression:
        ...
    @staticmethod
    def mk_imp(left: BooleanExpression, right: BooleanExpression) -> BooleanExpression:
        ...
    @staticmethod
    def mk_iff(left: BooleanExpression, right: BooleanExpression) -> BooleanExpression:
        ...
    @staticmethod
    def mk_xor(left: BooleanExpression, right: BooleanExpression) -> BooleanExpression:
        ...
    def is_const(self) -> bool:
        ...
    def is_var(self) -> bool:
        ...
    def is_not(self) -> bool:
        ...
    def is_and(self) -> bool:
        ...
    def is_or(self) -> bool:
        ...
    def is_imp(self) -> bool:
        ...
    def is_iff(self) -> bool:
        ...
    def is_xor(self) -> bool:
        ...
    def is_literal(self) -> bool:
        ...
    def is_binary(self) -> bool:
        ...
    def as_const(self) -> bool | None:
        ...
    def as_var(self) -> str | None:
        ...
    def as_not(self) -> BooleanExpression | None:
        ...
    def as_and(self) -> tuple[BooleanExpression, BooleanExpression] | None:
        ...
    def as_or(self) ->  tuple[BooleanExpression, BooleanExpression] | None:
        ...
    def as_imp(self) -> tuple[BooleanExpression, BooleanExpression] | None:
        ...
    def as_iff(self) -> tuple[BooleanExpression, BooleanExpression] | None:
        ...
    def as_xor(self) -> tuple[BooleanExpression, BooleanExpression] | None:
        ...
    def as_literal(self) -> tuple[str, bool] | None:
        ...
    def as_binary(self) -> tuple[str, BooleanExpression, BooleanExpression] | None:
        ...
    def support_set(self) -> set[str]:
        ...

class VariableId:
    def __init__(self, value: int = 0) -> None:
        """
        Construct a new `VariableId` using an `int` index of the variable.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __lt__(self, other) -> bool:
        ...
    def __le__(self, other) -> bool:
        ...
    def __gt__(self, other) -> bool:
        ...
    def __ge__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __getnewargs__(self) -> tuple[int]:
        ...

class ParameterId:
    def __init__(self, value: int = 0) -> None:
        """
        Construct a new `ParameterId` using an `int` index of the variable.
        """
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __lt__(self, other) -> bool:
        ...
    def __le__(self, other) -> bool:
        ...
    def __gt__(self, other) -> bool:
        ...
    def __ge__(self, other) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __getnewargs__(self) -> tuple[int]:
        ...

class RegulatoryGraph:
    def __init__(self,
                 variables: None | list[str] = None,
                 regulations: None | list[NamedRegulation] | list[str] = None
    ) -> RegulatoryGraph:
        """
        A `RegulatoryGraph` can be constructed from two optional arguments:
         - A list of variable names. If this list is not given, it is inferred from the list of regulations.
         - A list of regulations. These can be either `NamedRegulation` dictionaries, or string objects compatible
           with the `.aeon` format notation.

        If you don't provide any arguments, an "empty" `RegulatoryGraph` is constructed with no variables
        and no regulations.
        """
    def __str__(self) -> str:
        ...
    def __eq__(self, other) -> bool:
        ...
    def __ne__(self, other) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __getnewargs__(self) -> tuple[list[str], list[str]]:
        ...
    def __copy__(self) -> RegulatoryGraph:
        ...
    def __deepcopy__(self, memo: dict) -> RegulatoryGraph:
        ...
    @staticmethod
    def from_file(file_path: str) -> RegulatoryGraph:
        ...
    @staticmethod
    def from_aeon(file_content: str) -> RegulatoryGraph:
        ...
    def to_aeon(self) -> str:
        ...
    def to_dot(self) -> str:
        ...
    def variable_count(self) -> int:
        ...
    def variable_names(self) -> list[str]:
        ...
    def variables(self) -> list[int]:
        ...
    def find_variable(self, variable: VariableIdType) -> None | VariableId:
        ...
    def get_variable_name(self, variable: VariableIdType) -> str:
        ...
    def set_variable_name(self, variable: VariableIdType, name: str) -> None:
        ...
    def regulation_count(self) -> int:
        ...
    def regulations(self) -> list[IdRegulation]:
        ...
    def regulation_strings(self) -> list[str]:
        ...
    def find_regulation(self, source: VariableIdType, target: VariableIdType) -> None | IdRegulation:
        ...
    def add_regulation(self, regulation: NamedRegulation | IdRegulation | str) -> None:
        ...
    def remove_regulation(self, source: VariableIdType, target: VariableIdType) -> IdRegulation:
        ...
    def ensure_regulation(self, regulation: NamedRegulation | IdRegulation | str) -> None | IdRegulation:
        ...
    def extend(self, variables: list[str]) -> RegulatoryGraph:
        ...
    def drop(self, variables: VariableIdType | list[VariableIdType] | set[VariableIdType]) -> RegulatoryGraph:
        ...
    def inline_variable(self, variable: VariableIdType) -> RegulatoryGraph:
        ...
    def predecessors(self, variable: VariableIdType) -> set[VariableId]:
        ...
    def successors(self, variable: VariableIdType) -> set[VariableId]:
        ...
    def backward_reachable(self, pivots: VariableIdType | VariableCollection, subgraph: VariableCollection | None = None) -> set[VariableId]:
        ...
    def forward_reachable(self, pivots: VariableIdType | VariableCollection, subgraph: VariableCollection | None = None) -> set[VariableId]:
        ...
    def feedback_vertex_set(self, parity: SignType | None = None, subgraph: VariableCollection | None = None) -> set[VariableId]:
        ...
    def independent_cycles(self, parity: SignType | None = None, subgraph: VariableCollection | None = None) -> list[list[VariableId]]:
        ...
    def strongly_connected_components(self, subgraph: VariableCollection | None = None) -> list[set[VariableId]]:
        ...
    def weakly_connected_components(self, subgraph: VariableCollection | None = None) -> list[set[VariableId]]:
        ...
    def shortest_cycle(self,
                       pivot: VariableIdType,
                       parity: SignType | None = None,
                       subgraph: VariableCollection | None = None,
                       length: int | None = None
    ) -> list[VariableId] | None:
        ...



BddVariableType: TypeAlias = BddVariable | str
VariableIdType: TypeAlias = VariableId | str
ParameterIdType: TypeAlias = ParameterId | str
BoolType: TypeAlias = Literal[0, 1] | bool
SignType: TypeAlias = Literal["positive", "+", "negative", "-"] | bool
VariableCollection: TypeAlias = list[str] | list[VariableId] | set[str] | set[VariableId]
DynamicValuation: TypeAlias = dict[BddVariable, bool] | dict[BddVariable, Literal[0,1]] | dict[str, bool] | dict[str, Literal[0,1]]
BoolClauseType: TypeAlias = BddPartialValuation | BddValuation | DynamicValuation
BoolExpressionType: TypeAlias = BooleanExpression | str
class NamedRegulation(TypedDict):
    source: str
    target: str
    sign: NotRequired[SignType]
    essential: NotRequired[BoolType]
class IdRegulation(TypedDict):
    source: VariableId
    target: VariableId
    sign: NotRequired[SignType]
    essential: NotRequired[BoolType]
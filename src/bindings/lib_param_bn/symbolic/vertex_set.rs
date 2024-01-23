use crate::bindings::lib_bdd::bdd::Bdd;
use crate::bindings::lib_param_bn::symbolic::symbolic_context::SymbolicContext;
use crate::AsNative;
use biodivine_lib_bdd::Bdd as RsBdd;
use biodivine_lib_param_bn::biodivine_std::traits::Set;
use biodivine_lib_param_bn::symbolic_async_graph::GraphVertices;
use num_bigint::BigInt;
use pyo3::basic::CompareOp;
use pyo3::prelude::*;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::ops::Not;

/// A symbolic representation of a set of "vertices", i.e. valuations of variables
/// of a particular `BooleanNetwork`.
#[pyclass(module = "biodivine_aeon", frozen)]
#[derive(Clone)]
pub struct VertexSet {
    ctx: Py<SymbolicContext>,
    native: GraphVertices,
}

impl AsNative<GraphVertices> for VertexSet {
    fn as_native(&self) -> &GraphVertices {
        &self.native
    }

    fn as_native_mut(&mut self) -> &mut GraphVertices {
        &mut self.native
    }
}

#[pymethods]
impl VertexSet {
    /// Normally, a new `VertexSet` is derived using an `AsynchronousGraph`. However, in some
    /// cases you may want to create it manually from a `SymbolicContext` and a `Bdd`.
    ///
    /// Just keep in mind that this method does not check that the provided `Bdd` is semantically
    /// a valid set of vertices.
    #[new]
    pub fn new(py: Python, ctx: Py<SymbolicContext>, bdd: &Bdd) -> Self {
        Self {
            ctx: ctx.clone(),
            native: GraphVertices::new(bdd.as_native().clone(), ctx.borrow(py).as_native()),
        }
    }

    fn __richcmp__(&self, py: Python, other: &Self, op: CompareOp) -> Py<PyAny> {
        match op {
            CompareOp::Eq => VertexSet::semantic_eq(self, other).into_py(py),
            CompareOp::Ne => VertexSet::semantic_eq(self, other).not().into_py(py),
            _ => py.NotImplemented(),
        }
    }

    fn __str__(&self) -> String {
        format!(
            "VertexSet(cardinality={}, symbolic_size={})",
            self.cardinality(),
            self.symbolic_size(),
        )
    }

    fn __repr__(&self) -> String {
        format!(
            "VertexSet(cardinality={}, symbolic_size={})",
            self.cardinality(),
            self.symbolic_size(),
        )
    }

    fn __copy__(self_: Py<Self>) -> Py<Self> {
        self_.clone()
    }

    fn __deepcopy__(self_: Py<Self>, _memo: &PyAny) -> Py<Self> {
        self_.clone()
    }

    fn __hash__(&self) -> u64 {
        let mut hasher = DefaultHasher::new();
        self.as_native().hash(&mut hasher);
        hasher.finish()
    }

    /// Returns the number of vertices that are represented in this set.
    pub fn cardinality(&self) -> BigInt {
        self.as_native().exact_cardinality()
    }

    /// Set intersection.
    fn intersect(&self, other: &Self) -> Self {
        self.mk_derived(self.as_native().intersect(other.as_native()))
    }

    /// Set difference.
    fn minus(&self, other: &Self) -> Self {
        self.mk_derived(self.as_native().minus(other.as_native()))
    }

    /// Set union.
    fn union(&self, other: &Self) -> Self {
        self.mk_derived(self.as_native().union(other.as_native()))
    }

    /// True if this set is empty.
    fn is_empty(&self) -> bool {
        self.as_native().is_empty()
    }

    /// True if this set is a subset of the other set.
    ///
    /// Should be faster than just calling `set.minus(superset).is_empty()`
    fn is_subset(&self, other: &Self) -> bool {
        self.as_native().is_subset(other.as_native())
    }

    /// True if this set is a singleton, i.e. a single function interpretation.
    fn is_singleton(&self) -> bool {
        self.as_native().is_singleton()
    }

    /// True if this set is a subspace, i.e. it can be expressed using a single conjunctive clause.
    fn is_subspace(&self) -> bool {
        self.as_native().is_subspace()
    }

    /// Deterministically pick a subset of this set that contains exactly a single vertex.
    ///
    /// If this set is empty, the result is also empty.
    fn pick_singleton(&self) -> Self {
        self.mk_derived(self.as_native().pick_singleton())
    }

    /// The number of `Bdd` nodes that are used to represent this set.
    fn symbolic_size(&self) -> usize {
        self.as_native().symbolic_size()
    }

    /// Obtain the underlying `Bdd` of this `VertexSet`.
    fn to_bdd(&self, py: Python) -> Bdd {
        let rs_bdd = self.as_native().as_bdd().clone();
        let ctx = self.ctx.borrow(py);
        Bdd::new_raw_2(ctx.bdd_variable_set(), rs_bdd)
    }
}

impl VertexSet {
    pub fn mk_native(ctx: Py<SymbolicContext>, native: GraphVertices) -> Self {
        Self { ctx, native }
    }

    pub fn mk_derived(&self, native: GraphVertices) -> Self {
        Self {
            ctx: self.ctx.clone(),
            native,
        }
    }

    pub fn semantic_eq(a: &Self, b: &Self) -> bool {
        let a = a.as_native().as_bdd();
        let b = b.as_native().as_bdd();
        if a.num_vars() != b.num_vars() {
            return false;
        }

        RsBdd::binary_op_with_limit(1, a, b, biodivine_lib_bdd::op_function::xor).is_some()
    }
}

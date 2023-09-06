use crate::bindings::lib_param_bn::{
    PyBooleanNetwork, PyGraphColoredVertices, PySymbolicAsyncGraph,
};
use biodivine_hctl_model_checker::analysis::{analyse_formula, analyse_formulae};
use biodivine_hctl_model_checker::mc_utils::get_extended_symbolic_graph;
use biodivine_hctl_model_checker::model_checking::{model_check_tree, model_check_trees};
use biodivine_hctl_model_checker::preprocessing::node::HctlTreeNode;
use biodivine_hctl_model_checker::preprocessing::parser::parse_and_minimize_hctl_formula;
use biodivine_hctl_model_checker::result_print::PrintOptions;
use biodivine_lib_param_bn::BooleanNetwork;

use crate::{throw_runtime_error, throw_type_error, AsNative};

use macros::Wrapper;
use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::PyResult;

mod _impl_hctl_tree_node;

pub(crate) fn register(module: &PyModule) -> PyResult<()> {
    module.add_class::<PyHctlTreeNode>()?;

    module.add_function(wrap_pyfunction!(get_extended_stg, module)?)?;
    module.add_function(wrap_pyfunction!(model_check, module)?)?;
    module.add_function(wrap_pyfunction!(model_check_multiple, module)?)?;
    module.add_function(wrap_pyfunction!(mc_analysis, module)?)?;
    module.add_function(wrap_pyfunction!(mc_analysis_multiple, module)?)?;
    Ok(())
}

/// Structure for a HCTL formula syntax tree.
#[pyclass(name = "HctlTreeNode")]
#[derive(Clone, Debug, Eq, Hash, PartialEq, Wrapper)]
pub struct PyHctlTreeNode(HctlTreeNode);

#[pyfunction]
/// Create an extended symbolic transition graph that supports the number of needed HCTL variables.
pub fn get_extended_stg(
    bn: PyBooleanNetwork,
    num_hctl_vars: u16,
) -> PyResult<PySymbolicAsyncGraph> {
    match get_extended_symbolic_graph(&bn.as_native().clone(), num_hctl_vars) {
        Ok(result) => Ok(result.into()),
        Err(error) => throw_runtime_error(error),
    }
}

impl PyHctlTreeNode {
    /// Try to read a HCTL tree node from a dynamic Python type. This can be either:
    ///
    ///  - `PyHctlTreeNode` itself;
    ///  - A string that will be parsed as a HCTL formula.
    pub(crate) fn from_python(any: &PyAny, network: &BooleanNetwork) -> PyResult<PyHctlTreeNode> {
        if let Ok(val) = any.extract::<PyHctlTreeNode>() {
            Ok(val)
        } else if let Ok(string) = any.extract::<String>() {
            let parsed = parse_and_minimize_hctl_formula(network, string.as_str());
            match parsed {
                Err(e) => throw_runtime_error(e),
                Ok(tree) => Ok(PyHctlTreeNode::from(tree)),
            }
        } else {
            throw_type_error("Expected a HCTL formula or a HCTL tree node.")
        }
    }
}

#[pyfunction]
/// Run the model checking algorithm on a HCTL formula ([String] or [PyHctlTreeNode]).
///
/// Returns a satisfying color-state relation.
pub fn model_check(
    formula: &PyAny,
    stg: &PySymbolicAsyncGraph,
) -> PyResult<PyGraphColoredVertices> {
    let stg = stg.as_native();
    let formula = PyHctlTreeNode::from_python(formula, stg.as_network())?;
    match model_check_tree(formula.into(), stg) {
        Ok(result) => Ok(result.into()),
        Err(error) => throw_runtime_error(error),
    }
}

#[pyfunction]
/// Run the model checking algorithm on a list of HCTL formulae (each formula can be a [String]
/// or a [HctlTreeNode]).
///
/// Returns a list of satisfying color-state relations, one for each formula.
pub fn model_check_multiple(
    formulae: &PyList,
    stg: &PySymbolicAsyncGraph,
) -> PyResult<Vec<PyGraphColoredVertices>> {
    let stg = stg.as_native();
    let mut list: Vec<HctlTreeNode> = Vec::new();
    for formula in formulae {
        list.push(PyHctlTreeNode::from_python(formula, stg.as_network())?.into());
    }
    match model_check_trees(list, stg) {
        Ok(results) => Ok(results.into_iter().map(|r| r.into()).collect()),
        Err(error) => throw_runtime_error(error),
    }
}

#[pyfunction]
/// Run the whole model checking analysis pipeline on a single formula.
pub fn mc_analysis(bn: PyBooleanNetwork, formula: String) -> PyResult<()> {
    let result = analyse_formula(&bn.as_native().clone(), formula, PrintOptions::WithProgress);
    match result {
        Ok(()) => Ok(()),
        Err(e) => throw_runtime_error(e),
    }
}

#[pyfunction]
/// Run the whole model checking analysis pipeline on a list of several (individual) formulae.
pub fn mc_analysis_multiple(bn: PyBooleanNetwork, formulae: Vec<String>) -> PyResult<()> {
    let result = analyse_formulae(
        &bn.as_native().clone(),
        formulae,
        PrintOptions::WithProgress,
    );
    match result {
        Ok(()) => Ok(()),
        Err(e) => throw_runtime_error(e),
    }
}

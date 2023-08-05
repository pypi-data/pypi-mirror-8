"""
Linear programming (LP) library for combinatorial search.
Requires the PuLP library.
"""

import pulp
import pydecode
from collections import defaultdict


class HypergraphLP:
    """
    Manages the linear program for a hypergraph search problem.

    Attributes
    -----------

    objective : float
       Get the objective of the solved LP.

    path : The hyperpath (if ILP)
       Get the hyperpath of the solved ILP.

    edge_variables : Dict of edge values.
       Get the (fractional) path of the solved LP.

    """

    def __init__(self, lp, hypergraph, node_vars, edge_vars,
                 label_vars,
                 integral=False):
        r"""
        Initialize the Hypergraph LP.

        Call with HypergraphLP.make_lp().

        Parameters
        ------------

        lp : PuLP linear program
           The linear program for the hypergraph

        hypergraph : :py:class:`Hypergraph`
           The hypergraph.

        node_vars : map of Node to LP variable.
           The node variables :math:`y(v)`
           for all :math:`v \in {\cal V}`.

        edge_vars : map of Edge to LP variable.
           The hyperedge variables :math:`y(e)`
           for all :math:`e \in {\cal E}`.

        label_vars :

        integral : bool
        """

        self.lp = lp
        self.hypergraph = hypergraph
        self.node_vars = node_vars
        self.edge_vars = edge_vars
        self.integral = integral
        self.label_vars = label_vars

    def solve(self, solver=None):
        r"""
        Solve the underlying hypergraph linear program
        and return the best path.

         :math:`\arg \max_{y \in {\cal X}} \theta^{\top}y`.

        Parameters
        ----------

        solver : LP solver
           A PuLP LP solver (glpsol, Gurobi, etc.).
        """
        if solver is None:
            _solver = pulp.solvers.GLPK(msg=0)
        else:
            _solver = solver
        self._status = self.lp.solve(_solver)

    @property
    def path(self):
        if self._status != pulp.LpStatusOptimal:
            raise Exception("No optimal solution.")
        else:
            path_edges = [edge
                          for edge in self.hypergraph.edges
                          if pulp.value(self.edge_vars[edge.id]) == 1.0]
            return pydecode.Path(self.hypergraph, path_edges)

    @property
    def objective(self):
        return pulp.value(self.lp.objective)

    @property
    def edge_variables(self):
        return {edge: pulp.value(self.edge_vars[edge.id])
                for edge in self.hypergraph.edges
                if pulp.value(self.edge_vars[edge.id]) > 0.0}

    def decode_fractional(self):
        vec = [pulp.value(self.edge_vars[edge.id])
               for edge in self.hypergraph.edges]
        weights = pydecode.LogViterbiPotentials(self.hypergraph).from_vector(vec)
        return pydecode.best_path(self.hypergraph, weights)

    # def add_constraints(self, constraints):
    #     """
    #     Add hard constraints to the hypergraph.

    #     Parameters
    #     -----------

    #     constraints : :py:class:`Constraints`
    #     """
    #     for i, constraint in enumerate(constraints):
    #         self.lp += 0 == \
    #             constraints.bias[i, 0] + \
    #             pulp.lpSum([coeff * self.edge_vars[edge.id]
    #                         for (coeff, edge) in constraint])

    @staticmethod
    def make_lp(hypergraph, potentials, name="", integral=False):
        r"""
        Construct a linear program from a hypergraph.

        .. math::

          \max & \theta^{\top} x \\
          x(1) &= 1 \\
          x(v) &= \sum_{e \in {\cal E} : h(e) = v} x(e) \\
          x(v) &= \sum_{e \in {\cal E} : v \in t(e)} x(e)

        Parameters
        ----------

        hypergraph : :py:class:`pydecode.hyper.Hypergraph`
          The hypergraph search.


        potentials : :py:class:`pydecode.hyper.LogViterbiPotentials`
          The potentials.

        name : string
          A debugging name for linear program.

        integral : bool
          Construct as an integer linear program.

        Returns
        --------

        lp : :py:class:`HypergraphLP`
          Returns the hypergraph LP (or ILP)
        """

        if integral:
            var_type = pulp.LpInteger
        else:
            var_type = pulp.LpContinuous
        prob = pulp.LpProblem("Hypergraph Problem", pulp.LpMaximize)

        def node_name(node):
            return "node_{}".format(node.id)

        def edge_name(edge):
            return "edge_{}".format(edge.id)

        def label_name(label):
            return "label_{}".format(label)

        # Make variables for the nodes.
        node_vars = {node.id: pulp.LpVariable(node_name(node), 0, 1,
                                              var_type)
                     for node in hypergraph.nodes}

        edge_vars = {edge.id: pulp.LpVariable(edge_name(edge), 0, 1,
                                              var_type)
                     for edge in hypergraph.edges}

        # Build table of incoming edges
        in_edges = defaultdict(lambda: [])
        for edge in hypergraph.edges:
            for node in edge.tail:
                in_edges[node.id].append(edge)

        labels = defaultdict(list)
        for edge in hypergraph.edges:
            p = potentials[edge.id]
            v = edge_vars[edge.id]
            if edge.label != -1:
                labels[edge.label].append(edge.id)
        label_vars = {label: pulp.LpVariable(label_name(label), 0, 1,
                                              var_type)
                      for label in labels.keys()}


        # max \theta x
        prob += pulp.lpSum(
            [potentials[edge.id] * edge_vars[edge.id]
             for edge in hypergraph.edges])

        # x(r) = 1
        prob += node_vars[hypergraph.root.id] == 1

        # x(v) = \sum_{e : h(e) = v} x(e)
        for node in hypergraph.nodes:
            if node.is_terminal:
                continue
            prob += node_vars[node.id] == \
                pulp.lpSum((edge_vars[edge.id]
                            for edge in node.edges))

        # x(v) = \sum_{e : v \in t(e)} x(e)
        for node in hypergraph.nodes:
            if node.id == hypergraph.root.id:
                continue
            prob += node_vars[node.id] == \
                pulp.lpSum((edge_vars[edge.id]
                            for edge in in_edges[node.id]))

        for label in labels.keys():
            prob += label_vars[label] == \
                pulp.lpSum([edge_vars[edge.id]
                    for edge_id in labels[label]])

        return HypergraphLP(prob, hypergraph, node_vars,
                            edge_vars, integral)

# CSP stands for constraint satisfaction problems
# lecture 7 from into to AI
from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
V = TypeVar('V') # var type
D = TypeVar('D') # domain type

#base class for all constraints
class Constraint(Generic[V,D], ABC):
    # var that the constraint is b/t
    def __init__(self, variables : List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V,D]) -> bool:
        ...
    
class CSP (Generic[V,D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: List[D] = domains
        self.constraints: Dict[V, List[Constraint[V,D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("each var should have a domain assigned to it")

    def add_constraint(self, constraint: Constraint[V,D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def backtracking_search(self, assignment: Dict[V,D] = {}) -> Optional[Dict[V,D]]:
        # assignment is complete if every variable is assigned (ie the base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the csp ut not in the assingnment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        print (unassigned)

        # get the every possible domain value of the first unassigned variable
        first: V = unassigned[0]    # by the way calling a variable with a colon and a data type is known as type hinting its basically like how you can hint at data types in the parameters of a function.
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value

            # if we are still consistent, we recurse (aka continue)
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V,D]] = self.backtracking_search(local_assignment)
                # if we didnt find the resul, we will end up backtracking
                if result is not None:
                    return result
        return None


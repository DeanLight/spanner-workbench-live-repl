# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03a_ast_node_types.ipynb.

# %% auto 0
__all__ = ['get_term_list_string', 'RelationDeclaration', 'Relation', 'IERelation', 'AddFact', 'RemoveFact', 'Query', 'Rule',
           'Assignment', 'ReadAssignment']

# %% ../nbs/03a_ast_node_types.ipynb 4

# %% ../nbs/03a_ast_node_types.ipynb 5
from typing import List, Tuple, Set, Union, Sequence
from .primitive_types import DataTypes, DataTypeMapping, Span

# %% ../nbs/03a_ast_node_types.ipynb 6
def get_term_list_string(term_list: Sequence[DataTypeMapping.term], #the term list to be turned into a string
                         type_list: Sequence[DataTypes] #the types of the terms in term_list
                         ) -> str: #a string representation of the term list
    """
    returns a string representation of the term list.
    quotes are added to string terms so they will not be confused with variables. <br>
    @raise Exception: if length of term list doesn't match the length of type list.
    """
    if len(term_list) != len(type_list):
        raise Exception(f"received different lengths of term_list ({len(term_list)}) "
                        f"and type_list ({len(type_list)})")
        
    terms_with_quoted_strings = [f'"{term}"' if term_type is DataTypes.string
                                 else str(term)
                                 for term, term_type in zip(term_list, type_list)]
    term_list_string = ', '.join(terms_with_quoted_strings)
    return term_list_string

# %% ../nbs/03a_ast_node_types.ipynb 10
class RelationDeclaration:
    """a representation of a relation_declaration statement"""

    def __init__(self, relation_name: str, # the name of the relation.
                 type_list: Sequence[DataTypes]): # a list of the types of the terms in the relation's tuples.
        """
        @raise Exception: if there is invalid term type in term list.
        """
        self.relation_name = relation_name
        self.type_list = type_list
        
    def __str__(self) -> str:
        type_strings = []
        for term_type in self.type_list:
            if term_type is DataTypes.string:
                type_strings.append('str')
            elif term_type is DataTypes.span:
                type_strings.append('span')
            elif term_type is DataTypes.integer:
                type_strings.append('int')
            elif term_type is DataTypes.free_var_name:
                type_strings.append('free_var_name')
            else:
                raise ValueError(f"invalid term type ({term_type})")

        type_list_string = ', '.join(type_strings)
        relation_declaration_string = f"{self.relation_name}({type_list_string})"
        return relation_declaration_string

    def __repr__(self) -> str:
        return str(self)

# %% ../nbs/03a_ast_node_types.ipynb 14
class Relation:
    """a representation of a normal relation"""

    def __init__(self, relation_name: str, # the name of the relation
                 term_list: Sequence[DataTypeMapping.term], # a list of the relation terms
                 type_list: Sequence[DataTypes]): # a list of the relation term types
        """
        @raise Exception: if length of term list doesn't match the length of type list.
        """
        if len(term_list) != len(type_list):
            raise Exception(f"received different lengths of term_list ({len(term_list)}) "
                            f"and type_list ({len(type_list)})")
        self.relation_name = relation_name
        self.term_list = term_list
        self.type_list = type_list
        
    def __str__(self) -> str:
        term_list_string = get_term_list_string(self.term_list, self.type_list)
        relation_string = f"{self.relation_name}({term_list_string})"
        return relation_string

    def __repr__(self) -> str:
        return str(self)

    def get_term_list(self) -> Sequence[DataTypeMapping.term]:
        return self.term_list

    def get_type_list(self) -> Sequence[DataTypes]:
        return self.type_list

    def get_select_cols_values_and_types(self
            )-> set: # a set of constant variables that should be selected from the relation
        col_value_type = set()
        for i, (var_type, value) in enumerate(zip(self.type_list, self.term_list)):
            if var_type != DataTypes.free_var_name:
                col_value_type.add((i, value, var_type))

        return col_value_type

    def as_relation_declaration(self) -> RelationDeclaration:
        return RelationDeclaration(self.relation_name, self.type_list)

    def has_same_terms_and_types(self, other: "Relation" # The other relation to compare with
                        ) -> bool: # True if same, false otherwise
        """
        Checks only term list and type list equivalence.
        """

        return self.type_list == other.type_list and self.term_list == other.term_list

    def get_index_of_free_var(self, free_var : DataTypes.free_var_name # the free var to search for
                            ) -> int: # the index of free_var in term_list.
        """
        @raise Exception: if free_var doesn't exist in term_list.
        """

        for i, term in enumerate(self.term_list):
            if term == free_var:
                return i
            
        raise Exception(f"{free_var} doesn't exist in term_list of relation {self.relation_name}"
                        f"term_list: {self.term_list}")

# %% ../nbs/03a_ast_node_types.ipynb 21
class IERelation:
    """
    a representation of an information extraction (ie) relation.
    An information extraction relation is different than a normal relation as it is constructed from
    the results of a call to an information extraction function.

    The ie relation instructs us on how to construct it:
    * its name is the ie function we need to call
    * its input term list represents a relation where each tuple is an argument list to call the ie function with.
    * its output term list represents a relation that filters the tuples that are returned from the ie function
    calls, and matches the values inside the tuples to free variables.
    """

    def __init__(self, relation_name: str, # the name of the information extraction relation
                       input_term_list: List[DataTypeMapping.term], #a list of the input terms for the ie functiom, must be either literal values or free variables
                       input_type_list: List[DataTypes], # a list of the term types in input_term_list
                       output_term_list: List[DataTypeMapping.term], # a list of the output terms for the ie function, must be either literal values or free variables
                       output_type_list: List[DataTypes] # a list of the term types in output_term_list
                       ): 
        """
        @raise Exception: if length of in/out term list doesn't match length of in/out type_list.
        """
        if len(input_term_list) != len(input_type_list):
            raise Exception(f"received different lengths of input_term_list ({len(input_term_list)}) "
                            f"and input_type_list ({len(input_type_list)})")
        if len(output_term_list) != len(output_type_list):
            raise Exception(f"received different lengths of output_term_list ({len(output_term_list)}) "
                            f"and output_type_list ({len(output_type_list)})")
        self.relation_name = relation_name
        self.input_term_list = input_term_list
        self.output_term_list = output_term_list
        self.input_type_list = input_type_list
        self.output_type_list = output_type_list

    def __str__(self) -> str:
        input_term_list_string = get_term_list_string(self.input_term_list, self.input_type_list)
        output_term_list_string = get_term_list_string(self.output_term_list, self.output_type_list)
        ie_relation_string = f"{self.relation_name}({input_term_list_string}) -> ({output_term_list_string})"
        return ie_relation_string

    def __repr__(self) -> str:
        return str(self)

    def get_term_list(self) -> List[DataTypeMapping.term]:
        return self.input_term_list + self.output_term_list

    def get_type_list(self) -> List[DataTypes]:
        return self.input_type_list + self.output_type_list

    def has_same_terms_and_types(self, other: Relation, # Other relation to compare with
                ) -> bool: # True if everything equivalent besides name, false otherwise
        """
        Checks that everything besides names is equivalent.
        """

        return self.output_type_list == other.type_list and self.output_term_list == other.term_list

# %% ../nbs/03a_ast_node_types.ipynb 26
class AddFact(Relation):
    """
    a representation of an add_fact statement
    inherits from relation as a fact can be defined by a relation.
    """

    def __init__(self, relation_name: str, # the name of the relation
                        term_list: List[DataTypeMapping.term], # a list of the relation terms
                        type_list: Sequence[DataTypes]): # a list of the relation term types
        super().__init__(relation_name, term_list, type_list)

# %% ../nbs/03a_ast_node_types.ipynb 30
class RemoveFact(Relation):
    """
    a representation of a remove_fact statement
    inherits from relation as a fact can be defined by a relation.
    """

    def __init__(self, relation_name: str, # the name of the relation
                        term_list: List[DataTypeMapping.term], # a list of the relation terms
                        type_list: Sequence[DataTypes]): # a list of the relation term types
        super().__init__(relation_name, term_list, type_list)

# %% ../nbs/03a_ast_node_types.ipynb 34
class Query(Relation):
    """
    a representation of a query statement
    inherits from relation as a query can be defined by a relation
    """

    def __init__(self, relation_name: str, # the name of the relation
                        term_list: List[DataTypeMapping.term], # a list of the relation terms
                        type_list: Sequence[DataTypes]): # a list of the relation term types
        super().__init__(relation_name, term_list, type_list)

# %% ../nbs/03a_ast_node_types.ipynb 38
class Rule:
    """
    a representation of a rule statement.
    """

    def __init__(self,
                  head_relation: Relation, # the rule head, which is represented by a single relation
                    body_relation_list: List[Union[Relation, IERelation]], # a list of the rule body relations
                    body_relation_type_list: List[str] # a list of the rule body relations types (e.g. "relation", "ie_relation")
                    ):
        """
        @raise Exception: if length of term list doesn't match the length of type list.
        """
        if len(body_relation_list) != len(body_relation_type_list):
            raise Exception(f"received different lengths of body_relation_list ({len(body_relation_list)}) "
                            f"and body_relation_type_list ({len(body_relation_type_list)})")
        self.head_relation = head_relation
        self.body_relation_list = body_relation_list
        self.body_relation_type_list = body_relation_type_list
    
    def __str__(self) -> str:
        return f"{self.head_relation} <- {', '.join(map(str, self.body_relation_list))}"

    def __repr__(self) -> str:
        return str(self)

    def get_relations_by_type(self) -> Tuple[Set, Set]:
        """
        categorizes relations into two sets based on their types, distinguishing between regular relations and information-extraction relations.
        """
        relations, ie_relations = set(), set()
        for rel, rel_type in zip(self.body_relation_list, self.body_relation_type_list):
            if rel_type == "relation":
                relations.add(rel)
            else:
                ie_relations.add(rel)

        return relations, ie_relations

# %% ../nbs/03a_ast_node_types.ipynb 43
class Assignment:
    """
    a representation of an assignment statement.
    """

    def __init__(self, var_name: str, # the variable name to be assigned a value
                       value: DataTypeMapping.term, # the assigned value
                       value_type: DataTypes # the assigned value's type
            ):
        self.var_name = var_name
        self.value = value
        self.value_type = value_type
        
    def __str__(self) -> str:
        if self.value_type is DataTypes.string:
            # add quotes to a literal string value
            value_string = f'"{self.value}"'
        else:
            value_string = str(self.value)
        return f'{self.var_name} = {value_string}'

    def __repr__(self) -> str:
        return str(self)

# %% ../nbs/03a_ast_node_types.ipynb 47
class ReadAssignment:
    """
    a representation of a read_assignment statement.
    """

    def __init__(self, var_name: str, # the variable name to be assigned a value
                       read_arg: str, # the argument that is passed to the read() function (e.g. "some_file" in `s = read("some_file")`)
                       read_arg_type: type # the type of the argument that is passed to the read function
            ):
        if read_arg_type not in [DataTypes.string, DataTypes.var_name]:
            raise TypeError(
                f'the argument that was passed to the read() function has an unexpected type: {read_arg_type}')

        self.var_name = var_name
        self.read_arg = read_arg
        self.read_arg_type = read_arg_type
    
    def __str__(self) -> str:
        if self.read_arg_type is DataTypes.string:
            # add quotes to a literal string argument
            read_arg_string = f'"{self.read_arg}"'
        else:
            read_arg_string = str(self.read_arg)
        return f'{self.var_name} = read({read_arg_string})'

    def __repr__(self) -> str:
        return str(self)

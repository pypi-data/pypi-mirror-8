from IzVerifier.izspecs.containers.constants import *

__author__ = 'fcanas'


class ConditionDependencyGraph():
    compound_conditions = ['or', 'xor', 'and', 'not']

    def __init__(self, verifier, fail_on_undefined_vars=False, filter_claases=False):
        self.ill_defined = {}
        self.well_defined = set()
        self.verifier = verifier
        self.crefs = set((ref for ref in verifier.find_code_references('conditions')))
        self.srefs = set((ref for ref in verifier.find_specification_references('conditions')))
        self.conditions = verifier.get_container('conditions')
        self.variables = verifier.get_container('variables')
        self.drefs = self.conditions.get_keys()
        self.fail_on_undefined_vars = fail_on_undefined_vars
        self.filter_classes = filter_claases

    def all_references(self):
        srefs, specs = self.unzip(self.srefs)
        if self.filter_classes:
            crefs = self.verifier.filter_unused_classes(self.verifier.referenced_classes, self.crefs)
            crefs, sources = self.unzip(crefs)
        else:
            crefs, sources = zip(*self.crefs)
        return self.drefs | set(srefs) | set(crefs)

    def test_verify_all_dependencies(self):
        """
        For the given installer conditions, verify the dependencies for every single one of the conditions
        that are in some way referenced in specs or source.
        """

        for condition in self.all_references():
            result = self.verify_dependencies(condition)

            if result:
                self.ill_defined[condition] = result
            else:
                self.well_defined.add(condition)

        return self.ill_defined

    def test_verify_dependencies(self, cond_id, conditions):
        """
        Verifies that the given condition id is defined, and that its' dependencies and
        their transitive dependencies are all defined and valid.
        """

        if not cond_id in conditions.get_keys():
            return 1
        else:
            result = self.verify_dependencies(cond_id)
        return result

    def verify_dependencies(self, cond_id):
        """
        Performs a depth-first search of a condition's dependencies in order
        to verify that all dependencies and transitive dependencies are defined
        and valid.
        """
        undefined_paths = set()
        self._verify_dependencies(cond_id, undefined_paths, tuple())
        return undefined_paths

    def _verify_dependencies(self, cond_id, undefined_paths, current_path):
        """
        Given the soup for a condition, test that its dependencies are validly
        defined.
        """

        # Exception for izpack conditions:
        if cond_id in self.conditions.properties[WHITE_LIST]:
            return True

        # Short-circuit on well-defined conditions:
        if cond_id in self.well_defined:
            return True

        # Short-circuit ill-defined conditions:
        if cond_id in self.ill_defined.keys():
            current_path = current_path + ((cond_id, 'ill-defined condition'),)
            undefined_paths.add(current_path)
            return False

        # Cycle checking:
        tup = (cond_id, 'condition')
        if tup in current_path:
            current_path += ((cond_id, 'cyclic condition reference'),)
            undefined_paths.add(current_path)
            return False

        # Check for undefined condition.
        if not cond_id in self.conditions.get_keys():
            tup = (cond_id, 'undefined condition')
            current_path += (tup,)
            undefined_paths.add(current_path)
            return False

        current_path += (tup,)
        condition = self.conditions.container[cond_id]
        condition_type = condition['type']

        if condition_type in self.condition_tests.keys() and not \
                self.condition_tests[condition_type](self, condition, undefined_paths, current_path):
            return False

        self.well_defined.add(cond_id)
        return True

    def test_variable(self, condition, undefined_paths, current_path):
        """
        Tests if a 'variable' type condition is correctly defined.
        :param condition: the condition being tested.
        :param undefined_paths: current set of undefined paths.
        :param current_path: the current path.
        :return: True for a well-defined condition, False otherwise.
        """
        var = str(condition.find('name').text)
        if not var in self.variables.get_keys() and self.fail_on_undefined_vars:
            current_path += ((var, 'undefined variable'),)
            undefined_paths.add(current_path)
            return False
        else:
            return True

    def test_exists(self, condition, undefined_paths, current_path):
        """
        Tests if an 'exists' type condition is well-defined.
        :param condition: the condition being tested.
        :param undefined_paths: current set of undefined paths.
        :param current_path: the current path.
        :return: True for a well-defined condition, False otherwise.
        """
        var = str(condition.find('variable').text)
        if not var in self.variables.get_keys() and self.fail_on_undefined_vars:
            current_path += ((var, 'undefined variable'),)
            undefined_paths.add(current_path)
            return False
        else:
            return True

    def test_java(self, condition, undefined_paths, current_path):
        """
        Tests if a 'java' type condition is well-defined. ie, if the class that the java var is a
        field of exists.

        <condition type="java" id="myStaticFieldIsTrue">
          <java>
            <class>my.package.MyClass</class>
            <field>myStaticField</field>
          </java>
          <returnvalue type="boolean">true</returnvalue>
        </condition>

        :param condition: the condition being tested.
        :param undefined_paths: current set of undefined paths.
        :param current_path: the current path.
        :return: True for a well-defined condition, False otherwise.
        """
        cond_id = str(condition.get('id'))

        try:
            cid = str(condition.find('class').text)
        except AttributeError:
            current_path += ((cond_id, 'ill-defined java condition'),)
            undefined_paths.add(current_path)
            return False

        if not cid:
            current_path += ((cid, 'ill-defined java condition'),)
            undefined_paths.add(current_path)
            return False

        classes = self.verifier.get_container('classes').get_keys()
        if not cid in classes:
            current_path += ((cid, 'java class'),)
            undefined_paths.add(current_path)
            return False

    def test_compound(self, condition, undefined_paths, current_path):
        """
        Tests if a compound condition is well-defined: if it's children are all well-defined.
        :param condition: the condition being tested.
        :param undefined_paths: current set of undefined paths.
        :param current_path: the current path.
        :return: True for a well-defined condition, False otherwise.
        """
        defined_children = True
        dependencies = condition.find_all('condition')
        for dep in dependencies:
            did = str(dep['refid'])
            if not self._verify_dependencies(did, undefined_paths, current_path):
                defined_children = False
        return defined_children

    condition_tests = {
        'or': test_compound,
        'xor': test_compound,
        'and': test_compound,
        'not': test_compound,
        'variable': test_variable,
        'exists': test_exists,
        'java': test_java
    }

    def unzip(self, x):
        """
        Unzips a list of tuples, x.
        :param x:
        :return: Two lists if x is not empty, otherwise returns x and an empty list.
        """
        if (len(x)>0):
            return zip(*x)
        else:
            return x, list()





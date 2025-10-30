"""
Tests for CircuitOutage API serializers.
These tests validate the serializer structure by reading the source file directly.
This approach works without requiring NetBox installation.
"""

import ast
import os
import unittest


class TestCircuitOutageSerializerStructure(unittest.TestCase):
    """Test the CircuitOutageSerializer class structure"""

    def _get_serializers_file_ast(self):
        """Parse the serializers.py file and return AST"""
        serializers_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "netbox_circuitmaintenance",
            "api",
            "serializers.py",
        )
        with open(serializers_path, "r") as f:
            return ast.parse(f.read())

    def _find_class(self, tree, class_name):
        """Find a class definition in the AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        return None

    def _find_class_attr(self, class_node, attr_name):
        """Find a class attribute assignment"""
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == attr_name:
                        return node
        return None

    def _find_meta_class(self, class_node):
        """Find the Meta inner class"""
        for node in class_node.body:
            if isinstance(node, ast.ClassDef) and node.name == "Meta":
                return node
        return None

    def _get_meta_attribute(self, meta_node, attr_name):
        """Get a Meta class attribute value"""
        for node in meta_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == attr_name:
                        return node.value
        return None

    def _get_tuple_elements(self, node):
        """Extract string elements from a tuple"""
        if isinstance(node, ast.Tuple):
            return [elt.value for elt in node.elts if isinstance(elt, ast.Constant)]
        return []

    def test_circuit_outage_serializer_exists(self):
        """Test that CircuitOutageSerializer class exists"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(
            serializer_class, "CircuitOutageSerializer class should exist"
        )

    def test_circuit_outage_serializer_inherits_from_netbox_model_serializer(self):
        """Test that CircuitOutageSerializer inherits from NetBoxModelSerializer"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        # Check base classes
        base_names = [base.id for base in serializer_class.bases if hasattr(base, "id")]
        self.assertIn(
            "NetBoxModelSerializer",
            base_names,
            "CircuitOutageSerializer should inherit from NetBoxModelSerializer",
        )

    def test_circuit_outage_serializer_has_url_field(self):
        """Test that CircuitOutageSerializer has url field"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        # Look for url field assignment
        url_field = self._find_class_attr(serializer_class, "url")
        self.assertIsNotNone(
            url_field, "CircuitOutageSerializer should have a url field"
        )

    def test_circuit_outage_serializer_has_provider_field(self):
        """Test that CircuitOutageSerializer has provider field"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        # Look for provider field assignment
        provider_field = self._find_class_attr(serializer_class, "provider")
        self.assertIsNotNone(
            provider_field, "CircuitOutageSerializer should have a provider field"
        )

    def test_circuit_outage_serializer_has_meta_class(self):
        """Test that CircuitOutageSerializer has Meta class"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        meta_class = self._find_meta_class(serializer_class)
        self.assertIsNotNone(
            meta_class, "CircuitOutageSerializer should have a Meta class"
        )

    def test_circuit_outage_serializer_meta_has_model(self):
        """Test that Meta class specifies model"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        meta_class = self._find_meta_class(serializer_class)
        self.assertIsNotNone(meta_class)

        model_attr = self._get_meta_attribute(meta_class, "model")
        self.assertIsNotNone(model_attr, "Meta class should specify model attribute")

    def test_circuit_outage_serializer_meta_has_fields(self):
        """Test that Meta class specifies fields tuple"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        meta_class = self._find_meta_class(serializer_class)
        self.assertIsNotNone(meta_class)

        fields_attr = self._get_meta_attribute(meta_class, "fields")
        self.assertIsNotNone(fields_attr, "Meta class should specify fields attribute")

    def test_circuit_outage_serializer_has_required_fields(self):
        """Test that CircuitOutageSerializer includes all required fields"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "CircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        meta_class = self._find_meta_class(serializer_class)
        self.assertIsNotNone(meta_class)

        fields_attr = self._get_meta_attribute(meta_class, "fields")
        self.assertIsNotNone(fields_attr)

        # Extract field names from tuple
        field_names = self._get_tuple_elements(fields_attr)

        # Required fields based on design spec
        required_fields = {
            "id",
            "url",
            "display",
            "name",
            "summary",
            "status",
            "provider",
            "start",
            "end",
            "estimated_time_to_repair",
            "original_timezone",
            "internal_ticket",
            "acknowledged",
            "impacts",
            "notifications",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        }

        # Check that all required fields are present
        for field in required_fields:
            self.assertIn(
                field,
                field_names,
                f"Field '{field}' should be in CircuitOutageSerializer.Meta.fields",
            )


class TestNestedCircuitOutageSerializer(unittest.TestCase):
    """Test the NestedCircuitOutageSerializer class structure"""

    def _get_serializers_file_ast(self):
        """Parse the serializers.py file and return AST"""
        serializers_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "netbox_circuitmaintenance",
            "api",
            "serializers.py",
        )
        with open(serializers_path, "r") as f:
            return ast.parse(f.read())

    def _find_class(self, tree, class_name):
        """Find a class definition in the AST"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        return None

    def test_nested_circuit_outage_serializer_exists(self):
        """Test that NestedCircuitOutageSerializer class exists"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "NestedCircuitOutageSerializer")
        self.assertIsNotNone(
            serializer_class, "NestedCircuitOutageSerializer class should exist"
        )

    def test_nested_circuit_outage_serializer_inherits_from_writable_nested_serializer(
        self,
    ):
        """Test that NestedCircuitOutageSerializer inherits from WritableNestedSerializer"""
        tree = self._get_serializers_file_ast()
        serializer_class = self._find_class(tree, "NestedCircuitOutageSerializer")
        self.assertIsNotNone(serializer_class)

        # Check base classes
        base_names = [base.id for base in serializer_class.bases if hasattr(base, "id")]
        self.assertIn(
            "WritableNestedSerializer",
            base_names,
            "NestedCircuitOutageSerializer should inherit from WritableNestedSerializer",
        )


if __name__ == "__main__":
    unittest.main()

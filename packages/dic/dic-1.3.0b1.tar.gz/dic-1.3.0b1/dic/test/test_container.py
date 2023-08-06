import dic
import threading
import unittest

class Standalone(object):
    pass

class SpecialStandalone(Standalone):
    pass

class SimpleComponent(object):
    def __init__(self, s: Standalone):
        self.standalone = s


class ContainerBuilderTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = dic.container.ContainerBuilder()

    def test_build_creates_empty_container(self):
        # Arrange
        # Act
        self.builder.build()

        # Assert
        # No explosions

    def test_register_class_no_deps(self):
        # Arrange
        self.builder.register_class(Standalone)

        # Act
        container = self.builder.build()

        # Assert
        self.assertEqual(len(container.registry_map), 1)

    def test_register_class_simple_deps(self):
        # Arrange
        self.builder.register_class(SimpleComponent)

        # Act
        container = self.builder.build()

        # Assert
        self.assertEqual(len(container.registry_map), 1)

    def test_register_class_defaults_instance_per_dep(self):
        # Arrange
        self.builder.register_class(Standalone)

        # Act
        container = self.builder.build()

        # Assert
        self.assertIsInstance(container.registry_map[Standalone].component_scope, dic.scope.InstancePerDependency)

    def test_register_as_another_type(self):
        # Arrange
        self.builder.register_class(SpecialStandalone, register_as=[Standalone])

        # Act
        container = self.builder.build()

        # Assert
        self.assertIn(Standalone, container.registry_map)

    def test_register_callback(self):
        # Arrange
        self.builder.register_callback(SimpleComponent, lambda c: SimpleComponent(c.resolve(Standalone)))

        # Act
        container = self.builder.build()

        # Assert
        self.assertIn(SimpleComponent, container.registry_map)
        self.assertNotIn(Standalone, container.registry_map)


class ContainerTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = dic.container.ContainerBuilder()

    def test_resolve_simple_class(self):
        # Arrange
        self.builder.register_class(Standalone)
        container = self.builder.build()

        # Act
        x = container.resolve(Standalone)

        # Assert
        self.assertIsInstance(x, Standalone)

    def test_resolve_with_basic_dep(self):
        # Arrange
        self.builder.register_class(Standalone)
        self.builder.register_class(SimpleComponent)
        container = self.builder.build()

        # Act
        x = container.resolve(SimpleComponent)

        # Assert
        self.assertIsInstance(x, SimpleComponent)
        self.assertIsInstance(x.standalone, Standalone)

    def test_resolve_throws_with_missing_dep(self):
        # Arrange
        self.builder.register_class(SimpleComponent)
        container = self.builder.build()

        # Act
        # Assert
        with self.assertRaises(dic.container.DependencyResolutionError) as cm:
            container.resolve(SimpleComponent)

    def test_resolve_single_instance(self):
        # Arrange
        self.builder.register_class(Standalone, component_scope=dic.scope.SingleInstance)
        container = self.builder.build()

        # Act
        x = container.resolve(Standalone)
        y = container.resolve(Standalone)

        # Assert
        self.assertIs(x, y)

    def test_resolve_dep_single_instance(self):
        # Arrange
        self.builder.register_class(Standalone, component_scope=dic.scope.SingleInstance)
        self.builder.register_class(SimpleComponent)
        container = self.builder.build()

        # Act
        x = container.resolve(SimpleComponent)
        y = container.resolve(Standalone)

        # Assert
        self.assertIs(x.standalone, y)

    def test_resolve_instance_per_dep(self):
        # Arrange
        self.builder.register_class(Standalone)
        container = self.builder.build()

        # Act
        x = container.resolve(Standalone)
        y = container.resolve(Standalone)

        # Assert
        self.assertIsNot(x, y)

    def test_resolve_via_alias(self):
        # Arrange
        self.builder.register_class(SpecialStandalone, register_as=[Standalone])
        container = self.builder.build()

        # Act
        x = container.resolve(Standalone)

        # Assert
        self.assertIsInstance(x, SpecialStandalone)

    def test_resolve_with_callback(self):
        # Arrange
        standalone = Standalone()
        self.builder.register_callback(SimpleComponent, lambda c: SimpleComponent(standalone))
        container = self.builder.build()

        # Act
        component = container.resolve(SimpleComponent)

        # Assert
        self.assertIs(component.standalone, standalone)

    def test_resolve_callback_respects_scope(self):
        # Arrange
        self.builder.register_class(Standalone, component_scope=dic.scope.SingleInstance)
        self.builder.register_callback(SimpleComponent, lambda c: SimpleComponent(c.resolve(Standalone)))
        container = self.builder.build()

        # Act
        component1 = container.resolve(SimpleComponent)
        component2 = container.resolve(SimpleComponent)

        # Assert
        self.assertIsNot(component1, component2)
        self.assertIs(component1.standalone, component2.standalone)


if __name__ == '__main__':
    unittest.main()


from django.test import TestCase, Client
from nodes.models import Node
from users.models import User

class NodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Here we're assuming a User model exists and has a pk of 1.
        # Adjust according to your User model structure.
        teacher = User.objects.get(pk=1)
        manager = User.objects.get(pk=1)
        student = User.objects.get(pk=1)

        self.node = Node(name="Test Node",
                    # teachers=[teacher],
                    # managers=[manager],
                    # students=[student],
                    student_performance_labels=["test1", "test2"],
                    type="Takım",
                    isactive=True)
        self.node.save()

    def test_node_creation(self):
        node = Node.objects.first()
        self.assertEqual(node.name, "Test Node")

    def test_node_list(self):
        response = self.client.get('/nodes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'Test Node')
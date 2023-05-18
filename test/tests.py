# tests.py
import mongomock
import pytest
from rest_framework.test import APIClient
from nodes.models import Node
from nodes.api.views import NodeViewSet
from mongoengine.connection import connect, disconnect
from users.models import User

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'



@pytest.fixture(scope='function')
def db():
    disconnect(alias='default')  # disconnect the default connection if it exists
    connect('mongoenginetest', host='localhost', port=27017, mongo_client_class=mongomock.MongoClient)


@pytest.fixture(scope='function')
def test_client():
    client = APIClient()
    return client


@pytest.fixture(scope='function')
def create_node():
    # Here we're assuming a User model exists and has a pk of 1.
    # Adjust according to your User model structure.
    teacher = User.objects.get(pk=1)
    manager = User.objects.get(pk=1)
    student = User.objects.get(pk=1)

    node = Node(name="Test Node",
                teachers=[teacher],
                managers=[manager],
                students=[student],
                student_performance_labels=["test1", "test2"],
                type=Node.TEAM,
                isactive=True)
    node.save()
    return node


def test_node_creation(db, create_node):
    node = Node.objects.first()
    assert node.name == "Test Node"


def test_node_list(db, create_node, test_client):
    response = test_client.get('/nodes/')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Test Node'




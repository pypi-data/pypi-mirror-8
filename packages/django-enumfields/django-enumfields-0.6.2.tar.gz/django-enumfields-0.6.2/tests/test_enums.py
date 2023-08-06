# -- encoding: UTF-8 --

import uuid

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import connection
from django.test import Client
from django.utils.translation import ugettext_lazy
import pytest

from enumfields import Enum
from enumfields.fields import EnumIntegerField
from .models import MyModel
import six


def test_choices():
    class Color(Enum):
        __order__ = 'RED GREEN BLUE'

        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    COLOR_CHOICES = (
        ('r', 'Red'),
        ('g', 'Green'),
        ('b', 'Blue'),
    )
    assert Color.choices() == COLOR_CHOICES


def test_labels():
    class Color(Enum):
        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

        class Labels:
            RED = 'A custom label'
            BLUE = ugettext_lazy(u'bluë')

    # Custom label
    assert Color.RED.label == 'A custom label'
    assert six.text_type(Color.RED) == 'A custom label'

    # Automatic label
    assert Color.GREEN.label == 'Green'
    assert six.text_type(Color.GREEN) == 'Green'

    # Lazy label
    assert isinstance(six.text_type(Color.BLUE), six.string_types)
    assert six.text_type(Color.BLUE) == u'bluë'


@pytest.mark.django_db
def test_field_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    assert m.color == MyModel.Color.RED

    m = MyModel.objects.filter(color=MyModel.Color.RED)[0]
    assert m.color == MyModel.Color.RED


@pytest.mark.django_db
def test_db_value():
    m = MyModel(color=MyModel.Color.RED)
    m.save()
    cursor = connection.cursor()
    cursor.execute('SELECT color FROM %s WHERE id = %%s' % MyModel._meta.db_table, [m.pk])
    assert cursor.fetchone()[0] == MyModel.Color.RED.value


@pytest.fixture
def client():
    return Client()


SUPERUSER_USERNAME = "superuser"
SUPERUSER_PASS = "superpass"


@pytest.fixture
def superuser():
    return get_user_model().objects.create_superuser(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS,
                                                     email="billgates@microsoft.com")


@pytest.fixture
def superuser_client(client, superuser):
    client.login(username=SUPERUSER_USERNAME, password=SUPERUSER_PASS)
    return client


@pytest.mark.django_db
@pytest.mark.urls('tests.urls')
def test_model_admin(superuser_client):
    url = reverse("admin:tests_mymodel_add")
    secret_uuid = str(uuid.uuid4())
    response = superuser_client.post(url, follow=True, data={
        'color': 'Color.RED',
        'taste': 'Taste.UMAMI',
        'taste_int': 'Taste.SWEET',
        'random_code': secret_uuid
    })
    response.render()
    text = response.content

    assert b"This field is required" not in text
    assert b"Select a valid choice" not in text
    assert MyModel.objects.filter(random_code=secret_uuid).exists(), "Object wasn't created in the database"


def test_django_admin_lookup_value_for_integer_enum_field():
    field = EnumIntegerField(MyModel.Taste)

    assert field.get_prep_value(str(MyModel.Taste.BITTER)) == 3, "get_prep_value should be able to convert from strings"


@pytest.mark.django_db
def test_zero_enum_loads():
    # Verifies that we can save and load enums with the value of 0 (zero).
    m = MyModel(zero_field=MyModel.ZeroEnum.ZERO,
                color=MyModel.Color.GREEN)
    m.save()
    assert m.zero_field == MyModel.ZeroEnum.ZERO

    m = MyModel.objects.get(id=m.id)
    assert m.zero_field == MyModel.ZeroEnum.ZERO

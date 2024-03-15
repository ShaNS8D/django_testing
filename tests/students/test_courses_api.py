import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_first_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    url = f"/api/v1/courses/{course_id}/"
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name

@pytest.mark.django_db
def test_list_course(client, course_factory):
    course = course_factory(_quantity=10)
    url = f"/api/v1/courses/"
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    for i, m in enumerate(data):
        assert m['name'] == course[i].name

@pytest.mark.django_db
def test_filter_id_course(client, course_factory):
    course = course_factory(_quantity=10)
    url = f"/api/v1/courses/"
    response = client.get(url, data={'id': course[0].id})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course[0].id

@pytest.mark.django_db
def test_filter_name_course(client, course_factory):
    course = course_factory(_quantity=10)
    url = f"/api/v1/courses/"
    response = client.get(url, data={'name': course[0].name})
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course[0].name

@pytest.mark.django_db
def test_post_course(client):
    stedent_1 = Student.objects.create(name='s1', birth_date='2024-02-23')
    stedent_2 = Student.objects.create(name='s2', birth_date='2024-03-14')
    url = f"/api/v1/courses/"
    response = client.post(url, data={
        'name': 'course_1',
        'students': [stedent_1.id, stedent_2.id]
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_patch_course(client, course_factory):
    student = Student.objects.create(name='student_1', birth_date='1991-08-21')
    course = course_factory(_quantity=1)
    url = f"/api/v1/courses/{course[0].id}/"
    response = client.patch(url, data={
        'students': [student.id]
    })
    assert response.status_code == 200
    assert response.status_code == 200
    data = response.json()
    assert data['students'] == [student.id]


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=2)
    url = f"/api/v1/courses/{course[0].id}/"
    response = client.delete(url)
    assert response.status_code == 204
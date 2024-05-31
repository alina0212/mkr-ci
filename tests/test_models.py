import pytest
from django.db.utils import IntegrityError
from gallery.models import Category, Image


@pytest.mark.django_db
def test_category_creation(category):
    assert category.name == "Test Category"
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_image_creation(image, categories):
    category1, category2 = categories
    assert image.title == "Test Image"
    assert image.image == "path/to/image.jpg"
    assert image.age_limit == 18
    assert category1 in image.categories.all()
    assert category2 in image.categories.all()
    assert str(image) == "Test Image"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, image_path, age_limit, expected_exception",
    [
        ("Valid Image", "path/to/valid_image.jpg", 18, None),
        ("No Age Limit", "path/to/no_age_limit.jpg", None, IntegrityError),
    ]
)
def test_image_creation_with_parameters(title, image_path, age_limit, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            Image.objects.create(
                title=title,
                image=image_path,
                age_limit=age_limit
            )
    else:
        image = Image.objects.create(
            title=title,
            image=image_path,
            age_limit=age_limit
        )
        assert image.title == title
        assert image.image == image_path
        assert image.age_limit == age_limit


@pytest.fixture
def category():
    return Category.objects.create(name="Test Category")


@pytest.fixture
def categories():
    category1 = Category.objects.create(name="Category 1")
    category2 = Category.objects.create(name="Category 2")
    return category1, category2


@pytest.fixture
def image(categories):
    category1, category2 = categories
    image = Image.objects.create(
        title="Test Image",
        image="path/to/image.jpg",
        age_limit=18
    )
    image.categories.add(category1, category2)
    return image

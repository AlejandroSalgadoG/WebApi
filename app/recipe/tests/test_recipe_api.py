from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe, Tag
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **kwargs):
    attrs = {
        "title": "sample title",
        "time_minutes": 1,
        "price": Decimal("1.00"),
        "description": "sample description",
        "link": "http://example.com/recipe.pdf",
    }
    attrs.update(kwargs)
    return Recipe.objects.create(user=user, **attrs)


class PublicRecipeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="test123",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrive_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            email="other@example.com",
            password="test123",
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        payload = {
            "title": "test recipe",
            "time_minutes": 5,
            "price": Decimal("1.99"),
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_create_recipe_new_tags(self):
        payload = {
            "title": "curry",
            "time_minutes": 30,
            "price": Decimal("2.50"),
            "tags": [{"name": "thai"}, {"name": "dinner"}],
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload["tags"]:
            self.assertTrue(
                recipe.tags.filter(name=tag["name"], user=self.user).exists()
            )

    def test_create_recipe_existing_tags(self):
        tag_indian = Tag.objects.create(user=self.user, name="indian")

        payload = {
            "title": "naan",
            "time_minutes": 20,
            "price": Decimal("0.50"),
            "tags": [{"name": "indian"}, {"name": "breakfast"}]
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)

        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        self.assertIn(tag_indian, recipe.tags.all())
        for tag in payload["tags"]:
            self.assertTrue(
                recipe.tags.filter(name=tag["name"], user=self.user).exists()
            )

    def test_create_tag_on_update(self):
        recipe = create_recipe(user=self.user)

        payload = {"tags": [{"name": "lunch"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_tag = Tag.objects.get(user=self.user, name="lunch")
        self.assertIn(new_tag, recipe.tags.all())

    def test_update_recipe_tag(self):
        tag_breakfast = Tag.objects.create(user=self.user, name="breakfast")
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name="lunch")

        payload = {"tags": [{"name": "lunch"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())

    def test_clear_recipe_tags(self):
        tag = Tag.objects.create(user=self.user, name="dessert")
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)

        payload = {"tags": []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_new_ingredients(self):
        payload = {
            "title": "tacos",
            "time_minutes": 60,
            "price": Decimal("5.00"),
            "ingredients": [{"name": "pepper"}, {"name": "salt"}],
        }
        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        for ingredient in payload["ingredients"]:
            self.assertTrue(
                recipe.ingredients.filter(user=self.user, name=ingredient["name"]).exists()
            )

    def test_create_recipe_existing_ingredient(self):
        ingredient = Ingredient.objects.create(user=self.user, name="lemon")

        payload = {
            "title": "soup",
            "time_minutes": 20,
            "price": "2.20",
            "ingredients": [{"name": "lemon"}, {"name": "sauce"}]
        }

        res = self.client.post(RECIPES_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(ingredient, recipe.ingredients.all())
        for ingredient in payload["ingredients"]:
            self.assertTrue(
                recipe.ingredients.filter(user=self.user, name=ingredient["name"])
            )

    def test_create_ingredient_on_update_recipe(self):
        recipe = create_recipe(user=self.user)

        payload = {"ingredients": [{"name": "salt"}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url ,payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_ingredient = Ingredient.objects.get(user=self.user, name="salt")
        self.assertIn(new_ingredient, recipe.ingredients.all())

    def test_update_ingredient_on_update_recipe(self):
        ingredient1 = Ingredient.objects.create(user=self.user, name="pepper")
        ingredient2 = Ingredient.objects.create(user=self.user, name="salt")

        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient1)

        payload = {"ingredients": [{"name": "salt"}]}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient2, recipe.ingredients.all())
        self.assertNotIn(ingredient1, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        ingredient = Ingredient.objects.create(user=self.user, name="garlic")
        recipe = create_recipe(user=self.user)

        recipe.ingredients.add(ingredient)

        payload = {"ingredients": []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)

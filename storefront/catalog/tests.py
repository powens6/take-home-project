from django.test import TestCase
from django.urls import reverse
from .models import Category, Tag, Product

class CatalogTests(TestCase):
    def setUp(self):
        # Create test data
        self.category = Category.objects.create(name="Fishing Rods")
        self.tag = Tag.objects.create(name="Premium")
        self.product = Product.objects.create(
            name="Pro Angler Rod",
            description="Professional grade fishing rod",
            category=self.category
        )
        self.product.tags.add(self.tag)

    def test_product_creation(self):
        """Test that a product can be created with all required fields"""
        product = Product.objects.get(name="Pro Angler Rod")
        self.assertEqual(product.name, "Pro Angler Rod")
        self.assertEqual(product.description, "Professional grade fishing rod")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.tags.count(), 1)
        self.assertEqual(product.tags.first(), self.tag)

    def test_product_filtering(self):
        """Test the product filtering functionality"""
        # Create another product with different category
        other_category = Category.objects.create(name="Fishing Lures")
        other_product = Product.objects.create(
            name="Shiny Lure",
            description="Attractive fishing lure",
            category=other_category
        )

        # Test category filter
        response = self.client.get(reverse('product_list'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pro Angler Rod")
        self.assertNotContains(response, "Shiny Lure")

        # Test search filter
        response = self.client.get(reverse('product_list'), {'q': 'Professional'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pro Angler Rod")
        self.assertNotContains(response, "Shiny Lure")

    def test_category_product_relationship(self):
        """Test the relationship between categories and products"""
        # Create another product in the same category
        Product.objects.create(
            name="Beginner Rod",
            description="Entry level fishing rod",
            category=self.category
        )

        # Test that category has correct number of products
        self.assertEqual(self.category.products.count(), 2)
        
        # Test that products are accessible through category
        products = self.category.products.all()
        self.assertEqual(len(products), 2)
        self.assertTrue(any(p.name == "Pro Angler Rod" for p in products))
        self.assertTrue(any(p.name == "Beginner Rod" for p in products))

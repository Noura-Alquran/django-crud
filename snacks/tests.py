from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack


class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mohammad", email="Mohammed@email.com", password="pwd"
        )

        self.snack = Snack.objects.create(
            title="Dark chocolate", purchaser=self.user,description="Dark chocolate is loaded with flavanols that may lower blood pressure and reduce heart disease risk, provided the chocolate contains at least 70% cocoa solids" 
        )
    
    def test_string_representation(self):
        self.assertEqual(str(self.snack), "Dark chocolate")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "Dark chocolate")
        self.assertEqual(f"{self.snack.purchaser}", "Mohammad")
        self.assertEqual(self.snack.description,"Dark chocolate is loaded with flavanols that may lower blood pressure and reduce heart disease risk, provided the chocolate contains at least 70% cocoa solids")


    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dark chocolate")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser: Mohammad")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Banana",
                "purchaser": self.user.id,
                "description": "good snack",
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Banana")



    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated title","purchaser":self.user.id,"description":"New description"}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
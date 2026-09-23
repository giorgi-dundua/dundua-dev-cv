import unittest

from app import create_app


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_homepage(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Giorgi Dundua", response.data)

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_robots(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Sitemap: https://dundua.dev/sitemap.xml",
            response.data,
        )

    def test_sitemap(self):
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"<loc>https://dundua.dev/</loc>",
            response.data,
        )


if __name__ == "__main__":
    unittest.main()

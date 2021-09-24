import pytest

from website_scraper.scraper import Scraper


class TestScraper:
    @pytest.fixture
    def scraper(self):
        return Scraper(
            website_url="https://www.example.com", only_from_same_domain=True
        )

    def test_urls_from_same_domain_are_sanitized_ok(self, scraper):
        urls = [
            "https://www.example.com/about",
            "https://www.example.com/about",
            "https://www.example.com/contact",
            None,
            "#intro",
            "https://www.otherdomain.com/about",
        ]
        sanitized_urls = scraper.sanitize_urls(urls=urls)
        assert len(sanitized_urls) == 2
        assert "https://www.example.com/about", (
            "https://www.example.com/contact" in sanitized_urls
        )

    def test_title_is_sanitized_ok(self, scraper):
        assert (
            scraper.sanitize_page_title(" My awesome website ") == "my_awesome_website"
        )

    def test_get_path_from_url_ok(self, scraper):
        assert scraper.get_path_from_url("https://www.example.com") == "."
        assert scraper.get_path_from_url("https://www.example.com/") == "."
        assert scraper.get_path_from_url("https://www.example.com/foo/bar") == "foo/bar"

import requests
from bs4 import BeautifulSoup

from website_scraper.file_handler import FileHandler


class Scraper:
    def __init__(self, website_url, only_from_same_domain=True):
        self.website_url = website_url
        self.scrapped_urls = []
        self.only_from_same_domain = only_from_same_domain
        self.file_handler = FileHandler()

    def download_content_from_url(self, url) -> None:
        """
        Download content given url provided and save the html result into the path.
        """
        print("Trying to process url: {}".format(url))
        if url not in self.scrapped_urls:
            try:
                html = requests.get(url).text
                soup = BeautifulSoup(html, "html.parser")
                page_title = "{}.html".format(
                    self.sanitize_page_title(soup.title.string)
                )
                path = self.get_path_from_url(url)
                self.file_handler.save_content_to_file(
                    path=path, filename=page_title, content=html
                )
                self.scrapped_urls.append(url)
                linked_urls = [anchor.get("href") for anchor in soup.find_all("a")]
                sanitized_urls = self.sanitize_urls(linked_urls)
                for sanitized_url in sanitized_urls:
                    print(sanitized_url)
                    try:
                        self.download_content_from_url(sanitized_url)
                    except Exception as e:
                        print("Error trying to scrap url {}".format(sanitized_url))
                        print(e)
            except requests.exceptions.ConnectionError as e:
                print("Unable to establish connection : {}".format(e))
        else:
            print("{url} has already been downloaded, I pass".format(url=url))

    def sanitize_urls(self, urls) -> list:
        """
        Return a list of urls without duplicates.

        If only_from_same_domain is set to False, urls from others domain aren't filtered.

        """
        sanitized_urls = [sanitized_url for sanitized_url in set(urls) if sanitized_url]
        if self.only_from_same_domain:
            return list(filter(lambda url: self.website_url in url, sanitized_urls))
        else:
            return sanitized_urls

    def sanitize_page_title(self, title) -> str:
        """ Return input title in lowercase without whitespaces and words seperated by underscores. """
        return title.strip().replace(" ", "_").lower()

    def get_path_from_url(self, url) -> str:
        """ Return url path without trailing slash. """

        path = url.replace(self.website_url, "")
        if len(path) > 1:
            # make sure to remove trailing slash for correct path
            if path[0] == "/":
                path = path[1:]
            return path
        else:
            return "."

    def generate_sitemap(self) -> None:
        """ Generate structure content. """
        print("Here is the sitemap for url {} :\n".format(self.website_url))
        self.file_handler.show_structure(self.file_handler.output_dir)

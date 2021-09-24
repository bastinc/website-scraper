import sys

from website_scraper.scraper import Scraper


def main():
    if len(sys.argv) == 1:
        print("website-scraper <URL>")
    elif len(sys.argv) == 2:
        url = sys.argv[1]
        scraper = Scraper(website_url=url)
        print(
            "Download content to directory {}...".format(
                scraper.file_handler.output_dir
            )
        )
        scraper.download_content_from_url(url)
        scraper.generate_sitemap()
    else:
        print("Too many arguments")


if __name__ == "__main__":
    main()

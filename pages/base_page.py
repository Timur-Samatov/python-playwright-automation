class BasePage:
    """Base class for all page objects."""

    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def goto(self):
        """Navigate to the page URL. Override if custom navigation logic is needed."""
        if hasattr(self, "page_url"):
            self.page.goto(self.page_url)
        else:
            raise NotImplementedError(
                "Page must define page_url attribute or override goto() method"
            )

    def pause(self):
        self.page.pause()

    def validate_url(self, expected_url=None):
        """Validate that the current URL matches the expected URL.

        Args:
            expected_url: The URL to validate against. If None, uses self.page_url.
        """
        if expected_url is None:
            if not hasattr(self, "page_url"):
                raise ValueError(
                    "Page must define page_url attribute or provide expected_url argument"
                )
            expected_url = self.page_url

        assert (
            self.page.url == expected_url
        ), f"Expected URL {expected_url}, but got {self.page.url}"

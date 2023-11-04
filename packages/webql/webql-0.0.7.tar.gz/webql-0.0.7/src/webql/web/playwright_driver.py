import time
from enum import Enum

from playwright.sync_api import sync_playwright

from webql.common.errors import (
    AccessibilityTreeError,
    ClickError,
    ElementNotFoundError,
    InputError,
    NoOpenBrowserError,
    NoOpenPageError,
    OpenUrlError,
    PageTimeoutError,
)
from webql.common.utils import ensure_url_scheme
from webql.web.driver_constants import USER_AGENT
from webql.web.web_driver import WebDriver


class BrowserLoadState(Enum):
    DOMCONTENTLOADED = "domcontentloaded"
    """wait for the `DOMContentLoaded` event to be fired."""
    LOAD = "load"
    """wait for the `load` event to be fired."""
    NETWORKIDLE = "networkidle"
    """**DISCOURAGED** wait until there are no network connections for at least `500` ms."""


class PlaywrightWebDriver(WebDriver):
    def __init__(self, headless=True) -> None:
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._current_page = None
        """The current page that is being interacted with."""

        self._original_html = None
        """The page's original HTML content, prior to any TF modifications"""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

    def start_browser(self, user_session_extras: dict = None):
        self._start_browser(headless=self._headless, user_session_extras=user_session_extras)

    def stop_browser(self):
        """Closes the current browser session."""
        if self._browser:
            self._browser.close()
            self._browser = None
        self._playwright.stop()
        self._playwright = None

    def open_url(self, url: str):
        if not self._browser:
            raise NoOpenBrowserError()
        self._open_url(url)

    def get_html(self) -> dict:
        """Returns the original HTML (i.e. without any TF modifications) fetched from the most recently loaded page".

        Returns:

        string: The HTML content of the web page.
        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')
        return self._original_html

    def open_html(self, html: str):
        """
        Opens a new page and loads the given HTML content.
        """
        if not self._browser:
            raise NoOpenBrowserError()
        self._current_page = self._context.new_page()
        self._current_page.set_content(html)

    def get_accessiblity_tree(self, lazy_load_pages_count=3) -> dict:
        """Gets the accessibility tree for the current page.

        Parameters:
        lazy_load_pages_count (int): The number of pages to scroll down and up to load lazy loaded content.

        Returns:
        dict: AT of the page

        """
        if not self._current_page:
            raise NoOpenPageError()

        self._page_scroll(pages=lazy_load_pages_count)
        self._modify_dom()

        full_tree = None
        try:
            # Retrieve the accessibility tree
            full_tree = self._current_page.accessibility.snapshot(interesting_only=False)
        except Exception as e:
            raise AccessibilityTreeError() from e

        return full_tree

    def click(self, element_id: str):
        element_to_click = self._find_element_by_id(element_id)
        try:
            # force=True is needed to click on elements that are not visible
            # TODO: make it configurable (#11)
            element_to_click.click(force=True)
        except Exception as e:
            raise ClickError() from e

    def input(self, element_id: str, text: str):
        element_to_input = self._find_element_by_id(element_id)
        try:
            element_to_input.fill(text)
        except Exception as e:
            raise InputError() from e

    def _open_url(self, url: str, load_state: BrowserLoadState = None):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided. Waits for the given load state before returning.

        Parameters:

        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.

        """

        self._current_page = None
        url = ensure_url_scheme(url)

        try:
            page = self._context.new_page()
            page.goto(url)
            page.wait_for_load_state(load_state.value if load_state else None)
        except TimeoutError as e:
            raise PageTimeoutError() from e
        except Exception as e:
            raise OpenUrlError() from e
        self._current_page = page
        self._original_html = page.content()

    def _modify_dom(self):
        """Modifies the dom by assigning a unique ID to every node in the document,
        and adding DOM attributes to the `aria-keyshortcuts` attribute.
        """
        js_code = """
        () => {
            class WebQL_IDGenerator {
                constructor() {
                    this.currentID = 0;
                }

                getNextID() {
                    this.currentID += 1;
                    return this.currentID;
                }
            }
            const _tf_id_generator = new WebQL_IDGenerator();
            function extractAttributes(node) {
                const attributes = { html_tag: node.nodeName.toLowerCase() };
                const skippedAttributes = ['style'];
                for (let i = 0; i < node.attributes.length; i++) {
                    const attribute = node.attributes[i];
                    if (!attribute.specified || !skippedAttributes.includes(attribute.name)) {
                    attributes[attribute.name] = attribute.value || true;
                    }
                }
                return JSON.stringify(attributes);
            }
            function pre_process_dom_node(node) {
                let nodeId = node.id;
                if (!nodeId) {
                    nodeId = 'tf_' + _tf_id_generator.getNextID();
                    node.setAttribute('id', nodeId);
                }
                const attributes = extractAttributes(node);
                node.setAttribute('aria-keyshortcuts', attributes);

                const childNodes = Array.from(node.childNodes).filter(childNode => {
                    return (
                        childNode.nodeType === Node.ELEMENT_NODE ||
                        (childNode.nodeType === Node.TEXT_NODE && childNode.textContent.trim() !== '')
                    );
                });
                for (let i = 0; i < childNodes.length; i++) {
                    let childNode = childNodes[i];
                    if (childNode.nodeType === Node.TEXT_NODE) {
                        const text = childNode.textContent.trim();
                        if (text) {
                            if (childNodes.length > 1) {
                                const span = document.createElement('span');
                                span.textContent = text;
                                node.insertBefore(span, childNode);
                                node.removeChild(childNode);
                                childNode = span;
                            }
                        }
                    }
                    if (childNode.nodeType === Node.ELEMENT_NODE) {
                        pre_process_dom_node(childNode);
                    }
                }
            }
            pre_process_dom_node(document.documentElement);
        }
        """
        self._current_page.evaluate(js_code)

    def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up.

        Parameters:

        pages (int): The number of pages to scroll down.
        """
        if pages < 1:
            return

        delta_y = 10000
        for _ in range(pages):
            self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
            time.sleep(0.1)

        delta_y = -10000
        time.sleep(1)
        for _ in range(pages):
            self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
            time.sleep(0.1)

    def _start_browser(self, user_session_extras: dict = None, headless=True, load_media=False):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=headless)
        self._context = self._browser.new_context(
            user_agent=USER_AGENT, storage_state=user_session_extras
        )
        if not load_media:
            self._context.route(
                "**/*",
                lambda route, request: route.abort()
                if request.resource_type in ["image", "media", "font"]
                else route.continue_(),
            )

    def _find_element_by_id(self, element_id: str):
        try:
            return self._current_page.locator(f"#{element_id}")
        except Exception as e:
            raise ElementNotFoundError(element_id) from e

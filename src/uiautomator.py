import uiautomator2
from typing import Optional, Tuple

from agno.tools import Toolkit

class UiAutomatorTools(Toolkit):
    """Wrapper around uiautomator2 for device UI inspection and control.

    This toolkit provides a simplified interface for connecting to an Android
    device, querying UI elements, performing gestures, controlling apps, and
    executing shell commands.
    """

    def __init__(self, serialno: str):
        """Create a UiAutomatorTools instance.

        Args:
            serialno: The serial number, IP address, or host identifier of the
                target Android device as accepted by uiautomator2.connect().
        """
        self.device: uiautomator2.Device = uiautomator2.connect(serialno)
        super().__init__(name="UiAutomatorTools", 
                         tools=self.functions())
        

    def dump_hierarchy(self, compressed: bool = False, pretty: bool = False, max_depth: Optional[int] = None):
        """Return the current UI hierarchy dump from the connected device.

        Args:
            compressed: Whether to return a compressed XML dump.
            pretty: Whether to pretty-print the XML.
            max_depth: Maximum depth of the hierarchy to dump.

        Returns:
            The XML dump string returned by uiautomator2.dump_hierarchy().
        """
        return self.device.dump_hierarchy(compressed=compressed, pretty=pretty, max_depth=max_depth)

    def find_element(self, xpath: str, timeout: float = 0) -> uiautomator2.UiObject:
        """Return a UiObject for the first matching XPath expression.

        Args:
            xpath: The XPath expression used to locate the element.
            timeout: Time in seconds to wait for the element to appear.

        Returns:
            The matching UiObject.

        Raises:
            TimeoutError: If the element is not found within the timeout.
        """
        element = self.device.xpath(xpath=xpath)
        if timeout and not element.wait(timeout=timeout):
            raise TimeoutError(f"Element not found within {timeout} seconds: {xpath}")
        return element

    def exists(self, xpath: str, timeout: float = 0) -> bool:
        """Check whether an element matching the XPath exists.

        Args:
            xpath: The XPath expression used to query the UI.
            timeout: Time in seconds to wait for the element to appear.

        Returns:
            True if the element exists, False otherwise.
        """
        if timeout:
            return self.device(xpath=xpath).wait(timeout=timeout)
        return self.device.exists(xpath=xpath)

    def wait_for_element(self, xpath: str, timeout: float = 10) -> uiautomator2.UiObject:
        """Wait for an element to appear and return it.

        Args:
            xpath: The XPath expression used to locate the element.
            timeout: Time in seconds to wait for the element.

        Returns:
            The UiObject once it becomes available.

        Raises:
            TimeoutError: If the element is not found within the timeout.
        """
        return self.find_element(xpath, timeout=timeout)

    def click(self, xpath: str, timeout: float = 10):
        """Click a UI element specified by XPath.

        Args:
            xpath: The XPath expression for the element.
            timeout: Time in seconds to wait until the element is available.
        """
        element = self.wait_for_element(xpath, timeout=timeout)
        return element.click(timeout=timeout)

    def long_click(self, xpath: str, timeout: float = 10, duration: float = 0.5):
        """Perform a long click on a UI element.

        Args:
            xpath: The XPath expression for the element.
            timeout: Time in seconds to wait until the element is available.
            duration: Duration of the long press in seconds.
        """
        element = self.wait_for_element(xpath, timeout=timeout)
        return element.long_click(timeout=timeout, duration=duration)

    def set_text(self, xpath: str, text: str, timeout: float = 10, clear: bool = True):
        """Set text into an input field identified by XPath.

        Args:
            xpath: The XPath expression for the text field.
            text: The text to enter.
            timeout: Time in seconds to wait until the element is available.
            clear: Whether to clear existing text before entering new text.
        """
        element = self.wait_for_element(xpath, timeout=timeout)
        if clear:
            element.clear_text(timeout=timeout)
        return element.set_text(text, timeout=timeout)

    def clear_text(self, xpath: str, timeout: float = 10):
        """Clear the text of an input field identified by XPath.

        Args:
            xpath: The XPath expression for the text field.
            timeout: Time in seconds to wait until the element is available.
        """
        element = self.wait_for_element(xpath, timeout=timeout)
        return element.clear_text(timeout=timeout)

    def swipe(self, start: Tuple[int, int], end: Tuple[int, int], duration: float = 0.2, steps: Optional[int] = None):
        """Swipe across the screen from one point to another.

        Args:
            start: The starting (x, y) coordinates.
            end: The ending (x, y) coordinates.
            duration: Duration of the swipe in seconds.
            steps: Optional step count to control swipe granularity.
        """
        return self.device.swipe(start[0], start[1], end[0], end[1], duration=duration, steps=steps)

    def scroll(self, xpath: str, direction: str = "down", max_swipes: int = 5):
        """Scroll an element in the given direction.

        Args:
            xpath: The XPath expression for the scrollable container.
            direction: One of 'down', 'up', 'left', 'right', 'toBeginning', or 'toEnd'.
            max_swipes: Maximum number of swipe attempts.
        """
        element = self.device(xpath=xpath).scroll
        direction = direction.lower()
        if direction in ("down", "forward"):
            return element.vert.forward(max_swipes=max_swipes)
        if direction in ("up", "backward"):
            return element.vert.backward(max_swipes=max_swipes)
        if direction == "left":
            return element.horiz.forward(max_swipes=max_swipes)
        if direction == "right":
            return element.horiz.backward(max_swipes=max_swipes)
        if direction == "tobeginning":
            return element.vert.toBeginning(max_swipes=max_swipes)
        if direction == "toend":
            return element.vert.toEnd(max_swipes=max_swipes)
        raise ValueError(f"Unsupported scroll direction: {direction}")

    def screenshot(self, filename: Optional[str] = None, format: str = "pillow"):
        """Capture a screenshot from the device.

        Args:
            filename: Optional filename to save the screenshot. If omitted,
                the method returns a Pillow image object.
            format: Output format when no filename is provided.
        """
        return self.device.screenshot(filename=filename, format=format)

    def press_key(self, key: str):
        """Send a key press event to the device.

        Args:
            key: The key name or code to press.
        """
        return self.device.press(key)

    def press_back(self):
        """Press the Android back button."""
        return self.device.press("back")

    def press_home(self):
        """Press the Android home button."""
        return self.device.press("home")

    def press_recent(self):
        """Open the recent apps view."""
        return self.device.press("recent")

    def execute_shell(self, command: str, timeout: int = 60):
        """Execute a shell command on the connected device.

        Args:
            command: The shell command to execute.
            timeout: Timeout in seconds for command execution.
        """
        return self.device.shell(command, timeout=timeout)

    def get_current_package(self) -> str:
        """Return the package name of the currently focused app."""
        return self.device.app_current().get("package")

    def get_current_activity(self) -> str:
        """Return the activity name of the currently focused app."""
        return self.device.app_current().get("activity")

    def launch_app(self, package_name: str, activity: Optional[str] = None, wait: bool = True, stop: bool = False, use_monkey: bool = False):
        """Launch an app by package name."""
        return self.device.app_start(package_name, activity=activity, wait=wait, stop=stop, use_monkey=use_monkey)

    def stop_app(self, package_name: str):
        """Stop the specified app."""
        return self.device.app_stop(package_name)

    def install_app(self, apk_path: str):
        """Install an APK onto the connected device."""
        return self.device.app_install(apk_path)

    def uninstall_app(self, package_name: str):
        """Uninstall an app from the connected device."""
        return self.device.app_uninstall(package_name)

    def get_device(self):
        """Return the connected uiautomator2 device instance.

        Returns:
            The underlying uiautomator2.Device object.
        """
        return self.device

    def functions(self):
        """Return the list of functions available to the agent framework.
        
        Returns:
            A list of all public methods that can be called by the agent.
        """
        return [
            self.dump_hierarchy,
            self.find_element,
            self.exists,
            self.wait_for_element,
            self.click,
            self.long_click,
            self.set_text,
            self.clear_text,
            self.swipe,
            self.scroll,
            self.screenshot,
            self.press_key,
            self.press_back,
            self.press_home,
            self.press_recent,
            self.execute_shell,
            self.launch_app,
            self.stop_app,
            self.install_app,
            self.uninstall_app,
            self.get_device,
        ]
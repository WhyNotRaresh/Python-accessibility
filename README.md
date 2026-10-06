# selenium-axe-accessibility

A Python + Selenium WebDriver package that automatically audits web pages for accessibility issues using the [axe-core](https://github.com/dequelabs/axe-core) engine via [axe-selenium-python](https://github.com/mozilla/axe-selenium-python). It crawls configured URLs, runs accessibility checks, and outputs results to CSV files.

## Installation

```bash
pip install selenium-axe-accessibility
```

## Quick start

```python
import selenium_axe_accessibility

config = {
    'env': 'https://example.com',
    'path_prefix': '',
    'dir': './results',
    'login': False,
    'commands': [
        '/page-one',
        '/page-two',
    ]
}

selenium_axe_accessibility.run(config)
```

Each string in `commands` is a shorthand that expands to a `go_to` followed by a `run_axe`.

---

## Configuration

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `env` | `str` | ✓ | Base URL of the environment to audit (e.g. `https://example.com`) |
| `path_prefix` | `str` | ✓ | Prefix prepended to every path (e.g. `/app`) |
| `dir` | `str` | | Output directory for result files. Defaults to the current directory |
| `resolution` | `str` | | Browser window size. Defaults to `1920,1080` |
| `login` | `dict\|False` | ✓ | Login configuration, or `False` to skip login |
| `commands` | `list` | ✓ | List of commands to execute |

### Login configuration

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `commands` | `list` | ✓ | List of commands that perform the login procedure (see [Commands](#commands)) |
| `continue_on_fail` | `bool` | | If `True`, continue the audit as an anonymous user when login fails |

Example:

```json
"login": {
    "continue_on_fail": false,
    "commands": [
        { "command": "go_to", "url": "https://example.com/login" },
        { "command": "fill", "selector": "input#username", "value": "your-username" },
        { "command": "fill", "selector": "input#password", "value": "your-password" },
        { "command": "submit", "selector": "input#password" },
        { "command": "wait_for_url", "url": "https://example.com/" }
    ]
}
```

---

## Commands

Commands are specified as a list in the config. A plain string is shorthand for a `go_to` + `run_axe` pair. For anything else, use a dict with a `command` key.

### `go_to`

Navigate to a URL.

```python
{ 'command': 'go_to', 'url': 'https://example.com/page' }
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `url` | `str` | ✓ | The full URL to navigate to |

---

### `run_axe`

Run the axe accessibility engine on the current page. Results are written to the output file.

```python
{ 'command': 'run_axe' }
```

---

### `click`

Click on an element identified by a CSS selector.

```python
{ 'command': 'click', 'selector': 'button#accept-cookies' }
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `selector` | `str` | ✓ | CSS selector of the element to click |

---

### `fill`

Clear and fill a form element with a value.

```python
{ 'command': 'fill', 'selector': 'input#search', 'value': 'hello world' }
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `selector` | `str` | ✓ | CSS selector of the form element |
| `value` | `str` | ✓ | Value to type into the element |

---

### `submit`

Submit the form that a given element belongs to.

```python
{ 'command': 'submit', 'selector': 'input#password' }
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `selector` | `str` | ✓ | CSS selector of the element whose form will be submitted |

---

### `wait_for_url`

Wait until the current URL matches a given prefix.

```python
{ 'command': 'wait_for_url', 'url': 'https://example.com/dashboard' }
```

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `url` | `str` | ✓ | URL prefix to wait for |
| `timeout` | `int` | | Maximum wait time in seconds. Defaults to `60` |

---

## Output

Results are written to a CSV file in the configured `dir`. The file is named:

```
accessibility-<date>[-<username>][-<resolution>].csv
```

Each row represents one violation and contains:

| Column | Description |
|--------|-------------|
| URL | The page URL where the violation was detected |
| Name | Human-readable violation name |
| Impact | Axe impact level (`minor`, `moderate`, `serious`, `critical`) |
| Count | Number of elements affected on the page |
| HTML Target | Affected HTML nodes, separated by ` ;; ` |

---

## Custom writer

To use a custom output format, extend `AbstractWriter` and pass it to `run_with_writer()`:

```python
from selenium_axe_accessibility.writers.abstract_writer import AbstractWriter
import selenium_axe_accessibility

class MyWriter(AbstractWriter):
    def __enter__(self):
        # open your output resource
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # close your output resource
        pass

    def register_violation(self, violation, url):
        # handle one violation dict
        pass

selenium_axe_accessibility.run_with_writer(config, MyWriter())
```

---

## Adding a custom command

1. Create a class extending `AbstractCommand`:

```python
from selenium_axe_accessibility.commands.abstract_command import AbstractCommand

class MyCommand(AbstractCommand):
    def __init__(self, options):
        self.my_option = options['my_option']

    def exec(self, webdriver):
        # do something with webdriver
        # return a value only if results should be written
        pass
```

2. Register it before calling `run()`:

```python
from selenium_axe_accessibility.commands import register_command

register_command('my_command', 'my_module.MyCommand')
```

3. Use it in your config:

```python
{ 'command': 'my_command', 'my_option': 'value' }
```

Alternatively, skip registration and pass the full `'module.ClassName'` string directly as the `command` value.

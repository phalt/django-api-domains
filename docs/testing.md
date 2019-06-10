## Testing boundaries?

The only place in your code that touches the outside world (anything outside your domain - other domains, or external consumers) is `interfaces.py`. Any file that handles `interfaces.py` should **mock out other dependent domains** but you should still be testing your **own interface definitions**.

You should use Python's [standard `patch` tool for this](https://docs.python.org/3.5/library/unittest.mock.html#unittest.mock.patch).

You **can** use [`MagicMock`](https://docs.python.org/3.5/library/unittest.mock.html#unittest.mock.MagicMock) where it makes sense.

Here is an example:

```python
# book/test_services.py
from unittest.mock import patch

from src.book.services import create_book


@patch('src.book.interfaces.AuthorInterface.get_author')
def test_service_calls_author_interface(mocked_function_call):
    # Set up patched domain calls if you need it
    mocked_function_call.return_value = {
        'returned': 'object',
    }
    # The actual test
    result = create_book(
        name='A Wizard of Earthsea',
        author_id='d29eee0b-5b60-46d8-8c42-a8da9ddabbb6',
    )
    # Assert patched domain called with expected values
    assert mocked_function_call.assert_called_with(
      id='d29eee0b-5b60-46d8-8c42-a8da9ddabbb6',
    )
```

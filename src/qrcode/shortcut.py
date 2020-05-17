from functools import lru_cache


@lru_cache(maxsize=1)
def _get_redirect_template(path='redirect_template.html'):
    with open(path) as f:
        return f.read()


def make_redirect_html(filepath, url):
    template = _get_redirect_template()
    with open(filepath, 'w') as f:
        f.write(template.format(url=url))

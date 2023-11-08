
from pydlj import Dlj
url = "https://twitter.com/"
s = Dlj()


def test_cloudflare_page():
    assert s.cf.short(url).startswith("https://bitly.ddot.cc/")

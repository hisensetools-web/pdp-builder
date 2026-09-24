"""Pages built by a page builder rather than a storefront theme.

Tilda (very common on .ru stores such as bibikstore.ru) never uses /products/ URLs, puts the
real image on a <div data-original=...> with only a tiny placeholder in the inline style, and
keeps the rest of the slides in an embedded JSON blob with escaped slashes.
"""
import unittest

from pdpkit import scrape

TILDA = r"""
<!doctype html><html><head><title>Рассвет-Закат</title></head><body>
<div class="t-slds t-slds__main">
  <div class="t-slds__item t-slds__item_active">
    <div class="t-slds__bgimage t-bgimg"
         data-original="https://static.tildacdn.com/tild3234-3562/product_front.jpg"
         style="background-image:url('https://static.tildacdn.com/tild3234-3562/-/resize/20x/product_front.jpg')"></div>
  </div>
  <div class="t-slds__item">
    <div class="t-slds__bgimage" data-original="https://static.tildacdn.com/tild6611-9090/product_side.jpg"></div>
  </div>
</div>

<div class="t-store__prod-popup__slider">
  <img class="t-slds__img" data-original="https://static.tildacdn.com/tild7777-1111/product_detail.jpg" alt="detail">
</div>

<div class="t-cover" data-content-cover-bg="https://static.tildacdn.com/tild0000-0000/hero_banner.jpg"></div>
<div class="t-feed__post-popup">
  <img src="https://static.tildacdn.com/tild5555-2222/how-it-works.jpg" alt="how it works">
</div>

<script>
  window.t_store_products = [{"uid":"1","title":"Рассвет-Закат",
    "gallery":"[{\"img\":\"https:\/\/static.tildacdn.com\/tild1234-5678\/pack_shot.jpg\"},
                 {\"img\":\"https:\/\/static.tildacdn.com\/tild4321-8765\/in_use.jpg\"}]"}];
</script>
</body></html>
"""
BASE = "https://bibikstore.ru/rassvet-zakat1"


class TildaTests(unittest.TestCase):
    def setUp(self):
        self.refs = scrape.extract_image_refs(TILDA, BASE)
        self.urls = [r.url for r in self.refs]
        self.gallery = [r.url for r in self.refs if r.kind == "gallery"]

    def test_images_hidden_on_a_div_are_found(self):
        # the old code only read lazy attributes on <img>/<source>, so these were invisible
        self.assertIn("https://static.tildacdn.com/tild3234-3562/product_front.jpg", self.urls)
        self.assertIn("https://static.tildacdn.com/tild6611-9090/product_side.jpg", self.urls)

    def test_slider_images_count_as_the_product_gallery(self):
        self.assertIn("https://static.tildacdn.com/tild3234-3562/product_front.jpg", self.gallery)
        self.assertIn("https://static.tildacdn.com/tild6611-9090/product_side.jpg", self.gallery)
        self.assertIn("https://static.tildacdn.com/tild7777-1111/product_detail.jpg", self.gallery)

    def test_slides_that_only_exist_in_embedded_json_are_found(self):
        self.assertIn("https://static.tildacdn.com/tild1234-5678/pack_shot.jpg", self.urls)
        self.assertIn("https://static.tildacdn.com/tild4321-8765/in_use.jpg", self.urls)

    def test_page_furniture_is_not_the_gallery(self):
        self.assertIn("https://static.tildacdn.com/tild5555-2222/how-it-works.jpg", self.urls)
        self.assertNotIn("https://static.tildacdn.com/tild5555-2222/how-it-works.jpg", self.gallery)

    def test_a_low_res_placeholder_does_not_replace_the_real_file(self):
        self.assertIn("https://static.tildacdn.com/tild3234-3562/product_front.jpg", self.gallery)

    def test_every_url_is_absolute_and_unescaped(self):
        self.assertTrue(all(u.startswith("https://") and "\\/" not in u for u in self.urls))


class GenericSweepTests(unittest.TestCase):
    def test_escaped_json_urls_are_unescaped(self):
        html = r'<script>var a = {"src":"https:\/\/cdn.example.com\/a\/b\/photo-1.jpg"};</script>'
        urls = [r.url for r in scrape.extract_image_refs(html, "https://x.com/p")]
        self.assertEqual(urls, ["https://cdn.example.com/a/b/photo-1.jpg"])

    def test_the_sweep_still_skips_logos_and_badges(self):
        html = ('<script>var a = ["https://cdn.example.com/files/logo-dark.png",'
                '"https://cdn.example.com/files/visa-badge.png",'
                '"https://cdn.example.com/files/real-product.jpg"];</script>')
        urls = [r.url for r in scrape.extract_image_refs(html, "https://x.com/p")]
        self.assertEqual(urls, ["https://cdn.example.com/files/real-product.jpg"])


if __name__ == "__main__":
    unittest.main()

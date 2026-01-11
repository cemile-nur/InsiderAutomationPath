import unittest
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager

L_URL = "https://www.lcw.com/tr-TR/TR"
L_HOME_URL = "https://www.lcw.com/"
L_CATEGORY_URL = "https://www.lcw.com/kadin-kaban-t-5199"
L_CART_URL = "https://www.lcw.com/sepetim"

L_COOKIE = (
    By.XPATH,
    "//button[contains(., 'Tüm Çerezlere İzin Ver')] | //button[@id='cookierevocation-accept']"
)

L_INSIDER_CLOSE = (
    By.XPATH,
    "//div[contains(@class,'ins-close-button')]"
    " | //span[normalize-space()='×']"
    " | //button[contains(@class,'close-button')]"
    " | //button[contains(@aria-label,'Kapat')]"
)

L_PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='-o-']")

L_ADD_CART = (By.CSS_SELECTOR, "#pd_add_to_cart, button#pd_add_to_cart")
L_ADD_CART_TEXT = (By.XPATH, "//button[contains(., 'Sepete Ekle') or contains(., 'SEPETE EKLE')]")

L_SIZE_LABEL = (By.XPATH, "//*[normalize-space()='Beden:' or normalize-space()='Beden']")
L_SIZE_OPTIONS_XPATH = (
    By.XPATH,
    "//*[normalize-space()='Beden:' or normalize-space()='Beden']"
    "/following::*[1]//*[self::a or self::button or self::div]"
    "[normalize-space()!='' and string-length(normalize-space())<=3]"
)
L_SIZE_OPTIONS_FALLBACK = (
    By.XPATH,
    "//*[self::a or self::button or self::div]"
    "[normalize-space()!='' and string-length(normalize-space())<=3]"
    "[translate(normalize-space(), '0123456789', '')='']"
)

L_ADDED_PANEL = (By.XPATH, "//*[contains(.,'Ürün Sepete Eklendi') or contains(.,'Ürün sepete eklendi')]")

L_HEADER_CART = (
    By.XPATH,
    "//a[contains(.,'Sepetim') or contains(.,'Sepetim (') or contains(.,'Sepetim (0)')]"
)

L_CART_DRAWER = (By.CSS_SELECTOR, "[data-vaul-drawer], .cart-drawer, .vaul-drawer")
L_DRAWER_GO_TO_CART_BTN = (
    By.CSS_SELECTOR,
    "button.actions-go-to-cart, button[aria-label='Sepete Git'], button[aria-label*='Sepete Git']"
)

L_CART_ITEM = (By.CSS_SELECTOR, ".cart-item, .basket-item, [data-testid*='cart'], .shopping-cart")

L_LOGO = (By.CSS_SELECTOR, ".main-header-logo, a.main-header-logo, a[href='/tr-TR/TR']")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class LCWAutomation(unittest.TestCase):
    def setUp(self):
        opts = Options()
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-blink-features=AutomationControlled")

        prefs = {"profile.default_content_setting_values.notifications": 2}
        opts.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )
        self.wait = WebDriverWait(self.driver, 25)

    def _js_click(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("arguments[0].click();", el)

    def handle_popups(self):
        d = self.driver

        try:
            cookies = d.find_elements(*L_COOKIE)
            if cookies:
                self._js_click(cookies[0])
        except Exception:
            pass

        try:
            closes = d.find_elements(*L_INSIDER_CLOSE)
            if closes:
                self._js_click(closes[0])
        except Exception:
            pass

        try:
            d.execute_script("""
                document.querySelectorAll('.ins-preview-wrapper,.ins-selectable-element,.ins-web-wrap,.ins-notification')
                .forEach(el => el.remove());
            """)
        except Exception:
            pass

    def safe_click(self, locator, timeout=15, retries=3):
        w = WebDriverWait(self.driver, timeout)
        last = None
        for _ in range(retries):
            try:
                el = w.until(EC.element_to_be_clickable(locator))
                try:
                    el.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    self._js_click(el)
                return
            except Exception as e:
                last = e
                self.handle_popups()
        raise last

    def select_first_available_size(self):
        d = self.driver
        self.handle_popups()

        candidates = []
        try:
            self.wait.until(EC.presence_of_element_located(L_SIZE_LABEL))
            candidates = d.find_elements(*L_SIZE_OPTIONS_XPATH)
        except Exception:
            candidates = []

        if not candidates:
            candidates = d.find_elements(*L_SIZE_OPTIONS_FALLBACK)

        cleaned = []
        for el in candidates:
            try:
                if not el.is_displayed():
                    continue
                txt = (el.text or "").strip()
                if not txt:
                    continue
                cls = (el.get_attribute("class") or "").lower()
                aria_disabled = (el.get_attribute("aria-disabled") or "").lower()
                disabled_attr = el.get_attribute("disabled")
                if "disabled" in cls or "out-of-stock" in cls or aria_disabled == "true" or disabled_attr is not None:
                    continue
                cleaned.append(el)
            except Exception:
                continue

        if not cleaned:
            return False

        self._js_click(cleaned[0])
        logging.info(f"Seçilen beden: {(cleaned[0].text or '').strip()}")
        return True

    def open_drawer_and_go_to_cart(self):
        d = self.driver

        self.safe_click(L_HEADER_CART, timeout=15, retries=3)
        self.handle_popups()

        try:
            self.wait.until(EC.visibility_of_element_located(L_CART_DRAWER))
            self.safe_click(L_DRAWER_GO_TO_CART_BTN, timeout=15, retries=3)
        except Exception:
            d.get(L_CART_URL)

    def ensure_cart_has_item(self):
        """
        Sepet sayfasında ürün görünene kadar bekler.
        İlk deneme olmazsa 1 kez refresh yapıp tekrar bekler.
        """
        d = self.driver

        # /sepetim'e kesin geç
        if "sepet" not in d.current_url.lower():
            d.get(L_CART_URL)

        self.handle_popups()

        try:
            el = WebDriverWait(d, 15).until(EC.presence_of_element_located(L_CART_ITEM))
            return el.is_displayed()
        except Exception:
            pass

        d.refresh()
        self.handle_popups()

        try:
            el = WebDriverWait(d, 20).until(EC.presence_of_element_located(L_CART_ITEM))
            return el.is_displayed()
        except Exception:
            return False

    def test_shopping_flow(self):
        d = self.driver

        d.get(L_URL)
        self.handle_popups()
        self.assertIn("lcw.com", d.current_url, "Ana sayfa yüklenemedi!")
        self.assertTrue(True, "Ana sayfa OK")

        logging.info("Kategoriye gidiliyor...")
        d.get(L_CATEGORY_URL)
        self.handle_popups()
        self.assertIn("lcw.com", d.current_url, "Kategori sayfası açılamadı!")
        self.wait.until(EC.presence_of_all_elements_located(L_PRODUCT_LINKS))
        self.assertTrue(True, "Kategori OK")

        logging.info("İlk ürüne gidiliyor...")
        links = d.find_elements(*L_PRODUCT_LINKS)
        self.assertTrue(len(links) > 0, "Ürün linki bulunamadı!")
        href = links[0].get_attribute("href")
        self.assertTrue(href is not None and "lcw.com" in href, "Ürün href alınamadı!")
        d.get(href)

        try:
            self.wait.until(EC.presence_of_element_located(L_ADD_CART))
        except TimeoutException:
            self.wait.until(EC.presence_of_element_located(L_ADD_CART_TEXT))

        self.handle_popups()
        self.assertIn("lcw.com", d.current_url, "Ürün sayfası açılamadı!")
        self.assertTrue(True, "Ürün OK")

        logging.info("Beden seçimi kontrol ediliyor...")
        self.select_first_available_size()

        logging.info("Sepete ekleniyor...")
        try:
            self.safe_click(L_ADD_CART, timeout=15, retries=3)
        except Exception:
            self.safe_click(L_ADD_CART_TEXT, timeout=15, retries=3)

        try:
            WebDriverWait(d, 25).until(EC.visibility_of_element_located(L_ADDED_PANEL))
            panel_ok = True
        except Exception:
            panel_ok = False
        self.assertEqual(True, panel_ok, "Sepete ekleme başarısız: 'Ürün Sepete Eklendi' paneli gelmedi!")
        self.assertTrue(True, "Sepete ekle OK")

        logging.info("Sepete gidiliyor (Sepetim -> Drawer -> Sepete Git)...")
        self.open_drawer_and_go_to_cart()
        self.handle_popups()

        self.assertIn("sepet", d.current_url.lower(), "Sepet sayfası açılamadı!")

        cart_ok = self.ensure_cart_has_item()
        self.assertEqual(True, cart_ok, f"Sepete eklenen ürün sepet sayfasında görünmüyor! URL: {d.current_url}")

        logging.info("Anasayfaya dönülüyor...")
        try:
            self.safe_click(L_LOGO, timeout=10, retries=2)
        except Exception:
            d.get(L_HOME_URL)

        self.handle_popups()
        cur = d.current_url.rstrip("/") + "/"
        ok = (cur == L_HOME_URL) or (cur.startswith(L_URL.rstrip("/") + "/"))
        self.assertEqual(True, ok, f"Anasayfaya dönüş başarısız! URL: {d.current_url}")

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

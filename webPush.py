class WebPush:
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type):
        self.platform = platform
        self.optin = bool(optin)  
        self.global_frequency_capping = global_frequency_capping
        self.start_date = start_date
        self.end_date = end_date
        self.language = language
        self.push_type = push_type
    def send_push(self):
        print(f"{self.push_type} Push gönderildi!")


class TriggerPush(WebPush):
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type,
                 trigger_page: str):
        super().__init__(platform, optin, global_frequency_capping,
                         start_date, end_date, language, push_type)
        self.trigger_page = trigger_page   # string

class BulkPush(WebPush):
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type,
                 send_date: int):
        super().__init__(platform, optin, global_frequency_capping,
                         start_date, end_date, language, push_type)
        self.send_date = send_date   # integer

class SegmentPush(WebPush):
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type,
                 segment_name: str):
        super().__init__(platform, optin, global_frequency_capping,
                         start_date, end_date, language, push_type)
        self.segment_name = segment_name   # string


class PriceAlertPush(WebPush):
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type,
                 price_info: int, discount_rate: float):
        super().__init__(platform, optin, global_frequency_capping,
                         start_date, end_date, language, push_type)
        self.price_info = price_info       # integer
        self.discount_rate = discount_rate # float (0.20 = %20 indirim)
    def discountPrice(self):
        discounted = self.price_info * (1 - self.discount_rate)
        return discounted


class InstockPush(WebPush):
    def __init__(self, platform, optin, global_frequency_capping,
                 start_date, end_date, language, push_type,
                 stock_info: bool):
        super().__init__(platform, optin, global_frequency_capping,
                         start_date, end_date, language, push_type)
        self.stock_info = bool(stock_info)  # boolean
    def stockUpdate(self):
        """
        Stok bilgisini tersine çevirir.
        True ise False, False ise True yapar ve yeni değeri return eder.
        """
        self.stock_info = not self.stock_info
        return self.stock_info

trigger_push = TriggerPush(
    platform="Android",
    optin=True,
    global_frequency_capping=5,
    start_date="2025-01-01",
    end_date="2025-12-31",
    language="TR",
    push_type="Trigger",
    trigger_page="/urun/123"
)

bulk_push = BulkPush(
    platform="iOS",
    optin=True,
    global_frequency_capping=10,
    start_date="2025-02-01",
    end_date="2025-03-01",
    language="EN",
    push_type="Bulk",
    send_date=20250215
)

segment_push = SegmentPush(
    platform="Web",
    optin=False,
    global_frequency_capping=3,
    start_date="2025-01-15",
    end_date="2025-04-15",
    language="TR",
    push_type="Segment",
    segment_name="SepetiTerkEdenler"
)
price_alert_push = PriceAlertPush(
    platform="Android",
    optin=True,
    global_frequency_capping=2,
    start_date="2025-03-01",
    end_date="2025-06-01",
    language="TR",
    push_type="PriceAlert",
    price_info=1000,   
    discount_rate=0.25   
)
instock_push = InstockPush(
    platform="Web",
    optin=True,
    global_frequency_capping=4,
    start_date="2025-01-01",
    end_date="2025-12-31",
    language="TR",
    push_type="Instock",
    stock_info=False
)
trigger_push.send_push()
bulk_push.send_push()
segment_push.send_push()
indirimli_fiyat = price_alert_push.discountPrice()
print("İndirimli fiyat:", indirimli_fiyat)
price_alert_push.send_push()
print("Eski stok durumu:", instock_push.stock_info)
yeni_stok = instock_push.stockUpdate()
print("Yeni stok durumu:", yeni_stok)
instock_push.send_push()

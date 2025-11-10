#!/usr/bin/env python3
"""
Professional CW Enerji Chatbot - Tree Structure
"""

import re
import random
from datetime import datetime

class ProfessionalChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_data = {}
        self.current_state = "MAIN_MENU"
        self.last_intent = None

        # Professional tree-based response templates
        self.responses = {
            'main_menu': [
                {"type": "menu", "title": "CW Enerji'ye hoş geldiniz.", "options": [
                    {"text": "SATIN AL", "description": "Güneş paneli sistemleri ve fiyat teklifleri", "action": "satın al"},
                    {"text": "BİLGİ", "description": "Teknik detaylar ve ürün bilgileri", "action": "bilgi"},
                    {"text": "FİYAT", "description": "Fiyatlandırma ve ödeme seçenekleri", "action": "fiyat"},
                    {"text": "KURULUM", "description": "Montaj süreci ve zamanlama", "action": "kurulum"}
                ]}
            ],
            'info_menu': [
                {"type": "menu", "title": "Bilgi konuları:", "options": [
                    {"text": "Panel Teknolojileri", "description": "Monokristalin, polikristalin ve ince film paneller", "action": "panel teknolojileri"},
                    {"text": "Sistem Kapasitesi", "description": "3kW - 10kW arası sistem seçenekleri", "action": "sistem kapasitesi"},
                    {"text": "Garanti Koşulları", "description": "25 yıl performans ve 10 yıl işçilik garantisi", "action": "garanti koşulları"},
                    {"text": "Finansman Seçenekleri", "description": "Peşin, kredi ve leasing imkanları", "action": "finansman seçenekleri"}
                ]}
            ],
            'panel_types': [
                {"type": "list", "title": "Panel teknolojileri:", "items": [
                    {"title": "MONOKRİSTALİN PANELLER", "details": [
                        "Verimlilik: %22-24",
                        "Garanti: 25 yıl",
                        "Uygun: Alanı kısıtlı olanlar"
                    ]},
                    {"title": "POLİKRİSTALİN PANELLER", "details": [
                        "Verimlilik: %17-19",
                        "Garanti: 25 yıl",
                        "Uygun: Standart konutlar"
                    ]},
                    {"title": "İNCE FİLM PANELLER", "details": [
                        "Verimlilik: %12-15",
                        "Garanti: 20 yıl",
                        "Uygun: Özel projeler"
                    ]}
                ], "footer": "Ana menüye dönmek için 'merhaba' yazın."}
            ],
            'system_capacity': [
                {"type": "list", "title": "Sistem kapasiteleri:", "items": [
                    {"title": "3 kW", "details": ["1-2 kişilik aileler"]},
                    {"title": "5 kW", "details": ["3-4 kişilik aileler"]},
                    {"title": "7 kW", "details": ["5+ kişilik aileler"]},
                    {"title": "10 kW", "details": ["Ticari kullanım"]}
                ], "footer": "Doğru kapasite seçimi için aylık elektrik tüketiminizi (kWh) ve konumunuzu belirtin.\n\nAna menüye dönmek için 'merhaba' yazın."}
            ],
            'warranty_info': [
                {"type": "list", "title": "Garanti koşulları:", "items": [
                    {"title": "Performans garantisi", "details": [
                        "25 yıl: %85 minimum verim",
                        "Lineer degradasyon garantisi",
                        "Ürün değişim hakkı"
                    ]},
                    {"title": "İşçilik garantisi", "details": [
                        "10 yıl: Montaj ve işçilik",
                        "Ücretsiz onarım ve değişim",
                        "7/24 teknik destek"
                    ]}
                ], "footer": "Ana menüye dönmek için 'merhaba' yazın."}
            ],
            'financing_options': [
                {"type": "list", "title": "Finansman seçenekleri:", "items": [
                    {"title": "Peşin ödeme", "details": [
                        "%5-10 indirim",
                        "Hızlı kurulum",
                        "Ekstra garanti"
                    ]},
                    {"title": "Kredi seçenekleri", "details": [
                        "0 faizli imkanlar",
                        "12-48 ay taksit",
                        "Hızlı onay"
                    ]},
                    {"title": "Leasing", "details": [
                        "Kira öder gibi öde",
                        "Bakım dahil",
                        "Sigorta kapsamı"
                    ]}
                ], "footer": "Detaylı teklif için konum ve tüketim bilginizi belirtin.\n\nAna menüye dönmek için 'merhaba' yazın."}
            ],
            'pricing_info': [
                {"type": "list", "title": "Fiyatlandırma bilgileri:", "items": [
                    {"title": "3 kW", "details": ["120.000 - 180.000 TL"]},
                    {"title": "5 kW", "details": ["180.000 - 280.000 TL"]},
                    {"title": "7 kW", "details": ["250.000 - 380.000 TL"]},
                    {"title": "10 kW", "details": ["350.000 - 550.000 TL"]}
                ], "footer": "Fiyata dahil olanlar:\n• Paneller ve inverter\n• Montaj ekipmanları\n• Tüm izin ve belgeler\n• 25 yıl performans garantisi\n\nKişiselleştirilmiş teklif için konum ve tüketim bilginizi belirtin.\n\nAna menüye dönmek için 'merhaba' yazın."}
            ],
            'installation_info': [
                "Kurulum süreci:\n\nFaz 1: Keşif ve tasarım (1-2 gün)\n- Teknik analiz\n- Proje tasarımı\n- İzin hazırlığı\n\nFaz 2: İzin süreci (7-15 gün)\n- Belediye izinleri\n- Şebeke başvurusu\n- Yasal belgeler\n\nFaz 3: Montaj (1-3 gün)\n- Panel kurulumu\n- Elektrik bağlantıları\n- Sistem testleri\n\nFaz 4: Teslimat (1 gün)\n- Final kontroller\n- Eğitim ve belgeler\n- Devreye alma\n\nToplam süre: 3-4 hafta\n\nAna menüye dönmek için 'merhaba' yazın."
            ],
            'selling_process': [
                "Satın alma süreci:\n\nÖzel teklif için gerekli bilgiler\n- Konum (şehir/ilçe)\n- Aylık elektrik tüketimi (kWh)\n- Çatı tipi ve durumu\n- Bütçe aralığı (isteğe bağlı)\n\nBu bilgileri paylaştığınızda size özel teklif hazırlayacağım.\n\nAna menüye dönmek için 'merhaba' yazın."
            ],
            'goodbye': [
                "CW Enerji olarak zaman ayırdığınız için teşekkür ederiz. Temiz enerjiye geçiş yolculuğunuzda her zaman destekçiniziz.\n\nİletişim için:\nWeb: www.cwenerji.com\nTel: 0850 XXX XX XX\n\nİyi günler dileriz."
            ],
            'thanks': [
                "Rica ederim. CW Enerji olarak en doğru güneş enerjisi çözümünü bulmanız için buradayız.\n\nBaşka sorunuz olursa çekinmeyin."
            ],
            'default': [
                "Anlaşılamadı. Lütfen aşağıdaki seçeneklerden birini belirtin:\n\n1. SATIN AL\n2. BİLGİ\n3. FİYAT\n4. KURULUM\n\nVeya 'Menü' yazarak ana menüye dönebilirsiniz."
            ]
        }

    def get_intent(self, message):
        """Professional intent detection for Turkish"""
        message_lower = message.lower().strip()

        # Navigation commands
        if message_lower in ['menü', 'menu', 'ana menü', 'başla', '0', 'merhaba', 'don', 'geri']:
            self.current_state = "MAIN_MENU"
            return 'main_menu'

        # Goodbye
        if any(word in message_lower for word in ['hoşça kal', 'görüşürüz', 'kapat', 'bitir']):
            return 'goodbye'

        # Thanks
        if any(word in message_lower for word in ['teşekkür', 'sağol', 'thanks']):
            return 'thanks'

        # Main menu options
        if self.current_state == "MAIN_MENU":
            if message_lower in ['satın al', 'satın alma', 'al', 'buy', 'purchase']:
                self.current_state = "SELLING"
                return 'selling_process'
            elif message_lower in ['bilgi', 'information', 'info', 'detay', 'teknik']:
                self.current_state = "INFO_MENU"
                return 'info_menu'
            elif message_lower in ['fiyat', 'price', 'cost', 'ücret', 'maliyet']:
                self.current_state = "PRICING"
                return 'pricing_info'
            elif message_lower in ['kurulum', 'montaj', 'installation', 'setup', 'tesis']:
                self.current_state = "INSTALLATION"
                return 'installation_info'

        # Info menu options
        if self.current_state == "INFO_MENU":
            if message_lower in ['a', 'panel', 'paneller', 'panel teknolojileri', 'monokristalin', 'polikristalin']:
                return 'panel_types'
            elif message_lower in ['b', 'kapasite', 'sistem', 'capacity', '3 kw', '5 kw', '7 kw']:
                return 'system_capacity'
            elif message_lower in ['c', 'garanti', 'warranty', 'işçilik']:
                return 'warranty_info'
            elif message_lower in ['d', 'finansman', 'kredi', 'financing', 'peşin', 'leasing']:
                return 'financing_options'
            elif message_lower in ['e', 'başa dön', 'geri']:
                self.current_state = "MAIN_MENU"
                return 'back_to_menu'

        # Extract location and energy usage for recommendations
        entities = self.extract_entities(message)
        if entities and 'location' in entities and 'energy_usage' in entities:
            self.user_data.update(entities)
            return 'generate_recommendation'

        # Default for current states
        if self.current_state == "SELLING":
            return 'selling_process'
        elif self.current_state == "INFO_MENU":
            return 'info_menu'
        elif self.current_state == "PRICING":
            return 'pricing_info'
        elif self.current_state == "INSTALLATION":
            return 'installation_info'

        return 'default'

    def extract_entities(self, message):
        """Extract location and energy usage from message"""
        entities = {}
        message_lower = message.lower()

        # Turkish location extraction
        locations = ['istanbul', 'ankara', 'izmir', 'bursa', 'antalya', 'adana', 'konya', 'sakarya', 'eskişehir']
        for location in locations:
            if location in message_lower:
                entities['location'] = location.title()
                break

        # Energy usage extraction
        energy_pattern = r'(\d+)\s*(?:kwh|kilowatt|kilovatsaat)'
        match = re.search(energy_pattern, message_lower)
        if match:
            entities['energy_usage'] = int(match.group(1))

        return entities

    def calculate_recommendation(self, location=None, energy_usage=None):
        """Calculate personalized recommendation"""
        if not energy_usage:
            energy_usage = 1000

        if not location:
            location = "bölgenizde"

        # Calculations
        daily_usage = energy_usage / 30
        system_size = round(daily_usage / 5 * 1.5, 1)
        system_watts = system_size * 1000
        price = round(system_watts * 30, 0)
        bill_reduction = min(95, max(70, int(system_size * 8)))

        return {
            'system_size': system_size,
            'price': price,
            'bill_reduction': bill_reduction,
            'location': location
        }

    def generate_recommendation_response(self):
        """Generate professional recommendation"""
        if 'location' in self.user_data and 'energy_usage' in self.user_data:
            rec = self.calculate_recommendation(
                self.user_data['location'],
                self.user_data['energy_usage']
            )

            return f"""CW ENERJI ÖZEL TEKLİFİ

KONUM: {rec['location']}
AYLIK TÜKETİM: {self.user_data['energy_usage']} kWh
ÖNERİLEN SİSTEM: {rec['system_size']} kW
YATIRIM MİKTARI: {rec['price']:,.0f} TL
FATURA TASARRUFU: %{rec['bill_reduction']}

DETAYLI BİLGİLER
• Aylık tasarruf: 1.500-6.000 TL
• Yatırım geri dönüşü: 6-8 yıl
• Mülk değeri artışı: %10-15
• Çevresel katkı: Yılda 2-3 ton CO2

TEKLİF İÇİN İLETİŞİM
Telefon: 0850 XXX XX XX
Web: www.cwenerji.com
E-posta: bilgi@cwenerji.com

Ana menü için 'Menü' yazın."""

        return "Kişiselleştirilmiş teklif için konum ve aylık tüketim bilginizi belirtin."

    def get_response(self, message):
        """Get response based on tree structure"""
        intent = self.get_intent(message)
        self.last_intent = intent

        # Handle recommendation generation
        if intent == 'generate_recommendation':
            return self.generate_recommendation_response()

        # Get standard response
        response_options = self.responses.get(intent, self.responses['default'])
        response = random.choice(response_options)

        return response

    def get_response_json(self, message):
        """Get response in JSON format for interactive UI"""
        intent = self.get_intent(message)
        self.last_intent = intent

        # Handle recommendation generation
        if intent == 'generate_recommendation':
            return {"type": "text", "content": self.generate_recommendation_response()}

        # Get standard response
        response_options = self.responses.get(intent, self.responses['default'])
        response = random.choice(response_options)

        # Check if response is a menu (dict), list (dict), or text (string)
        if isinstance(response, dict):
            return response
        else:
            return {"type": "text", "content": response}

    def reset_conversation(self):
        """Reset conversation to main menu"""
        self.current_state = "MAIN_MENU"
        self.user_data = {}
        self.last_intent = None
        self.conversation_history = []
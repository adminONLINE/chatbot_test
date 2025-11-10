#!/usr/bin/env python3
"""
Simple rule-based solar panel chatbot for demo purposes
"""

import re
import random
from datetime import datetime

class SolarChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_data = {}
        self.current_state = "MAIN_MENU"  # State management
        self.last_intent = None

        # Professional tree-based response templates
        self.responses = {
            'main_menu': [
                "CW Enerji'ye hoş geldiniz. Size nasıl yardımcı olabilirim?\n\n1. SATIN AL - Güneş paneli sistemleri ve fiyat teklifleri\n2. BİLGİ - Teknik detaylar ve ürün bilgileri\n3. FİYAT - Fiyatlandırma ve ödeme seçenekleri\n4. KURULUM - Montaj süreci ve zamanlama\n\nLütfen bir seçenek belirtin (1-4) veya doğrudan konu yazın."
            ],
            'info_menu': [
                "Hangi konuda bilgi almak istersiniz?\n\nA. Panel Teknolojileri\nB. Sistem Kapasitesi\nC. Garanti Koşulları\nD. Finansman Seçenekleri\nE. Başa Dön\n\nLütfen bir seçenek belirtin (A-E)."
            ],
            'panel_types': [
                "Panel teknolojileri hakkında detaylı bilgi:\n\nMONOKRİSTALİN PANELLER\n• Verimlilik: %22-24\n• Garanti: 25 yıl\n• Uygun: Alanı kısıtlı olanlar\n\nPOLİKRİSTALİN PANELLER\n• Verimlilik: %17-19\n• Garanti: 25 yıl\n• Uygun: Standart konutlar\n\nİNCE FİLM PANELLER\n• Verimlilik: %12-15\n• Garanti: 20 yıl\n• Uygun: Özel projeler\n\nDiğer konular için 'Bilgi' yazın veya ana menü için 'Menü' yazın."
            ],
            'system_capacity': [
                "Sistem kapasitesi hesaplaması:\n\nSTANDART KAPASİTELER\n• 3 kW: 1-2 kişilik aileler\n• 5 kW: 3-4 kişilik aileler\n• 7 kW: 5+ kişilik aileler\n• 10 kW: Ticari kullanım\n\nDoğru kapasite seçimi için aylık elektrik tüketiminizi (kWh) ve konumunuzu belirtin.\n\nDiğer konular için 'Bilgi' yazın veya ana menü için 'Menü' yazın."
            ],
            'warranty_info': [
                "Garanti koşulları:\n\nPERFORMANS GARANTİSİ\n• 25 yıl: %85 minimum verim\n• Lineer degradasyon garantisi\n• Ürün değişim hakkı\n\nİŞÇİLİK GARANTİSİ\n• 10 yıl: Montaj ve işçilik\n• Ücretsiz onarım ve değişim\n• 7/24 teknik destek\n\nDiğer konular için 'Bilgi' yazın veya ana menü için 'Menü' yazın."
            ],
            'financing_options': [
                "Finansman seçenekleri:\n\nPEŞİN ÖDEME\n• %5-10 indirim\n• Hızlı kurulum\n• Ekstra garanti\n\nKREDİ SEÇENEKLERİ\n• 0 faizli imkanlar\n• 12-48 ay taksit\n• Hızlı onay\n\nLEASING\n• Kira öder gibi öde\n• Bakım dahil\n• Sigorta kapsamı\n\nDetaylı teklif için konum ve tüketim bilginizi belirtin.\n\nDiğer konular için 'Bilgi' yazın veya ana menü için 'Menü' yazın."
            ],
            'pricing_info': [
                "Fiyatlandırma hakkında bilgi:\n\nSTANDART SİSTEM PAKETLERİ\n• 3 kW: 120.000 - 180.000 TL\n• 5 kW: 180.000 - 280.000 TL\n• 7 kW: 250.000 - 380.000 TL\n• 10 kW: 350.000 - 550.000 TL\n\nFİYATA DAHİL OLANLAR\n• Paneller ve inverter\n• Montaj ekipmanları\n• Tüm izin ve belgeler\n• 25 yıl performans garantisi\n\nKişiselleştirilmiş teklif için konum ve tüketim bilginizi belirtin.\n\nAna menü için 'Menü' yazın."
            ],
            'installation_info': [
                "Kurulum süreci hakkında bilgi:\n\nKURULUM FAZELERİ\n\n1. KEŞİF VE TASARIM (1-2 gün)\n   • Teknik analiz\n   • Proje tasarımı\n   • İzin hazırlığı\n\n2. İZİN SÜRECİ (7-15 gün)\n   • Belediye izinleri\n   • Şebeke başvurusu\n   • Yasal belgeler\n\n3. MONTAJ (1-3 gün)\n   • Panel kurulumu\n   • Elektrik bağlantıları\n   • Sistem testleri\n\n4. TESLİMAT (1 gün)\n   • Final kontroller\n   • Eğitim ve belgeler\n   • Devreye alma\n\nToplam süre: 3-4 hafta\n\nAna menü için 'Menü' yazın."
            ],
            'selling_process': [
                "Satın alma süreci:\n\nÖZEL TEKLİF İÇİN GEREKLİ BİLGİLER\n• Konum (şehir/ilçe)\n• Aylık elektrik tüketimi (kWh)\n• Çatı tipi ve durumu\n• Bütçe aralığı (isteğe bağlı)\n\nBu bilgileri paylaştığınızda size özel teklif hazırlayacağım.\n\nAna menü için 'Menü' yazın."
            ],
            'back_to_menu': [
                "Ana menüye dönüyorsunuz.\n\nCW Enerji'ye hoş geldiniz. Size nasıl yardımcı olabilirim?\n\n1. SATIN AL - Güneş paneli sistemleri ve fiyat teklifleri\n2. BİLGİ - Teknik detaylar ve ürün bilgileri\n3. FİYAT - Fiyatlandırma ve ödeme seçenekleri\n4. KURULUM - Montaj süreci ve zamanlama\n\nLütfen bir seçenek belirtin (1-4) veya doğrudan konu yazın."
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
            ],
            'information': [
                "Memnuniyetle! CW Enerji olarak güneş enerjisi sektöründe 10+ yıllık tecrübemizle size en doğru bilgileri sunabiliriz. Özellikle hangi konu hakkında detaylı bilgi almak istersiniz? \n\n🔋 **Teknik Bilgiler**: Panel teknolojileri, verimlilik oranları\n💰 **Finansman**: Fiyatlandırma modelleri, yatırım getirisi\n⚙️ **Kurulum**: Montaj süreci, izinler, zamanlama\n🛡️ **Garanti**: Ürün ve işçilik garantileri\n📈 **Faydalar**: Tasarruf potansiyeli, çevresel etkiler",
                "Harika! CW Enerji olarak güneş enerjisi konusunda size tüm detayları anlatmaktan memnuniyet duyarız. Sizi hangi konuda aydınlatmamı istersiniz?\n\n✅ **Ürün Gamımız**: Monokristalin, polikristalin ve ince film teknolojileri\n✅ **Fiyatlandırma**: Sistem maliyetleri, devlet teşvikleri, geri ödeme süreleri\n✅ **Kurulum Süreci**: Keşiften devreye almaya kadar tüm adımlar\n✅ **Finansman Seçenekleri**: Peşin, kredi ve leasing imkanları\n✅ **Satış Sonrası**: Bakım, monitoring ve teknik destek hizmetlerimiz",
                "Elbette! CW Enerji olarak güneş enerjisi alanında size kapsamlı bilgi sunmak için buradayım. Hangi konuda detaylı bilgi almak istersiniz?\n\n🌞 **Panel Çeşitleri**: Farklı teknolojilerin avantajları ve dezavantajları\n🏠 **Sistem Tasarımı**: Eviniz için en uygun kapasite hesaplaması\n💵 **Maliyet Analizi**: Yatırım miktarı ve tasarruf projeksiyonları\n🔧 **Montaj Süreci**: Teknik detaylar ve zaman çizelgesi\n📞 **Müşteri Hizmetleri**: 7/24 destek ve bakım garantilerimiz"
            ],
            'benefits': [
                "CW Enerji olarak güneş enerjisinin faydalarını şöyle özetleyebiliriz:\n\n💰 **Finansal Avantajlar**:\n• Elektrik faturalarınızda %70-90 arasında tasarruf\n• Yatırımınız 6-8 yılında amorti olur\n• Mülk değerinizi %10-15 oranında artırır\n• Devlet teşvikleri ve vergi indirimlerinden yararlanma\n\n🌱 **Çevresel Katkılar**:\n• Yılda 2-3 ton CO2 emisyonu önler\n• Sürdürülebilir ve temiz enerji kullanımı\n• Gelecek nesillere temiz bir çevre bırakma\n\n🔌 **Teknik Avantajlar**:\n• 25-30 yıl performans garantisi\n• Bakım gerektirmeyen sistemler\n• Şebeke bağlantısı ve elektrik satma imkanı\n\nCW Enerji ile bu faydalardan hemen yararlanmaya başlayın!",
                "CW Enerji ile güneş enerjisine geçmenin sağladığı değerler:\n\n**EKONOMİK KAZANÇLAR**\n💵 Aylık elektrik faturasından %70-90 tasarruf\n📈 Yatırım geri dönüşü 6-8 yıl\n🏠 Evinizin değer artışı (10-15%)\n🎁 Devlet destekleri ve teşvikler\n\n**ÇEVRESEL FAYDALAR**\n🌍 Karbon ayak izinizdeki ciddi azalma\n🌳 Yılda 100'den fazla ağaç eşdeğeri CO2 tasarrufu\n🔋 Temiz ve yenilenebilir enerji kullanımı\n\n**KOLAYLIKLAR**\n⚙️ Minimum bakım gereksinimi\n📱 CW Enerji mobil uygulaması ile takip\n🛡️ 25 yıl ürün garantisi\n📞 7/24 teknik destek hizmetimiz",
                "CW Enerji müşterilerinin yaşadığı dönüşüm hikayeleri:\n\n**MÜŞTERİ YORUMLARINDAN**\n\"İlk 3 ayda faturam %85 azaldı!\" - İstanbul, Aile K.\n\"Yatırımım 6.5 yılda geri döndü.\" - Ankara, İş Adamı\n\"Evimin değeri 45.000 TL arttı.\" - İzmir, Emekli\n\n**KİMLER İÇİN İDEAL**\n✅ Yüksek elektrik faturaları ödeyenler\n✅ Yatırımını değerlendirmek isteyenler\n✅ Çevreye duyarlı bireyler ve kurumlar\n✅ Geleceğe yatırım yapmak isteyenler\n\nCW Enerji olarak 10.000+ mutlu müşterimizle bu dönüşüme liderlik ediyoruz!"
            ],
            'pricing': [
                "CW Enerji olarak şeffaf fiyatlandırma politikası sunuyoruz. Güneş enerji sistemlerimiz kapasiteye göre değişmekle birlikte genel aralık:\n\n**STANDART SİSTEM PAKETLERİ**\n🔋 3 kW (1-2 kişilik hane): 120.000 - 180.000 TL\n🔋 5 kW (3-4 kişilik hane): 180.000 - 280.000 TL\n🔋 7 kW (5+ kişilik hane): 250.000 - 380.000 TL\n🔋 10 kW (Ticari): 350.000 - 550.000 TL\n\n**FİYATA DAHİL OLANLAR**\n✅ CW Enerji yüksek verimli paneller\n✅ European mark inverters\n✅ Profesyonel montaj ekiplerimiz\n✅ Tüm izin ve belgeler\n✅ 25 yıl performans garantisi\n\nSize özel teklif için konum ve tüketim bilginizi paylaşır mısınız?",
                "CW Enerji yatırım maliyetleri ve geri dönüş analizi:\n\n**YATIRIM KALEMLERİ**\n📊 Sistem tasarımı ve keşif: ÜCRETSİZ\n🔋 Güneş panelleri: Kapasiteye göre\n⚡ İnverter ve ekipmanlar: Sistem ile uyumlu\n🔧 Montaj ve kurulum: Profesyonel ekip\n📋 İzin ve resmi işlemler: CW Enerji tarafindan\n\n**GERİ DÖNÜŞ PROJEKSİYONU**\n💰 Aylık tasarruf: 1.500 - 8.000 TL\n📅 Amorti süresi: 6-8 yıl\n🏠 Mülk değeri artışı: %10-15\n🌱 Çevresel katkı: Yılda 2-3 ton CO2\n\nTam bir maliyet analizi için aylık tüketiminizi ve şehir bilginizi alabilir miyim?",
                "CW Enerji olarak esnek ödeme seçenekleri sunuyoruz:\n\n**PEŞİN ÖDEME AVANTAJLARI**\n💎 %5-10 indirim imkanı\n⚡ Hızlı kurulum (15-20 gün)\n🎁 Ekstra 1 yıl bakım garantisi\n\n**KREDİ SEÇENEKLERİ**\n🏦 0 faizli kredi imkanları\n⏳ 12-48 ay taksit olanakları\n📋 Minimum evrak ile hızlı onay\n\n**LEASING MODELLERİ**\n🔄 Kira öder gibi öde, senin olsun\n📈 Bütçeni zorlamadan yatırım\n🛡️ Bakım ve sigorta dahil\n\nHangi finansman modeli sizin için uygun? Size özel detaylı teklif hazırlamak için bilgilerinizi bekliyorum."
            ],
            'types': [
                "CW Enerji olarak sunmuş olduğumuz güneş paneli teknolojileri:\n\n**🏆 MONOKRİSTALİN PANELLER**\n✅ Verimlilik: %22-24 (en yüksek)\n✅ Garanti: 25 yıl performans\n✅ Alan: Daha az alanda daha fazla enerji\n✅ Özellik: Lüks segment, maksimum performans\n✅ Uygun: Alanı kısıtlı olanlar için ideal\n\n**💎 POLİKRİSTALİN PANELLER**\n✅ Verimlilik: %17-19 (dengeli)\n✅ Garanti: 25 yıl performans\n✅ Fiyat: En iyi performans/fiyat oranı\n✅ Özellik: En çok tercih edilen model\n✅ Uygun: Standart konutlar için mükemmel\n\n**🔧 İNCE FİLM (THIN-FILM) PANELLER**\n✅ Verimlilik: %12-15 (esnek)\n✅ Garanti: 20 yıl performans\n✅ Özellik: Esnek, hafif, kıvrılabilir\n✅ Uygun: Özel mimari projeler için\n\nCW Enerji teknik ekibi, ihtiyaçlarınıza en uygun panel teknolojisini belirlemek için ücretsiz keşif hizmeti sunar.",
                "CW Enerji ürün gamı ve karşılaştırma:\n\n**TEKNİK ÖZELLİKLER**\n📊 **Monokristalin**: Tek kristal silikon, koyu renk, yüksek verim\n📊 **Polikristalin**: Çoklu kristal silikon, mavi renk, dengeli verim\n📊 **Thin-Film**: Amorf silikon, esnek yapı, özel uygulamalar\n\n**FİYAT PERFORMANS ANALİZİ**\n💰 **Monokristalin**: Yüksek yatırım, hızlı geri dönüş\n💰 **Polikristalin**: Dengeli yatırım, standart geri dönüş\n💰 **Thin-Film**: Düşük yatırım, özel proje odaklı\n\n**CW ENERJİ ÖNERİSİ**\n🏠 **Konut için**: Polikristalin (en çok tercih)\n🏢 **Ticari için**: Monokristalin (maksimum verim)\n🏭 **Endüstriyel**: Özel projelere göre belirlenir\n\nHangi panel türü ilginizi çekiyor? Detaylı teknik spektasyonları paylaşabilirim.",
                "CW Enerji panel seçim kriterleri:\n\n**PERFORMANS DEĞERLENDİRMESİ**\n⚡ Çatı alanınızın büyüklüğü\n⚡ Hedeflenen enerji üretimi\n⚡ Bütçe ve yatırım geri dönüşü beklentisi\n⚡ Estetik görünüm tercihi\n\n**TEKNİK SEÇİM YARDIMI**\n🔍 **Küçük çatılar için**: Monokristalin (minimum alan, maksimum enerji)\n🔍 **Standart çatılar için**: Polikristalin (en iyi fiyat/performans)\n🔍 **Büyük alanlar için**: Polikristalin (ekonomik ve verimli)\n🔍 **Özel tasarımlar için**: Thin-Film (kıvrılabilir, esnek)\n\n**CW ENERJİ AVANTAJI**\n📋 Ücretsiz çatı analizi ve kapasite hesaplaması\n📋 3 farklı panel seçeneği ile karşılaştırmalı teklif\n📋 10 yıl işçilik garantisi ek olarak\n\nSize özel panel önerisi için çatı ölçülerinizi ve enerji hedeflerinizi paylaşabilir misiniz?"
            ],
            'installation': [
                "CW Enerji kurulum sürecimiz şu şekilde ilerler:\n\n**📋 FAZ 1: ÖN ANALİZ VE KEŞİF (1-2 GÜN)**\n🔍 Teknik ekip ziyareti ve çatı ölçümleri\n📊 Enerji ihtiyaç analizi ve sistem kapasitesi belirleme\n💻 Detaylı proje tasarımı ve 3D modelleme\n📋 Resmi izinler için başvuru hazırlığı\n\n**📋 FAZ 2: İZİN SÜREÇLERİ (7-15 GÜN)**\n🏢 Belediye izinleri\n⚡ Şebeke başvurusu (TEDA/EPİAŞ)\n📄 Tüm yasal belgelerin tamamlanması\n✅ CW Enerji tüm süreçleri yönetir\n\n**📋 FAZ 3: KURULUM (1-3 GÜN)**\n🔧 Montaj ekiplerinin yerleştirilmesi\n⚙️ Panel ve inverter montajı\n🔌 Elektrik bağlantıları\n📱 Sistemin devreye alınması\n\n**📋 FAZ 4: TEST VE TESLİMAT (1 GÜN)**\n✅ Performans testleri\n📞 Mobil uygulama eğitimi\n📋 Garanti belgeleri teslimi\n🎉 Sistemin kullanıma başlaması\n\nCW Enerji olarak baştan sona tüm süreçleri sizin için yönetiyoruz!",
                "CW Enerji montaj zaman çizelgesi ve detayları:\n\n**HAFTA 1: HAZIRLIK SÜRECİ**\n📋 Gerekli belgelerin listelenmesi\n📊 Teknik değerlendirme raporu\n💰 Kesin fiyat teklifi sunumu\n✅ Sözleşme imzalanması\n\n**HAFTA 2: İZİN BAŞVURULARI**\n🏛️ Belediye ve kurum izinleri\n⚡ Elektrik dağıtım şirketi başvurusu\n📋 Tüm resmi prosedürler\n📞 Süreç takibi ve bilgilendirme\n\n**HAFTA 3-4: KURULUM HAFTASI**\n👷 Profesyonel montaj ekibi (3-5 kişi)\n🔧 Ekipman ve malzeme teslimi\n⚙️ Panel montajı (1-2 gün)\n🔌 Elektrik bağlantıları (1 gün)\n\n**HAFTA 4: DEVRE TESLİMİ**\n✅ Son kontroller ve testler\n📱 CW Enerji mobil uygulaması kurulumu\n📓 Eğitim ve kullanım kılavuzu\n🎇 Devreye alma ve enerji üretimi başlangıcı\n\nToplam süre: ortalama 3-4 hafta. CW Enerji kalitesi ile!",
                "CW Enerji kurulum hizmet detayları:\n\n**MONTAJ EKİBİMİZ**\n👷‍♂️ Sertifikalı elektrik mühendisleri\n👷‍♂️ Deneyimli montaj teknisyenleri\n👷‍♂️ İş güvenliği uzmanları\n📱 Proje koordinatörleri\n\n**KULLANILAN MALZEMELER**\n🔩 Alman standartlarında montaj aparatları\n⚡ Avrupa kalitesinde kablo ve bağlantılar\n🛡️ Yangın güvenlikli sistemler\n📊 Performans monitoring cihazları\n\n**KURULUM SONRASI**\n📱 7/24 mobil uygulama ile takip\n📞 Acil durum müdahale ekibi\n🔋 Yıllık bakım ve performans kontrolü\n📊 Detaylı üretim raporları\n\n**CW ENERJİ FARKI**\n✅ Tüm izin ve belgeleri biz hallederiz\n✅ Sigorta ve garanti işlemleri dahil\n✅ 10 yıl işçilik garantisi\n✅ Ücretsiz ilk yıl bakım hizmeti\n\nKurulum tarihi için şimdi ön rezervasyon yapabilirsiniz!"
            ],
            'maintenance': [
                "Güneş panelleri çok düşük bakım gerektirir! Sadece yılda 2-4 kez temizleyin ve enkazı kaldırın. 25 yıl garantili gelirler ve minimum bozulma ile tipik olarak 30+ yıl sürerler. Bu kadar basit!",
                "Bakım inanılmaz derecede kolay! Panellerinizi yılda 2-4 kez temizleyin ve herhangi bir yaprağı veya enkazı kaldırın. Panelleriniz 25 yıl garantili gelirler ve zaman içinde çok az performans kaybı ile 30+ yıl dayanacak şekilde tasarlanmıştır.",
                "Güneş panelleri minimum bakım gerektirir. Onları mevsimsel olarak (yılda 2-4 kez) temizleyin ve enkazdan uzak tutun. 25 yıl garantiler içerir ve çoğu sistem mükemmel performans ile 30+ yıl sürer. Çok az bakım gerekir!"
            ],
            'financing': [
                "Esnek finansman sunuyoruz: 1) Peşinatsız güneş kredileri, 2) Güç Satın Alma Anlaşmaları (PPA), 3) Güneş kiralamaları, ve 4) İndirimli nakit alımlar. Çoğu müşteri peşin ödeme olmadan ilk günden tasarruf eder!",
                "Finansman esnek ve erişilebilirdir! Peşinatsız güneş kredileri, mevcut elektrik tarifelerinden daha az ödediğiniz Güç Satın Alma Anlaşmaları, bakım sorumluluğu olmayan güneş kiralamaları ve indirimli nakit alımlar sunuyoruz. Birçok seçenek peşin ödeme olmadan başlar!",
                "Güneş enerjisine geçmeyi birden çok finansman seçeneği ile uygun hale getiriyoruz: Rekabetçi oranlarla peşinatsız krediler, daha düşük oranlarla güç satın aldığınız PPAlar, bakım endişesi olmayan kiralamalar ve anlık indirimlerle nakit alımlar. Çoğu müşteri ilk günden tasarruf görür!"
            ],
            'warranty': [
                "Panellerimiz sektör lideri garantilerle gelir: 25 yıl performans garantisi (%85 çıktı), 10 yıl işçilik garantisi ve 25 yıl inverter garantisi. Ürünlerimizin tamamen arkasındayız!",
                "Kapsamlı garantilerle korunursunuz: %85 çıktı sağlayan 25 yıl performans garantisi, kurulum kalitesini kapsayan 10 yıl işçilik garantisi ve 25 yıl inverter garantisi. Her kurulumun tamamen arkasındayız!",
                "Garanti kapsamı mükemmeldir: 25 yıl performans garantisi (paneller %85 çıktıyı korur), 10 yıl işçilik garantisi ve 25 yıl inverter garantisi. Yatırımınız on yıllarca korunur!"
            ],
            'goodbye': [
                "CW Enerji ailesi olarak zaman ayırdığınız için teşekkür ederiz. Temiz enerjiye geçiş yolculuğunuzda her zaman destekçiniziz. Güneşli günler dileriz!",
                "Hoşça kal! CW Enerji olarak güneş enerjisi hakkında daha fazla bilgi almak istediğinizde bize ulaşmaktan çekinmeyin. Enerji bağımsızlığı hedefinizde size destek olmaktan mutluluk duyarız!",
                "Güneş enerjisine gösterdiğiniz ilgi için CW Enerji olarak teşekkür ederiz! Unutmayın, her güneşli gün temiz bir gelecek için yeni bir fırsattır. Bize her zaman ulaşabilirsiniz!"
            ],
            'thanks': [
                "Rica ederim! CW Enerji olarak en doğru güneş enerjisi çözümünü bulmanız için buradayız. Başka sorunuz olursa çekinmeyin!",
                "Memnuniyetle! CW Enerji ailesi olarak güneş enerjisinin faydalarını paylaşmaktan mutluluk duyaruz. Sizi aydınlatmak için buradayız.",
                "Çok teşekkürler! CW Enerji olarak müşterilerimizin bilinçli kararlar vermesine yardımcı olmayı biz bir görev olarak görüyoruz. Başka nasıl yardımcı olabilirim?"
            ],
            'default': [
                "CW Enerji olarak güneş enerjisi sistemlerinde uzmanız. Size nasıl yardımcı olabilirim? Güneş paneli fiyatlandırması, kurulum süreci, finansman seçenekleri veya teknik bilgiler hakkında detaylı bilgi alabilirsiniz.",
                "CW Enerji teknik ekibi olarak sorularınızı yanıtlamak için buradayız. Güneş enerjisi yatırım getirisi, sistem kapasitesi, panel teknolojileri veya devlet teşvikleri hakkında bilgi almak ister misiniz?",
                "CW Enerji'den merhaba! Güneş enerjisi çözümlerimiz hakkında sizi nasıl aydınlatabilirim? Ücretsiz keşif, fiyat teklifi veya teknik bilgilendirme konularında size yardımcı olabilirim."
            ]
        }

    def get_intent(self, message):
        """Simple rule-based intent detection for Turkish"""
        message_lower = message.lower()

        # Greeting patterns in Turkish
        if any(word in message_lower for word in ['merhaba', 'selam', 'hey', 'günaydın', 'iyi geceler', 'selamlar']):
            return 'greeting'

        # Selling/purchase intent in Turkish
        if any(word in message_lower for word in ['satın al', 'almak istiyorum', 'satın almak istiyorum', 'isteği', 'ihtiyacım var', 'arıyorum', 'ilgileniyorum', 'al', 'alsam']):
            if any(word in message_lower for word in ['güneş paneli', 'güneş', 'panel']):
                return 'selling'

        # Information seeking in Turkish
        if any(word in message_lower for word in ['söyle', 'bilgi', 'öğrenmek', 'açıkla', 'nedir', 'nasıl çalışır', 'hakkında']):
            if any(word in message_lower for word in ['güneş paneli', 'güneş', 'panel']):
                return 'information'

        # Specific topics in Turkish
        if any(word in message_lower for word in ['fayda', 'avantaj', 'neden', 'iyi olan']):
            return 'benefits'

        if any(word in message_lower for word in ['maliyet', 'fiyat', 'ne kadar', 'pahalı', 'yatırım', 'bütçe']):
            return 'pricing'

        if any(word in message_lower for word in ['tip', 'çeşit', 'kategori', 'seçenek', 'farklı']):
            return 'types'

        if any(word in message_lower for word in ['kur', 'kurulum', 'montaj', 'tak', 'yerleştir']):
            return 'installation'

        if any(word in message_lower for word in ['bakım', 'temiz', 'koru', 'gözlem']):
            return 'maintenance'

        if any(word in message_lower for word in ['finans', 'finansman', 'kredi', 'ödeme', 'borç', 'taksit']):
            return 'financing'

        if any(word in message_lower for word in ['garanti', 'korumak', 'güvence']):
            return 'warranty'

        # Goodbye patterns in Turkish
        if any(word in message_lower for word in ['hoşça kal', 'görüşürüz', 'kendine iyi bak', 'sonra']):
            return 'goodbye'

        # Thanks patterns in Turkish
        if any(word in message_lower for word in ['teşekkür', 'sağol', 'yardım', 'minnettar']):
            return 'thanks'

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

        # Simple energy usage extraction (supports Turkish and English)
        energy_pattern = r'(\d+)\s*(?:kwh|kilowatt|kilovatsaat)'
        match = re.search(energy_pattern, message_lower)
        if match:
            entities['energy_usage'] = int(match.group(1))

        return entities

    def calculate_recommendation(self, location=None, energy_usage=None):
        """Calculate personalized recommendation in Turkish"""
        if not energy_usage:
            energy_usage = 1000  # Default

        if not location:
            location = "bölgenizde"

        # Simple calculations with Turkish currency
        daily_usage = energy_usage / 30
        system_size = round(daily_usage / 5 * 1.5, 1)
        system_watts = system_size * 1000
        # Using Turkish Lira pricing
        price = round(system_watts * 30 / 1000, 0)  # TL per watt
        bill_reduction = min(95, max(70, int(system_size * 8)))

        return {
            'system_size': system_size,
            'price': price,
            'bill_reduction': bill_reduction,
            'location': location
        }

    def get_response(self, message):
        """Get response for user message"""
        intent = self.get_intent(message)
        entities = self.extract_entities(message)

        # Store user data
        if entities:
            self.user_data.update(entities)

        # Check if we have location and energy usage for recommendation
        if 'location' in self.user_data and 'energy_usage' in self.user_data and intent in ['selling', 'pricing']:
            rec = self.calculate_recommendation(self.user_data['location'], self.user_data['energy_usage'])
            response = f"**CW ENERJİ ÖZEL TEKLİFİ**\n\n📍 **Konum**: {rec['location']}\n⚡ **Aylık Tüketim**: {self.user_data['energy_usage']} kWh\n🔋 **Önerilen Sistem**: {rec['system_size']} kW kapasite\n💰 **Yatırım Miktarı**: {rec['price']:,.0f} TL\n📈 **Fatura Tasarrufu**: %{rec['bill_reduction']}\n\n**DETAİLİ ANALİZ**\n💵 Aylık tasarruf potansiyeli: 1.500-6.000 TL\n📅 Yatırım geri dönüşü: 6-8 yıl\n🏠 Mülk değeri artışı: %10-15\n🌱 Çevresel katkı: Yılda 2-3 ton CO2 azaltma\n\n**CW ENERJİ AVANTAJLARI**\n✅ Ücretsiz keşif ve proje tasarımı\n✅ 25 yıl performans garantisi\n✅ 10 yıl işçilik garantisi ek olarak\n✅ Tüm izin ve belgelerin takibi\n✅ 7/24 teknik destek hizmeti\n\nBu özel teklifle ilgili detaylı bilgi almak ister misiniz? Finansman seçenekleri veya kurulum takvimi hakkında size yardımcı olabilirim."
            return response

        # Get standard response
        response_options = self.responses.get(intent, self.responses['default'])
        return random.choice(response_options)

    def reset_conversation(self):
        """Reset conversation data"""
        self.user_data = {}
        self.conversation_history = []
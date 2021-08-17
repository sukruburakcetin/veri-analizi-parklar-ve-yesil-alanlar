# veri-analizi_parklar-ve-yesil-alanlar
İstanbul Büyük Şehir Belediyesi Açık Veri Portalı'ndan Elde Edilmiş Veri Üzerinden İstanbul'daki Parklar ve Yeşil Alanların İlçe Bazında Çeşitli Sosyokültürel Değerlerle İlişkilendirilip Analiz Edilmesi

İstanbul Bahçelievler'de büyüdüm. Bu süreçte bir ilçenin, tüm etnik kültür farklılıklarını içerdiği beldelerinde gözlem yapma fırsatım oldu. Özellikle bu süreçte, lise sınavlarına hazırlandığım esnada dershanelere giderken ve daha sonraki üniversite dönemim boyunca da yine aynı lokasyon boyunda eğitim hayatımı sürdürürken, hedef bölgeye ulaşırken istemeden de olsa merak ettiğim bir olgu keşfetmiştim.

Komşu ilçelerde, kendi aralarında küçücük mesafeler olmasına rağmen, yeşil alanlar(ormanlar/korular) ve parkların eşit dağılmadığına dair bir kanı oluşmuştu.

Özellikle Bahçelievler/Şirinevler bölgesi ile Bakırköy/Ataköy bölgeleri arasında bu ilçeleri sadece bir köprü ile bağlanıyor olmasına rağmen, Şirinevler'deki ağaçsız ve olabildiğince aktif yeşil alan sayısının Ataköy gibi bir yere göre --gözlemlerime göre-- çok az olması ve özellikle bu süreçte nüfus olarak da Şirinevler'in Ataköy'e göre --gözlemlerime göre-- fazla olmasına rağmen bu aktif yeşil alanlardaki durum bana bu düzende bir eşitsizlik olduğu çağrıştırıyordu. 

Ben de bu durumu incelemek istedim. Özellikle nüfus ve yıllık ortalama gelire göre bu dinamiklerin değişebileceğini düşünerek yola çıkmak istedim. Çünkü özellikle içinde yaşadığım bu alanda ekonomik ve nüfus bakımından ciddi artılar ve eksiler vardı.

Şimdi TESEV'in Yazar Author Bürge Elvan Erginli // Haritalama Mapping Murat Güvenç, Murat Tülek'in önderliğinde 2019'da İstanbul için oluşturduğu rapor üzerinden de baktığımızda bariz bir fark olduğu gözlemlenmektedir.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Data/Non-GIS%20data/external/bahcelievler_veriler.PNG?raw=true)
![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Data/Non-GIS%20data/external/bakirkoy_veriler.PNG?raw=true)

Bu durumu Pearson korelasyon katsayısı üzerinden de analiz ederek, bu farkındalık gibi gözüken olguyu kısmen de olsa nümerik açıdan desteklemek istedim.

Bunun için İBB'nin Veri Portalı kısmında (https://data.ibb.gov.tr/dataset/parklar-ve-yesil-alanlar) Park Bahçe ve Yeşil Alanlar Daire Başkanlığı'nın düzenlediği veriyi kullanmaya karar verdim.

Biraz veri üzerinde manipülasyonlar yaptım ve veri üzerinde ayıklama yaparak kaçı Park, kaçı Koru/Orman, kaçı Mesare Alanı diye bunları etiketledim ve yine diğer kullandığım yıllık gelirler tablosu ile "join/birleştirme" yapabilmek için İlçe isimlerini doğru formata çektim.

Daha sonra Parklar'ı da kendi içinde Park isimlerinde geçen "Çocuk" ya da "Spor Alanı" ibareleriyle yeni ilgi alanları kategorisi ekledim.

Verileri kesiştirdiğim yıllık gelirler tablosunu İstanbul Üniversitesi İktisat Fakültesi’nin yürüttüğü İstanbul Kalkınma Ajansı’nın desteklediği Mahallem İstanbul projesinin İstanbul’da gelir dağılımıyla ilgili analiz sonuçları üzerinden oluşturdum.

![alt text](https://i.pstimaj.com/img/78/0x1060/5ae1f42eae298b8e0125189a.jpg)

Daha sonra bu veriyi, ilçe nüfusunun, yıllık ortalama hane halkı gelirinin bulunduğu tabloyu TESEV'in aktif yeşil alan sayısı ve kişi başına m2 bazında düşen yeşil alan sayısıyla zenginleştirdim.

İBB Veri Portalındaki Parklar ve Yeşil Alanlar veri setindeki ilçe bazındaki dağılımını gösteren bir koroplet(chloropleth) harita çıkardım. Bu haritayı çıkarırken (https://data.humdata.org/dataset/turkey-administrative-boundaries-levels-0-1-2) sitesinden Türkiye il ve ilçe verilerini indirdim. ArcGIS Map üzerinden İstanbul ilini sorgu çekerek ekstrak ettim. 

İstanbul'a ait GIS datası(shapefile) çıkarma:

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Data/Non-GIS%20data/external/istanbul_ilini_cikti_al.png?raw=true)

Yüksek yoğunluktaki renkler sayı ile doğru orantılı şekilde tonlama şiddetini göstermektedir.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/yayilim/yayilim_tr.svg?raw=true)

Koroplet haritaya göre sadece sayılara bakılarak söz konusu farkındalığı kanıtlayabilir bir veri oluşturamıyoruz. Bu veriye göre daha çok kıyı kesimlerdeki ilçelerde park sayısının iç kesimlere göre daha fazla olduğunu söyleyebiliriz. Projemin ileriki aşamalarında 2D uydu görüntüsü üzerinde de karşılaştırabileceğimiz gibi bu dağılımın ilin coğrafik yeşil alan miktarıyla da ilgili olmadığını söyleyebilirim.

Bu hariya göre başlıca iller Eyüpsultan, Üsküdar, Ümraniye, Kartal.

Veriyi çeşitlendirirken ismine göre ayıkladığımdan bahsetmiştim. İsminde Koru, Orman, Mesire geçenleri etiketleyip bir bar grafiği oluşturdum. Bu verileri kısmen de olsa destekeyip kanıtlamak için de yine İBB Veri Portalındaki "https://data.ibb.gov.tr/dataset/2019-yili-park-bahce-ve-yesil-alan-verileri" veri setiyle de teyit ettim. Sadece 2019 içerdiği için kısmen uyuşmasa da özellikle Mesire ve Ormanları veri içerinden ayıklamada paralellik gösterdiğini, incelediğim (https://data.ibb.gov.tr/dataset/parklar-ve-yesil-alanlar) veri setinin kendi içinde tutarlı olduğunu söyleyebilirim.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/turler/turler_genel_tr.png?raw=true)

Veriyi bölgesel bazda da açarak, sunumu çeşitlendirmek adına Bahçelievler ve Beyoglu illerinde de mahallelere göre inceledim.

İBB ek hizmet binası Kasımpaşa'da olduğu için oraya ait küçük bir analiz göstermek istedim.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/turler/turler_beyoglu_genel_tr.png?raw=true)

Yine yaşadığım ilçeye ait (https://data.ibb.gov.tr/dataset/parklar-ve-yesil-alanlar) veri setinden mahalle bazında park ve yeşil ormanlar ayıklaması yapıp, bar grafikti sunmak istedim.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/turler/turler_bahcelievler_genel_tr.png?raw=true)

Parkların kendi arasında isme göre ayıklanarak sadece "Çocuk Parkı" geçen parkları Çocuk Parkı olarak etiketleyip, Spor olanları Spor olarak etiketleyip, detay verilmeyenleri genelleştirilmiş olarak aktardım ve bunu bar grafikte gösterdim.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/turler/turler_sadece_parklar_tr.png?raw=true)

İBB Veri Portalından elde ettiğimiz veri üzerinden nüfus ve yıllık gelire göre ilişkilendirmesini inceleyebiliriz.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/nufus/nufus_ibb_tr.svg?raw=true)

Parkların farklı değişkenlerle korelasyonuna baktığımızda nüfus ile ilçe bazındaki park sayısılarının kısmen de olsa, zayıf bir ağırlıkta bağlatısı var diyebiliriz. 

Pearson katsayısında değer pozitif olduğu sürece iki değer arasında doğru orantı vardır. Eğer negatifse ters orantılıdır.
Pearson katsayısı 0.8'in üstünde olduğunda yüksek oranda bağlantı var diyebiliriz.

Bu grafiğe göre park sayılarının ilçe bazında dağılımlarının yıllık ortalama hane halkı geliriyle alakalı olmadığını çıkarabiliriz(r=0.09) ya da bir bağlantı söz konusu olup olmadığı konusunda tam fikir elde edemedik diyebiliriz.

Bu veri setinden elde ettiğim korelasyon değerlerinde ilçe bazında yıllık ortalama hane halkı gelirinin bağımsız olması ayrıca farklı veri kümesi oluşturup, bu değerlendirmeleri incelemem için beni teşvik etti ve TESEV'in yukarıda da kısmi görsellerini aktardığım  "Aktif Yeşil Alan" miktarı ile "Kişi Başına m2 Bazında Düşen Yeşil Alan Miktarı" verileri üzerinden yine nüfus ve yıllık gelir bazında ilişkilendirmesini incelemek için yola koyuldum.

Bu verileri (https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Data/Non-GIS%20data/external/rapor_istanbul95.rapor_1.pdf) projeye de eklediğim pdf dosyasından çıkardıktan sonra korelasyon işlemine başladım.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/nufus/nufus_alt_population_tr.svg?raw=true)

Burada alternatif data üzerinden analiz sonucuna bakılacak olursa, koroplet görselin vurgu alanları tamamen değişti. Önceki veriye göre Eyüpsultan başı çekerken, şimdi Bakırköy başta gelmektedir. Tabi bu sonucu etkileyen sadece aktif yeşil alanlara bakılıyor olmasıydı. Daha önceki verimizde her ne kadar adres içerikli parklar olsa da, aktif yeşil alan miktarını etkileyen koru, orman, mesire alanları analiz fikrine ulaşmamızı uzaklaştırıyordu.

Bu görselde Aktif Yeşil Alan sayısının nüfus ile bağlantısı daha da güçsüzleşmektedir. Şirinevler ve Ataköy karşılaştırmasında da, Şirinevler'de nüfus artarken park sayısının Ataköy'ün nufüsunun az olmasına rağmen düşük olmasını buna bağlayabiliriz.

Verinin kendi içinde doğru bir korelasyon oluşturup oluşturmadığını gözlemlemek için de, Aktif Yeşil Alanlar ile Kişi Başına m2 Bazında Düşen Alan Miktarının birbiriyle ilişkisini inceledim ve 0.70 korelasyon pearson r değeriyle verinin kendi içinde kararlı olduğunu ve analiz edilebilir nitelikte olduğunu söyleyebilirim.

Bu verinin kendi içinde stabil olması beni heyecanlandırdı ve veriyi hemen yıllık ortalama hane halkı bazında da incelemek istedim.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/gelir/gelir_alt_gelir_tr.svg?raw=true)

Burada da görüldüğü üzere, yıllık ilçe bazındaki ortalama hane gelir miktarının, nufüs ve aktif yeşil alanların kendi arasındaki zayıf bağlantının aksine güçlü bir bağlantıya sahip olduğunu pearson katsayısı r = 0.59 ile söyleyebiliriz.

Kısacası 1. veride nüfus 0.38, yıllık gelir 0.09 pearson katsayısı ile sonuçlanırken,

diğer yandan 2. veride nüfus 0.22, yıllık gelir ise 0.59 pearson katsayısı ile bağdaşım göstermektedir.

--

2D uydu görüntülerinden elde ettiğim koroplet haritanın sınır çizgilerini label olarak baz alıp, bu alanlar içerisine denk gelen gerçeğe yakın olan coğrafik görüntünün ilçe alanları üzerindeki yeşil olma durumunu 0 ile 9 katsayıları arasında etiketlemek istedim.

Buradaki amaç alan içinde ne kadar yeşil alan varsa katsayının da görüntü analizi sonrası puanlama gücü o derece artmaktadır.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/analizi/analizi_figure.png?raw=true)

Bu çıktıları almak için koroplet haritanın sınırlarını modlanmış canny edge detection kullanarak elde ettim.

Daha sonra findContours algoritması ile bu sınır bölgeleri ekstrakt edilmiş alanları vektör dizinine aktardım.

Daha sonra oluşabilecek küçük konturları elemek için bir filtreden geçirdim.

Elde ettiğim incelenebilir kontor alanlarını(ilçe bölgelerini), maphills sitesinden elde ettiğim 2D İstanbul uydu görüntüsü üzerine flatten ederek(yani kaplayarak), tüm bölgeleri sırasıyla kırptım.

Kırpılan bölgelerin dominant renklerini k-mean clustering algoritması kapsül ettim. Ortalama piksel değerini almak yerine domine eden rengi almak önemliydi. Çıktıları (https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/tree/main/Data/Non-GIS%20data/external/stash) klasörde inceleyebilirsiniz.

Sınıf olarak 1 kullandım çünkü en yoğun piksel değeri benim için yeterliydi.

Daha sonra bu en yoğun kapsüllenmiş domine rengin 3 boyutlu değerlerinin medyanını alarak gri skaladaki karşılığını buldum.

Gri skaladaki rengi belirli aralıklarla puanladım. Test ederken yeşil renge yakınlık gösterenlerin gri skala ortalama değerinin 130'dan düşük olduğunu tespit ettim.

Değer düştükçe, yeşil alan oranı katsayısını optimize ettim.

Bu sayede çıktı görüntüde ne kadar yeşil alan çoksa o kadar yüksek puan alacaktır.

Burada kuzey kesimlerde daha çok yeşil alan olduğu için bölgeler 5 puan alırken, daha düşük alanlar 3 puan almaktadır.

![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/analizi/analizicontoursOverlayed.png?raw=true)

Görüntüyü analiz etmek zorlaştığı için, elde ettiğim yeşil alan indekslerini excell dosyasına çıkarttım ve bu dosyadan verilere şehir bazında yine erişerek bir koroplet harita ve bar grafiği oluşturdum.


![alt text](https://github.com/sukruburakcetin/veri-analizi_parklar-ve-yesil-alanlar/blob/main/Scripts/Working%20Scripts/Data%20Analysis%20and%20Visualization%20Scripts/Data%20Analysis_Istanbul%20Parks%20and%20Green%20Areas%20Map/Media/Plots/analizi/analizi_figur_koroplet_ve_bar.svg?raw=true)




# CacheClean

Bu scriptin yazılma amacı, apache sunucularının diskte tuttukları cache boyutu yönetme ihtiyacıdır.Apache server yazılımının hazırda bunu yapan bir eklentisi mevcuttur fakat yüksek I/O yapan ve hızlı disklere sahip olan sistemlerde performans sorunu yaratmaktadır.- Biz yaşadık =) Hani çamur atmak gibi olmasın. -

Scriptimiz, config dosyasına girdiğiniz parametreler doğrultusunda çalışmaya başlar.Verdiğiniz dosya yolunu, belirlediğiniz süre aralığında kontrol eder, eğer boyut belirlediğiniz boyutun üzerindeyse listelediği dosyaları oluşturulma zamanına göre sıralar ve en eskisinden başlayarak silme işlemini başlatır.Her silme işleminden sonra toplam boyutu kontrol eder.Eğer ulaşılan boyut, belirlediğiniz minimum boyuta eşit yada altındaysa silme işlemini durdurur ve log dosyasına yazar. - Evet, log dosya yolunu da siz belirtiyorsunuz =) -
Böylelikle tuttuğunuz cachelerden en fazla verimi almanız sağlanır.

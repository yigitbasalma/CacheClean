# CacheClean

Bu scriptin yazılma amacı, apache sunucularının diskte tuttukları cache boyutu yönetme ihtiyacıdır.Apache server yazılımının hazırda bunu yapan bir eklentisi mevcuttur fakat yüksek I/O yapan ve hızlı disklere sahip olan sistemlerde performans sorunu yaratmaktadır.- Biz yaşadık =) Hani çamur atmak gibi olmasın. -

Scriptimiz, config dosyasına girdiğiniz parametreler doğrultusunda çalışmaya başlar.Verdiğiniz dosya yolunu, belirlediğiniz süre aralığında kontrol eder, eğer boyut belirlediğiniz boyutun üzerindeyse listelediği dosyaları oluşturulma zamanına göre sıralar ve en eskisinden başlayarak silme işlemini başlatır.Her silme işleminden sonra toplam boyutu kontrol eder.Eğer ulaşılan boyut, belirlediğiniz minimum boyuta eşit yada altındaysa silme işlemini durdurur ve log dosyasına yazar. - Evet, log dosya yolunu da siz belirtiyorsunuz =) -
Böylelikle tuttuğunuz cachelerden en fazla verimi almanız sağlanır.

Şuan için boyutu 1KB altı olan dosyalarla ilgili blok size değerlerinde yaşanan bir sıkıntı yüzünden tam boyutu alamıyoruz.Arada 4 GB kadar bir aşağı sapma bulunuyor. Maksimum ve minimum boyutları bunu göz önünde bulundurarak tanımlamalısınız.İleriki versiyonlarda bu durum fixlenecektir.

Script, cache level 2 olan her yerde kullanılabilir.Burdan kasıt; cache dosyalarının <cache_path>/a/a/cache.header şeklinde tutulmasıdır.Bu ayarlar Apache ve Nginx için config dosyalarında yapılmaktadır.Farklı level kullanımlarına ayak uydurabilmek için sonraki versiyonlarda scriptin config dosyasına bu özelliği de ekleyeceğim.

Scripti chkconfig ile kullanmak veya kolayca başlatıp sonlandırmak için "cacheclean" dosyasını, /etc/init.d altına atarak aşağıdaki komutu çalıştırmanız yeterli.Artık sunucunuz açılırken script servis olarak başlayacaktır.

NOT: Kullanmadan önce script içindeki "schome" değişkenine, scriptin bulunduğu yolu yazmayı unutmayın.

```
chkconfig cacheclean on
```

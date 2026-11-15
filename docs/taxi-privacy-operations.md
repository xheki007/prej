# Privatësia dhe fshirja: vendimet operative para publikimit

Status: përgatitje për shqyrtim, jo procedurë e shpallur si e aktivizuar. Asnjë e dhënë ekzistuese nuk është fshirë nga kjo punë.

## Kanali i kërkesave

Faqja statike përgatit një email te kontakti publik ekzistues i PREJ. Dërgimi bëhet nga përdoruesi në shërbimin e tij të emailit. Faqja nuk pranon formular, nuk ruan telefonin dhe nuk bën kërkesa rrjeti me të dhënat e llogarisë. Alternativa manuale funksionon pa JavaScript dhe pa aplikacion emaili të parazgjedhur.

Kërkesa duhet të përfshijë aplikacionin, telefonin e llogarisë dhe fushëveprimin. Kërkuesit nuk i kërkohen fjalëkalime, OTP ose dokumente identiteti me email. Një email nga një adresë e panjohur nuk është provë e pronësisë së numrit të telefonit.

## Vendimi i pronarit dhe pjesët e hapura

- PREJ merr dhe regjistron kërkesën, pastaj verifikon pronësinë përmes kanalit të llogarisë. Mos dërgo kurrë OTP te personeli; përdor një rrjedhë të kontrolluar verifikimi.
- Pronari miratoi shprehimisht më 15.11.2026 përfundimin e fshirjes së të dhënave të zakonshme të llogarisë brenda 30 ditëve nga verifikimi. Ky është afat operacional i miratuar, jo afat ligjor i pretenduar. Miratimi nuk provon zbatimin teknik dhe nuk autorizon fshirjen e të dhënave reale pa kërkesë të verifikuar. Afatin e faturave pronari do ta konfirmojë më vonë.
- Llogaria e përbashkët Rider/Driver kërkon sqarim nëse kërkesa prek të dy rolet. Mos fshi të dhënat e një personi tjetër ose të një flote tjetër.
- Ruajtja e faturave/dëftesave duhet të përcaktohet nga operatori dhe kontabilisti sipas detyrimeve që zbatohen realisht. Nuk është caktuar një numër vitesh me supozim. PREJ SH.P.K. si ofrues platforme duhet të dallohet nga transportuesi që lëshon dëftesën.
- Duhet miratuar periudha për historikun jo financiar, dokumentet e shoferit, regjistrat e sigurisë dhe kopjet rezervë. Një datë `expiresAt` pa punë të planifikuar pastrimi nuk provon fshirje.

## Hapat teknikë që mbeten për zbatim dhe provë

1. Regjistro kërkesën në një hapësirë me qasje të kufizuar; mos kopjo përmbajtje private në Git, raportin publik PREJ ose screenshot.
2. Verifiko identitetin dhe fushëveprimin, kërkesat e hapura financiare dhe udhëtimet aktive. Mos fshi në mes të një udhëtimi.
3. Përgatit një inventar vetëm për lexim: profil, pajisje/token-a, sesione, të dhëna lokacioni, historik, njoftime, aplikim shoferi, dokumente dhe të dhëna të lidhura.
4. Ndaj të dhënat që duhen fshirë/anonimizuar nga ato që duhet të mbahen me arsye dhe afat të miratuar. Mos modifiko faturat ose regjistrimet financiare historike në mënyrë që të humbet integriteti i tyre.
5. Ekzekuto me kontroll të fushëveprimit, revokim sesionesh dhe shmangie të rrjedhës së re të të dhënave. Testo fillimisht në të dhëna sintetike dhe me dry-run; fshirja reale kërkon kërkesë të verifikuar.
6. Verifiko sistemet kryesore, procesorët dhe rotacionin e backup-eve. Në rikthim nga backup duhet riaplikuar evidenca e fshirjes para hapjes së shërbimit.
7. Konfirmo vetëm pasi kontrollet të tregojnë çfarë është fshirë dhe çfarë mbetet me afat të përcaktuar. Mos e barazo `disabledAt` me fshirje.

## Evidenca e kodit të inspektuar

- `prej-platform/packages/database/prisma/schema.prisma`: User, Device, Session, RiderProfile, DriverProfile, Ride, ReceiptProfile, ReceiptDocument dhe lidhje me kufizime referenciale. Fshirja direkte e User nuk është procedurë e plotë.
- `apps/api/src/driver-location/domain.ts`: konfigurimi i parazgjedhur i mostrave 30 ditë, interval i lejuar 1–90 ditë.
- `apps/api/src/driver-location/ingestion.service.ts`: `purgeExpiredSamples()` ekziston por kërkon planifikim operacional; nuk u pretendua se është aktiv.
- `apps/api/src/auth/config.ts`: OTP development ndalohet në production; mbështeten external dhe twilio-verify. Ofruesi aktiv duhet konfirmuar pa nxjerrë sekrete.
- Android Rider/Driver: Google Maps, Expo Notifications, SecureStore; Driver shton background location dhe task manager. SDK-të duhen audituar kundrejt versionit të nënshkruar.
- Kontrolli i AAB-ve versionCode 2 më 15.11.2026 gjeti Maps SDK 19.1.0, Play Services Location 21.3.0, descriptor-at Firebase Messaging/Installations dhe emrat e resource-ve të konfigurimit FCM. Nuk u nxorën çelësa ose vlera resource-sh. Politika draft SQ/EN/DE tani përfshin edhe IP, diagnostikën dhe identifikuesit teknikë. Dokumentacioni aktual i Maps mbulon versionin e fundit; sjellja e versionit konkret dhe ofruesit aktivë kërkojnë kontroll përfundimtar.

Referenca të inventarit: [Maps SDK disclosure](https://developers.google.com/maps/documentation/android-sdk/play-data-disclosure), [Firebase disclosure](https://firebase.google.com/docs/android/play-data-disclosure), [Expo push](https://docs.expo.dev/push-notifications/faq/). Prania e SDK-së nuk provon dorëzim njoftimesh ose fshirje te procesori.

## Porta e publikimit

Politika mbetet me shenjë të dukshme draft derisa të konfirmohen afatet, procesi i zbatueshëm dhe ofruesit e prodhimit. Testi i faqeve nuk është provë e një fshirjeje reale. Një URL publike nuk e bën automatikisht aplikacionin gati për shqyrtim nga Google Play.

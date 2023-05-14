# TripleDES
Ne kemi krijuar një aplikacion i cili bën enkriptimin dhe dekriptimin e një fajlli përmes algoritmit TripleDES me dy çelësa në modin CBC. Për krijimin e aplikacionit kemi shfrytëzuar gjuhën programuese Python.

Triple DES Algorithm është një algoritëm simetrik i cili e përdor algoritmin DES (Data Encryption Standard) tre herë brenda një blloku të të dhënave. Ky algoritëm bën enkripitmin/dekriptimin duke shfrytëzuar 2 apo 3 çelësa të ndryshëm dhe gjatësia e tyre është 112 respektivisht 156 bit,në rastin tonë 2 çelësa.

Ndërfaqen e përdoruesit e kemi krijuar përmes librarisë tkinter, përdoruesi duhet të shkruaj çelësat, të ngarkojë fajllin pastaj të caktoj veprimin të cilit dëshiron t’a bëjë enkriptim/dekriptim. Në funksionin për enkriptim për të punar në modin CBC është përdour vektori inicializues. Funksioni për dekriptim e bën ekstraktimin e vektorit inicializues dhe e bën dektriptimin me çelësat e dhënë nga përdoruesi.

Libraritë e përdorura:
Tkinter – për krijimin e GUI 
Crypto.Cipher – modul për implementimin e algoritmeve të ndryshme
Os - përzgjedhje të fajllit
Binascii – për konvertim të të dhënave të ndryshme nga binare në heksadecimale dhe anasjelltas

Anëtarët: Arnis Hoxha, Astrit Krasniqi, Besmira Berisha, Blendi Zeqiri

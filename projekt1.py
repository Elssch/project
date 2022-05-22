import hashlib


def pobierz():
    return input('Podaj ścieżke pliku: ')


def czytaj_fasta(sciezka):
    plik = open(sciezka, 'r')

    naglowki = []
    sekwencje = []
    sekwencje_raw = []

    for linijka in plik:
        if linijka.startswith('>'):
            naglowki.append(linijka[1:].strip())
            sekwencje.append('')
            sekwencje_raw.append('')
        else:
            sekwencje[-1] += linijka.strip()
            sekwencje_raw[-1] += linijka

    plik.close()

    return naglowki, sekwencje, sekwencje_raw


def encode(sekwencje):
    encoded = []
    for i in range(len(sekwencje)):
        sekwencja = sekwencje[i].encode('utf-8')
        encoded.append(sekwencja)
    return encoded


def md5(lista):
    checksums = []
    for sekwencja in lista:
        md5 = hashlib.md5(sekwencja).hexdigest()
        checksums.append(md5)
    print(checksums)
    return checksums


def sprawdz_sumy(naglowki, md5, nazwa='raport.txt'):
    zle = []
    error = 0
    good = 0
    for i in range(len(naglowki)):
        if 'MD5=' in naglowki[i]:
            if md5[i] in naglowki[i]:
                good += 1
            else:
                naglowek_suma = naglowki[i], md5[i]
                zle.append(naglowek_suma)
                error += 1
        else:
            print(f'Brak sum kontrolnych w nagłówku.')

    print(f'Prawidłowe sekwencje: {good}')
    print(f'Nieprawidłowe sekwencje: {error}')
    print(f'Raport zawierający niepoprawne sekwencje zapisany w {nazwa}')

    plik = open(nazwa, 'w')
    plik.write('Niepoprawne sumy kontrolne:\n\n')
    for i in range(len(zle)):
        naglowek = zle[i]
        a = naglowek[0].split('MD5=')
        b = a[1].split(';', 1)
        plik.write(f'Nagłówek: {naglowek[0]}\n')
        plik.write(f'Suma kontrolna w nagłówku: {b[0]}\n')
        plik.write(f'Prawidłowa suma kontrolna: {naglowek[1]}\n\n')
    plik.close()


def dopisz_sumy(naglowki, md5):
    zmodyfikowane = []
    for i in range(len(naglowki)):
        if 'MD5=' not in naglowki[i]:
            print('---')
            print(f'Nagłówek: {naglowki[i]}')
            print(f'Suma kontrolna w nagłówku: BRAK')
            print(f'Suma kontrolna dla sekwencji: {md5[i]}')
            naglowek = naglowki[i]
            naglowek += f'; MD5={md5[i]};'
            zmodyfikowane.append(naglowek)
            print(f'Suma kontrolna dopisana do nagłówka')
        else:
            zmodyfikowane.append(naglowki[i])
    return zmodyfikowane


def zapisz_zmodyfikowany(naglowki, sekwencje, sciezka):

    path = sciezka.replace('.fasta', '')
    plik = open(path+'_zmodyfikowane.fasta', 'w')
    for i in range(len(naglowki)):
        plik.write('>' + naglowki[i] + '\n')
        plik.write(sekwencje[i])
    plik.close()


sciezka = pobierz()
sekwencje = czytaj_fasta(sciezka)
kodowanie = encode(sekwencje[1])
hashed = md5(kodowanie)
tryb = input(
    f'Wybierz tryb działania algorytmu.\n0 - tryb weryfikacji\n1 - tryb dopisywania\nTryb: ')
if tryb == '0':
    sprawdz_sumy(sekwencje[0], hashed)
elif tryb == '1':
    modified = dopisz_sumy(sekwencje[0], hashed)
    zapisz_zmodyfikowany(modified, sekwencje[2], sciezka)
else:
    print(f'Nieprawidłowy tryb.')

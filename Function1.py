def bolunen_sayi_bulma(min_sayi, max_sayi, bolen_sayi):
    tam_bolunenler = []
    for sayi in range(min_sayi, max_sayi + 1):
        if sayi % bolen_sayi == 0:
            tam_bolunenler.append(sayi)
    print("Tam bölünenler:", tam_bolunenler)
    return len(tam_bolunenler)

adet = bolunen_sayi_bulma(1, 20, 4)
print("Bölünen sayı adedi:", adet)

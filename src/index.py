from varasto import Varasto


def tulosta_alkutila(mehua, olutta):
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")

    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def mehu_setterit(mehua):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def virheelliset_luonnit():
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    print(Varasto(-100.0))

    print("Varasto(100.0, -50.7)")
    print(Varasto(100.0, -50.7))


def lisays(nimi, varasto, kutsu, maara):
    print(f"{nimi}: {varasto}")
    print(kutsu)
    varasto.lisaa_varastoon(maara)
    print(f"{nimi}: {varasto}")


def otto(nimi, varasto, kutsu, maara):
    print(f"{nimi}: {varasto}")
    print(kutsu)
    saatiin = varasto.ota_varastosta(maara)
    print(f"saatiin {saatiin}")
    print(f"{nimi}: {varasto}")


def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    tulosta_alkutila(mehua, olutta)
    mehu_setterit(mehua)
    virheelliset_luonnit()

    lisays("Olutvarasto", olutta, "olutta.lisaa_varastoon(1000.0)", 1000.0)
    lisays("Mehuvarasto", mehua, "mehua.lisaa_varastoon(-666.0)", -666.0)
    otto("Olutvarasto", olutta, "olutta.ota_varastosta(1000.0)", 1000.0)
    otto("Mehuvarasto", mehua, "mehua.otaVarastosta(-32.9)", -32.9)


if __name__ == "__main__":
    main()

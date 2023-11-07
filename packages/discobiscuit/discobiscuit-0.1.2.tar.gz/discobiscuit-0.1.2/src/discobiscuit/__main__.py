from discobiscuit.clients import MesClient

__VERSION__ = "0.1.2"

def main():
    # Initialise client
    host = "eeel121"
    port = 21022
    mc = MesClient(host=host, port=port)

    sfc = "EE231030357415x"

    product = mc.get_product_by_sfc(sfc=sfc)

    print(product)


if __name__ == "__main__":
    main()

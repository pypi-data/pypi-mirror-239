import httpx

from discobiscuit.exceptions import UnknownSFCException
from discobiscuit.models.mes import Product


class MesClient:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self.base_url = f"http://{host}:{port}/api/"

    def ping(self):
        return "pong"

    def get_product_by_sfc(self, sfc: str) -> Product:
        url = f"{self.base_url}products/get-by-sfc"
        params = {"sfc": sfc}

        product: Product

        with httpx.Client() as client:
            r = client.get(url=url, params=params)

            if r.status_code != 200:
                if r.status_code == 404:
                    raise UnknownSFCException(r.content.decode("utf-8"))
                else:
                    raise Exception(r.content.decode("utf-8"))
            product = Product(**r.json())

        return product

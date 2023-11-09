import os
import logging
from datetime import datetime
import textwrap

import zeep
import base64
import requests
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.


logger = logging.getLogger(__file__)


EU_COUNTRY_CODES = [
    "DE",
    "BE",
    "BG",
    "CZ",
    "DK",
    "DE",
    "EE",
    "IE",
    "EL",
    "FR",
    "GR",
    "HR",
    "IT",
    "CY",
    "LV",
    "LT",
    "LU",
    "HU",
    "MT",
    "NL",
    "AT",
    "PL",
    "PT",
    "RO",
    "SI",
    "SK",
    "FI",
    "SE",
]


class DHL:
    __version__ = "0.1.0"
    __dhl_version__ = "3.4.0"

    def __init__(
        self, auth_user, auth_password, api_user, api_password, is_test=False
    ):
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.api_user = api_user
        self.api_password = api_password
        self.is_test = is_test
        self.client = self._get_client()
        self.version = self._get_version()

    def _get_wsdl_file(self):
        if self.is_test:
            return os.path.join(
                os.path.dirname(__file__),
                f"wsdl/{self.__dhl_version__}/test.wsdl",
            )
        return os.path.join(
            os.path.dirname(__file__),
            f"wsdl/{self.__dhl_version__}/production.wsdl",
        )

    def _get_auth_header(self):
        auth_type = zeep.xsd.Element(
            "{http://dhl.de/webservice/cisbase}Authentification",
            zeep.xsd.ComplexType(
                [
                    zeep.xsd.Element(
                        "{http://dhl.de/webservice/cisbase}user",
                        zeep.xsd.String(),
                    ),
                    zeep.xsd.Element(
                        "{http://dhl.de/webservice/cisbase}signature",
                        zeep.xsd.String(),
                    ),
                ]
            ),
        )
        return auth_type(user=self.api_user, signature=self.api_password)

    def _get_version(self):
        return {"majorRelease": "3", "minorRelease": "1"}

    def _get_client(self):
        session = Session()
        session.auth = HTTPBasicAuth(self.auth_user, self.auth_password)
        client = zeep.Client(
            wsdl=self._get_wsdl_file(),
            transport=zeep.transports.Transport(session=session, timeout=30),
        )
        client.set_default_soapheaders([self._get_auth_header()])
        return client

    def _get_weight_in_kg(self, value, unit="kg"):
        if unit not in ["kg", "g", None]:
            raise ValueError("unit accepts only 'kg' or 'g'")
        if unit == "kg" or unit is None:
            return value
        return value / 1000.0

    def _get_shipper(self, shipper):
        shipper_name = self.client.get_type("ns0:NameType")(
            name1=shipper["name"], name2=shipper.get("name2")
        )
        address = self.client.get_type("ns0:NativeAddressTypeNew")(
            streetName=shipper["street"],
            streetNumber=shipper["street_number"],
            zip=shipper["zip"],
            city=shipper["city"],
            Origin=self.client.get_type("ns0:CountryType")(
                countryISOCode=shipper["country_code"]
            ),
        )
        communication = self.client.get_type("ns0:CommunicationType")(
            phone=shipper["phone"],
            email=shipper["email"],
            contactPerson=shipper["contact_person"],
        )

        return self.client.get_type("ns1:ShipperType")(
            Name=shipper_name, Address=address, Communication=communication
        )

    def _get_receiver(self, receiver, fallback_phone=""):
        phone = receiver.get("phone")
        if phone == "":
            phone = fallback_phone

        dhl_receiver = self.client.get_type("ns1:ReceiverType")(
            name1=receiver["name"],
            Communication=self.client.get_type("ns0:CommunicationType")(
                phone=phone,
                email=receiver.get("email"),
            ),
        )

        if (
            receiver.get("packing_station")
            and receiver.get("packing_station") != "0"
        ):
            dhl_receiver.Packstation = self.client.get_type(
                "ns0:PackStationType"
            )(
                packstationNumber=receiver["street_number"],
                postNumber=receiver["packing_station"],
                zip=receiver["zip"],
                city=receiver["city"],
            )
        elif receiver.get("account_no") and receiver.get("account_no") != "0":
            dhl_receiver.Postfiliale = self.client.get_type(
                "ns0:PostfilialeTypeNoCountry"
            )(
                postfilialNumber=receiver["street_number"],
                postNumber=receiver["account_no"],
                zip=receiver["zip"],
                city=receiver["city"],
            )
        else:
            dhl_receiver.Address = self.client.get_type(
                "ns0:ReceiverNativeAddressType"
            )(
                name2=receiver.get("name2"),
                streetName=receiver["street"],
                streetNumber=receiver["street_number"],
                zip=receiver["zip"],
                city=receiver["city"],
                Origin=self.client.get_type("ns0:CountryType")(
                    countryISOCode=receiver["country_code"]
                ),
                name3=" ".join(
                    [
                        receiver.get("district", "")
                        if receiver.get("district", "")
                        else "",
                        receiver.get("careOfName", "")
                        if receiver.get("careOfName", "")
                        else "",
                        receiver.get("floorNumber", "")
                        if receiver.get("floorNumber", "")
                        else "",
                        receiver.get("roomNumber", "")
                        if receiver.get("roomNumber", "")
                        else "",
                        receiver.get("note", "")
                        if receiver.get("note", "")
                        else "",
                    ]
                ).strip()[:50],
            )

        return dhl_receiver

    def _get_shipment_details(
        self,
        dhl_product,
        dhl_account_number,
        order_id,
        weight_total,
        weight_unit,
        shipment_date=None,
        is_premium=False,
    ):
        if not shipment_date:
            shipment_date = datetime.now()

        shipment_details = self.client.get_type("ns1:ShipmentDetailsTypeType")(
            product=dhl_product,
            accountNumber=dhl_account_number,
            shipmentDate=shipment_date.strftime("%Y-%m-%d"),
            customerReference=order_id,
            ShipmentItem=self.client.get_type("ns1:ShipmentItemTypeType")(
                weightInKG=self._get_weight_in_kg(weight_total, weight_unit)
            ),
        )

        if is_premium:
            shipment_details.Service = self.client.get_type(
                "ns1:ShipmentService"
            )(Premium=1)

        return shipment_details

    def _get_export_document(self, order):
        logger.debug("create export document", order)
        if "customs" not in order:
            logger.error(
                "ERROR: could not find customs information on order", order
            )
            raise Exception(
                "ERROR: could not find customs information on order", order
            )

        export_positions = []
        for position in order["positions"]:
            if "customs" not in position:
                logger.error(
                    "ERROR: could not find customs information on position",
                    position,
                )
                raise Exception(
                    "ERROR: could not find customs information on position",
                    position,
                )
            export_positions.append(
                {
                    "description": textwrap.shorten(
                        position["name"], width=256, placeholder="..."
                    ),
                    "countryCodeOrigin": position["customs"][
                        "country_code_origin"
                    ],
                    "customsTariffNumber": position["customs"][
                        "customs_tariff_number"
                    ],
                    "amount": position["amount"],
                    "customsValue": position["price"],
                    "netWeightInKG": self._get_weight_in_kg(
                        position["weight"], position.get("weight_unit")
                    ),
                }
            )

        return self.client.get_type("ns1:ExportDocumentType")(
            invoiceNumber=order["customs"]["invoice_no"],
            exportType="OTHER",
            exportTypeDescription=order["customs"]["description"],
            placeOfCommital=order["customs"]["place_of_commital"],
            ExportDocPosition=export_positions,
        )

    def get_version(self):
        return self.client.service.getVersion(majorRelease=3, minorRelease=1)

    def get_label(self, shipment_number):
        return self.client.service.getLabel(
            Version=self.version, shipmentNumber=shipment_number
        )

    def get_label_from_url(self, url):
        response = requests.get(url, timeout=8)
        return base64.b64encode(response.content)

    def do_manifest(self, shipmentNumber=None):
        if shipmentNumber:
            return self.client.service.doManifest(
                Version=self.version, shipmentNumber=shipmentNumber
            )
        return self.client.service.doManifest(Version=self.version)

    def get_manifest(self, manifest_date):
        return self.client.service.getManifest(
            Version=self.version, manifestDate=manifest_date
        )

    def create_shipment_order(
        self,
        order_id: str,
        shipper: dict,
        receiver: dict,
        weight_total: float,
        dhl_product: str,
        dhl_account_number: str,
        label_type="URL",
        label_format="910-300-600",
        force_print=False,
        order_to_ship=None,
        shipment_date=None,
        is_premium=False,
        weight_unit="kg",
    ):
        """
        create_shipment_order register a DHL shipment.
        For detailed information check the DHL documenation.

            Parameters:
                order_id (str): Free field to to tag multiple shipment orders individually by client
                shipper (dict): Shipper address. Use schemas.Address to get the needed fields
                receiver (dict): Receiver address. Use schemas.Address to get the needed fields
                weight_total (float): Total weight of the shipment (incl. packaging)
                dhl_product (str): Determines the DHL Paket product to be ordered. Check DHL documentation for the right product
                dhl_account_number (str): DHL account number (14 digits)
                label_type (str): Dial to determine label ouput format. Must be either 'URL' or 'B64'
                label_format (str): In this optional section you can define the label formats. Check DHL documentation for the right formats
                force_print (bool): If set to true (=1), the label will be only be printable, if the receiver address is valid.
                order_to_ship (dict): Order detail information. Use schemas.ShipmentOrder to get the needed fields
                shipment_date (datetime): Date of shipment should be close to current date (default) and must not be in the past. Will be convert to string shipment_date.strftime("%Y-%m-%d")
                is_premium (bool): Premium for fast and safe delivery of international shipments. If not set Service Premium will not send to DHL
                weight_unit (str): Used unit for weight_total. Defauklt "kg". Possible values ["g", "kg"]

            Returns:
                CreateShipmentOrderResponse (dict): DHL response CreateShipmentOrderResponse
        """  # noqa

        try:
            shipment_order_type = self.client.get_type("ns1:ShipmentOrderType")
            shipment = {
                "ShipmentDetails": self._get_shipment_details(
                    dhl_product,
                    dhl_account_number,
                    order_id,
                    weight_total,
                    weight_unit,
                    shipment_date,
                    is_premium,
                ),
                "Shipper": self._get_shipper(shipper),
                "Receiver": self._get_receiver(receiver, shipper["phone"]),
            }

            # create export documents if receiver country is not in the EU
            if receiver["country_code"] not in EU_COUNTRY_CODES:
                logger.debug(
                    "create export document for not EU",
                    receiver["country_code"],
                )
                shipment["ExportDocument"] = self._get_export_document(
                    order_to_ship
                )

            shipment_order = shipment_order_type(
                sequenceNumber=order_id,
                Shipment=shipment,
                PrintOnlyIfCodeable=force_print,
            )

            return self.client.service.createShipmentOrder(
                Version=self.version,
                ShipmentOrder=shipment_order,
                labelResponseType=label_type,
                labelFormat=label_format,
            )
        except Exception as ex:
            print("ERROR:", ex)
            logger.exception(f"could not create shipment; {ex}")
            raise Exception("could not create shipment", ex)

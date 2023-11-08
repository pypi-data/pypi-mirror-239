# Python eVatR Client

A Python client for simple and qualified VAT-number validations.

This is a Python port of the Typescript client that can be found here: [eVatR Typescript Client](https://github.com/qqilihq/evatr/tree/master)

You can find detailed information on the underlying API here (German): https://evatr.bff-online.de/eVatR/xmlrpc/

Users need to provide a registered German VAT-number (Umsatzsteuer-Identifikationsnummern) to use this client.

This tool is not endorsed by the "Bundeszentralamt für Steuern".

## Usage

```python
from evatr_client import EvatrClient, ISimpleParams, IQualifiedParams
from dataclass_wizard import asdict

client = EvatrClient()

simpleParams: ISimpleParams = ISimpleParams(
    include_raw_xml=False,
    own_vat_number="DE129273398",
    validate_vat_number="CZ00177041",
)

simple_result = client.check_simple(simpleParams)
print(asdict(simple_result))

qualifiedParams: IQualifiedParams = IQualifiedParams(
    include_raw_xml=False,
    own_vat_number="DE129273398",
    validate_vat_number="CZ00177041",
    company_name="SKODA AUTO a.s.",
    city="Mlada Boleslav",
    zip="293 01",
    street="tr. Vaclava Klementa 869",
)

qualified_result = client.check_qualified(qualifiedParams)
print(asdict(qualified_result))
```

Example result:

`ISimpleResult`
```json
{
    "valid": True,
    "date": "07.11.2023",
    "time": "11:40:23",
    "errorCode": "200",
    "errorDescription": "Die angefragte USt-IdNr. ist gültig.",
    "ownVatNumber": "DE129273398",
    "validatedVatNumber": "CZ00177041",
    "validFrom": None,
    "validUntil": None,
    "rawXml": None
}
```

`IQualifiedResult`

```json
{
    "valid": True, 
    "date": "07.11.2023", 
    "time": "11:40:37", 
    "errorCode": "200", 
    "errorDescription": "Die angefragte USt-IdNr. ist gültig.", 
    "ownVatNumber": "DE129273398", 
    "validatedVatNumber": "CZ00177041", 
    "validFrom": None, 
    "validUntil": None, 
    "rawXml": None, 
    "companyName": "SKODA AUTO a.s.", 
    "city": "Mlada Boleslav",
    "zip": "293 01", 
    "street": "tr. Vaclava Klementa 869", 
    "resultName": "A", 
    "resultCity": "A", 
    "resultZip": "A", 
    "resultStreet": "A", 
    "resultNameDescription": "stimmt überein",
    "resultCityDescription": "stimmt überein", 
    "resultZipDescription": "stimmt überein", 
    "resultStreetDescription": "stimmt überein"
}

```

## Installation

The source code is currently hosted on GitHub at: https://github.com/CeeDiii/evatr-client

The Python package is available at Python Package Index (PyPI)

```
$ pip install evatr-client
```

## Development

Install dependencies from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```

You can scrape the error codes with the script `scripts/scrape_status_codes.py`. The script has to be executed from the project root directory:

```shell
python scripts/scrape_status_codes.py
```

## Testing

To get the actual test results, execute the following command from the root project directory:

```shell
python -m unittest
```

## Contributing

Feel free to open issues and pull requests in this repo.

## License MIT

Copyright © 2023 CeeDiii

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

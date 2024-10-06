from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mapping country names to their corresponding currency codes
country_to_currency = {
    "india": "INR",
    "united states": "USD",
    "united arab emirates": "AED",
    "afghanistan": "AFN",
    "albania": "ALL",
    "armenia": "AMD",
    "netherlands antilles": "ANG",
    "angola": "AOA",
    "argentina": "ARS",
    "australia": "AUD",
    "aruba": "AWG",
    "azerbaijan": "AZN",
    "bosnia and herzegovina": "BAM",
    "barbados": "BBD",
    "bangladesh": "BDT",
    "bulgaria": "BGN",
    "bahrain": "BHD",
    "burundi": "BIF",
    "bermuda": "BMD",
    "brunei": "BND",
    "bolivia": "BOB",
    "brazil": "BRL",
    "bahamas": "BSD",
    "bhutan": "BTN",
    "botswana": "BWP",
    "belarus": "BYN",
    "belize": "BZD",
    "canada": "CAD",
    "congo": "CDF",
    "switzerland": "CHF",
    "chile": "CLP",
    "china": "CNY",
    "colombia": "COP",
    "costa rica": "CRC",
    "cuba": "CUP",
    "cape verde": "CVE",
    "czech republic": "CZK",
    "djibouti": "DJF",
    "denmark": "DKK",
    "dominican republic": "DOP",
    "algeria": "DZD",
    "egypt": "EGP",
    "eritrea": "ERN",
    "ethiopia": "ETB",
    "euro": "EUR",
    "fiji": "FJD",
    "falkland islands": "FKP",
    "united kingdom": "GBP",
    "georgia": "GEL",
    "ghana": "GHS",
    "gibraltar": "GIP",
    "gambia": "GMD",
    "guinea": "GNF",
    "guatemala": "GTQ",
    "guyana": "GYD",
    "hong kong": "HKD",
    "honduras": "HNL",
    "croatia": "HRK",
    "haiti": "HTG",
    "hungary": "HUF",
    "indonesia": "IDR",
    "israel": "ILS",
    "india": "INR",
    "iraq": "IQD",
    "iran": "IRR",
    "iceland": "ISK",
    "jamaica": "JMD",
    "jordan": "JOD",
    "japan": "JPY",
    "kenya": "KES",
    "kyrgyzstan": "KGS",
    "cambodia": "KHR",
    "kiribati": "KID",
    "comoros": "KMF",
    "south korea": "KRW",
    "kuwait": "KWD",
    "kazakhstan": "KZT",
    "laos": "LAK",
    "lebanon": "LBP",
    "sri lanka": "LKR",
    "liberia": "LRD",
    "lesotho": "LSL",
    "libya": "LYD",
    "morocco": "MAD",
    "moldova": "MDL",
    "madagascar": "MGA",
    "north macedonia": "MKD",
    "myanmar": "MMK",
    "mongolia": "MNT",
    "macau": "MOP",
    "mauritania": "MRU",
    "mauritius": "MUR",
    "maldives": "MVR",
    "malawi": "MWK",
    "mexico": "MXN",
    "malaysia": "MYR",
    "mozambique": "MZN",
    "namibia": "NAD",
    "nigeria": "NGN",
    "nicaragua": "NIO",
    "norway": "NOK",
    "nepal": "NPR",
    "new zealand": "NZD",
    "oman": "OMR",
    "panama": "PAB",
    "peru": "PEN",
    "papua new guinea": "PGK",
    "philippines": "PHP",
    "pakistan": "PKR",
    "poland": "PLN",
    "paraguay": "PYG",
    "qatar": "QAR",
    "romania": "RON",
    "serbia": "RSD",
    "russia": "RUB",
    "rwanda": "RWF",
    "saudi arabia": "SAR",
    "solomon islands": "SBD",
    "seychelles": "SCR",
    "sudan": "SDG",
    "sweden": "SEK",
    "singapore": "SGD",
    "sierra leone": "SLE",
    "somalia": "SOS",
    "suriname": "SRD",
    "south sudan": "SSP",
    "sao tome and principe": "STN",
    "syria": "SYP",
    "swaziland": "SZL",
    "thailand": "THB",
    "tajikistan": "TJS",
    "turkmenistan": "TMT",
    "tunisia": "TND",
    "tonga": "TOP",
    "turkey": "TRY",
    "trinidad and tobago": "TTD",
    "taiwan": "TWD",
    "tanzania": "TZS",
    "ukraine": "UAH",
    "uganda": "UGX",
    "uruguay": "UYU",
    "uzbekistan": "UZS",
    "venezuela": "VES",
    "vietnam": "VND",
    "vanuatu": "VUV",
    "samoa": "WST",
    "central african republic": "XAF",
    "east caribbean": "XCD",
    "cfa franc": "XOF",
    "french polynesia": "XPF",
    "yemen": "YER",
    "south africa": "ZAR",
    "zambia": "ZMW",
    "zimbabwe": "ZWL",
    # For the upper
    "INDIA": "INR",
    "UNITED STATES": "USD",
    "UNITED ARAB EMIRATES": "AED",
    "AFGHANISTAN": "AFN",
    "ALBANIA": "ALL",
    "ARMENIA": "AMD",
    "NETHERLANDS ANTILLES": "ANG",
    "ANGOLA": "AOA",
    "ARGENTINA": "ARS",
    "AUSTRALIA": "AUD",
    "ARUBA": "AWG",
    "AZERBAIJAN": "AZN",
    "BOSNIA AND HERZEGOVINA": "BAM",
    "BARBADOS": "BBD",
    "BANGLADESH": "BDT",
    "BULGARIA": "BGN",
    "BAHRAIN": "BHD",
    "BURUNDI": "BIF",
    "BERMUDA": "BMD",
    "BRUNEI": "BND",
    "BOLIVIA": "BOB",
    "BRAZIL": "BRL",
    "BAHAMAS": "BSD",
    "BHUTAN": "BTN",
    "BOTSWANA": "BWP",
    "BELARUS": "BYN",
    "BELIZE": "BZD",
    "CANADA": "CAD",
    "CONGO": "CDF",
    "SWITZERLAND": "CHF",
    "CHILE": "CLP",
    "CHINA": "CNY",
    "COLOMBIA": "COP",
    "COSTA RICA": "CRC",
    "CUBA": "CUP",
    "CAPE VERDE": "CVE",
    "CZECH REPUBLIC": "CZK",
    "DJIBOUTI": "DJF",
    "DENMARK": "DKK",
    "DOMINICAN REPUBLIC": "DOP",
    "ALGERIA": "DZD",
    "EGYPT": "EGP",
    "ERITREA": "ERN",
    "ETHIOPIA": "ETB",
    "EURO": "EUR",
    "FIJI": "FJD",
    "FALKLAND ISLANDS": "FKP",
    "UNITED KINGDOM": "GBP",
    "GEORGIA": "GEL",
    "GHANA": "GHS",
    "GIBRALTAR": "GIP",
    "GAMBIA": "GMD",
    "GUINEA": "GNF",
    "GUATEMALA": "GTQ",
    "GUYANA": "GYD",
    "HONG KONG": "HKD",
    "HONDURAS": "HNL",
    "CROATIA": "HRK",
    "HAITI": "HTG",
    "HUNGARY": "HUF",
    "INDONESIA": "IDR",
    "ISRAEL": "ILS",
    "IRAQ": "IQD",
    "IRAN": "IRR",
    "ICELAND": "ISK",
    "JAMAICA": "JMD",
    "JORDAN": "JOD",
    "JAPAN": "JPY",
    "KENYA": "KES",
    "KYRGYZSTAN": "KGS",
    "CAMBODIA": "KHR",
    "KIRIBATI": "KID",
    "COMOROS": "KMF",
    "SOUTH KOREA": "KRW",
    "KUWAIT": "KWD",
    "KAZAKHSTAN": "KZT",
    "LAOS": "LAK",
    "LEBANON": "LBP",
    "SRI LANKA": "LKR",
    "LIBERIA": "LRD",
    "LESOTHO": "LSL",
    "LIBYA": "LYD",
    "MOROCCO": "MAD",
    "MOLDOVA": "MDL",
    "MADAGASCAR": "MGA",
    "NORTH MACEDONIA": "MKD",
    "MYANMAR": "MMK",
    "MONGOLIA": "MNT",
    "MACAU": "MOP",
    "MAURITANIA": "MRU",
    "MAURITIUS": "MUR",
    "MALDIVES": "MVR",
    "MALAWI": "MWK",
    "MEXICO": "MXN",
    "MALAYSIA": "MYR",
    "MOZAMBIQUE": "MZN",
    "NAMIBIA": "NAD",
    "NIGERIA": "NGN",
    "NICARAGUA": "NIO",
    "NORWAY": "NOK",
    "NEPAL": "NPR",
    "NEW ZEALAND": "NZD",
    "OMAN": "OMR",
    "PANAMA": "PAB",
    "PERU": "PEN",
    "PAPUA NEW GUINEA": "PGK",
    "PHILIPPINES": "PHP",
    "PAKISTAN": "PKR",
    "POLAND": "PLN",
    "PARAGUAY": "PYG",
    "QATAR": "QAR",
    "ROMANIA": "RON",
    "SERBIA": "RSD",
    "RUSSIA": "RUB",
    "RWANDA": "RWF",
    "SAUDI ARABIA": "SAR",
    "SOLOMON ISLANDS": "SBD",
    "SEYCHELLES": "SCR",
    "SUDAN": "SDG",
    "SWEDEN": "SEK",
    "SINGAPORE": "SGD",
    "SIERRA LEONE": "SLE",
    "SOMALIA": "SOS",
    "SURINAME": "SRD",
    "SOUTH SUDAN": "SSP",
    "SAO TOME AND PRINCIPE": "STN",
    "SYRIA": "SYP",
    "SWAZILAND": "SZL",
    "THAILAND": "THB",
    "TAJIKISTAN": "TJS",
    "TURKMENISTAN": "TMT",
    "TUNISIA": "TND",
    "TONGA": "TOP",
    "TURKEY": "TRY",
    "TRINIDAD AND TOBAGO": "TTD",
    "TAIWAN": "TWD",
    "TANZANIA": "TZS",
    "UKRAINE": "UAH",
    "UGANDA": "UGX",
    "URUGUAY": "UYU",
    "UZBEKISTAN": "UZS",
    "VENEZUELA": "VES",
    "VIETNAM": "VND",
    "VANUATU": "VUV",
    "SAMOA": "WST",
    "CENTRAL AFRICAN REPUBLIC": "XAF",
    "EAST CARIBBEAN": "XCD",
    "CFA FRANC": "XOF",
    "FRENCH POLYNESIA": "XPF",
    "YEMEN": "YER",
    "SOUTH AFRICA": "ZAR",
    "ZAMBIA": "ZMW",
    "ZIMBABWE": "ZWL"
}

# Single endpoint for both currency conversion and fetching rates
@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_json()
    print("Received Data: ", data)  # Debugging line to check incoming data

    # Determine the intent from the incoming data
    intent_name = data['queryResult']['intent']['displayName']

    if intent_name == 'rate':  # If intent is to get the conversion rate
        return get_rates(data)
    elif intent_name == 'currency-conveter':  # If intent is to perform currency conversion
        return currency_conversion(data)
    else:
        return jsonify({'fulfillmentText': 'Unknown intent.'}), 400


def currency_conversion(data):
    try:
        # Ensure the path to parameters is correct as per Dialogflow JSON structure
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_country = data['queryResult']['parameters']['currency-name'][0]  # assuming a list of target countries

    except KeyError as e:
        return jsonify({'fulfillmentText': f'Missing parameter: {str(e)}'}), 400

    print(f"Source Currency: {source_currency}, Amount: {amount}, Target Currency: {target_country}")

    # Fetch the conversion rate
    conversion_rate = fetch_conversion(source_currency, target_country)

    if conversion_rate == 'Not available':
        return jsonify({'fulfillmentText': 'Conversion rate not available.'}), 400

    final_amount = amount * conversion_rate
    print(f"Final Amount: {final_amount}")

    response = {
        'fulfillmentText': f"{amount} {source_currency} is {final_amount:.2f} {target_country}."
    }
    return jsonify(response)


def get_rates(data):
    try:
        base_currency = data['queryResult']['parameters']['base_country'].upper()
        target_country = data['queryResult']['parameters']['target_country'].lower()
        
        # Convert target country to currency code
        target_currency = country_to_currency.get(target_country, None)
        if not target_currency:
            return jsonify({'fulfillmentText': f'Currency for {target_country} not found.'}), 400

    except KeyError as e:
        return jsonify({'fulfillmentText': f'Missing parameter: {str(e)}'}), 400

    print(f"Base Currency: {base_currency}, Target Currency: {target_currency}")

    # Fetch rate for specific target currency
    rate = fetch_conversion(base_currency, target_currency)
    if rate == 'Not available':
        return jsonify({'fulfillmentText': 'Conversion rate not available.'}), 400
    
    response = {
        'fulfillmentText': f"1 {base_currency} = {rate:.4f} {target_currency}."
    }

    return jsonify(response)


def fetch_conversion(source, target):
    # API call to get the conversion rate for the specific currencies
    url = f'https://api.currencyapi.com/v3/latest?apikey=cur_live_jYr62acaSyV9WJRfbSbTTzt3MX24V774WfQEvMos&base_currency={source}&currencies={target}'
    
    response = requests.get(url)
    response_data = response.json()
    
    # Check if the response is valid
    if 'data' in response_data and target in response_data['data']:
        conversion_rate = response_data['data'][target].get('value', 'Not available')
    else:
        conversion_rate = 'Not available'

    print(f"Conversion Rate: {conversion_rate}")
    return conversion_rate


if __name__ == "__main__":
    app.run(debug=True)

import requests
from urllib.parse import unquote, urlparse
from parse import parse
from loguru import logger
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.location import Location
from app.models.address import GoogleMapsURL, Address


def expand_maps_url(short_url: str) -> str:
    """Expand google maps url

    Args:
        short_url (str): Short URL from google maps. Example: https://maps.app.goo.gl/uTcg6FGLdhDQQQe88

    Raises:
        ValueError: If the URL cannot be expanded due to a request error.

    Returns:
        str: The expanded URL after following redirects. Example: https://www.google.com/maps/place/Nama+Tempat/@lat,lng,zoom/data=...
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.head(short_url, headers=headers, allow_redirects=True)
    except requests.RequestException as e:
        logger.error(f"Error while expanding URL: {e}")
        raise ValueError(f"Failed to expand URL: {e}")

    return response.url


def extract_place_info(maps_url: str) -> GoogleMapsURL:
    """Extract place information from a Google Maps URL.

    Args:
        maps_url (str): The expanded Google Maps URL. Example: https://www.google.com/maps/place/Nama+Tempat/@lat,lng,zoom/data=...
    Returns:
        dict: A dictionary containing the place name, latitude, longitude, and zoom level.
    """
    decoded_url = unquote(maps_url)
    path = urlparse(decoded_url).path

    pattern = "/maps/place/{place_name}/@{lat:f},{lng:f},{zoom}m/data={data_payload}"
    result = parse(pattern, path)

    if result:
        nama_tempat = result["place_name"].replace("+", " ")

        return GoogleMapsURL(
            url=maps_url,
            name=nama_tempat,
            latitude=result["lat"],
            longitude=result["lng"],
        )
    else:
        logger.warning(
            "URL format tidak dikenali, tidak dapat mengekstrak informasi tempat."
        )
        raise ValueError(
            "URL not in expected format, cannot extract place information."
        )
        
async def get_address_from_coordinates(latitude: float, longitude: float) -> Address:
    """Get address from latitude and longitude using geopy.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        str: The address corresponding to the given coordinates, or an error message if the geocoding fails.
    """
    geolocator = Nominatim(user_agent="vantage_ai_geocoder")
    reverse_geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    try:
        location: Location = reverse_geocode((latitude, longitude))
        if location is None:
            raise ValueError("No address found for the given coordinates.")
        print(location.raw)
        raw_address = location.raw.get("address", {})
        return Address(
            jalan=location.raw.get("display_name", ""),
            desa_kelurahan=location.raw.get("suburb", ""),
            kecamatan=location.raw.get("city_district", ""),
            kota=location.raw.get("city", ""),
            provinsi=location.raw.get("state", ""),
            kode_pos=location.raw.get("postcode", ""),
        )
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f"Geocoding error: {e}")
        raise ValueError(f"Geocoding failed: {e}")


# short_link = "https://maps.app.goo.gl/uTcg6FGLdhDQQQe88"
# long_link = expand_maps_url(short_link)


# # 1. Bersihkan URL dari encoding (seperti %2F menjadi /)
# decoded_url = unquote(short_link)

# # 2. Ambil bagian path-nya saja: /maps/place/Nama+Tempat/@lat,lng,zoom/data=...
# path = urlparse(decoded_url).path

# # 3. Ekstrak menggunakan library `parse` tanpa regex sama sekali
# pattern = "/maps/place/{place_name}/@{lat:f},{lng:f},{zoom}m/data={data_payload}"
# result = parse(pattern, path)

# if result:
#     # Mengganti tanda '+' dengan spasi untuk nama tempat
#     nama_tempat = result["place_name"].replace("+", " ")

#     print(f"Nama Tempat : {nama_tempat}")
#     print(f"Latitude    : {result['lat']}")
#     print(f"Longitude   : {result['lng']}")
#     print(f"Zoom Level  : {result['zoom']}")

if __name__ == "__main__":
    import asyncio
    # Contoh penggunaan
    short_link = "https://maps.app.goo.gl/uTcg6FGLdhDQQQe88"
    long_link = expand_maps_url(short_link)
    place_info = extract_place_info(long_link)
    print(place_info)
    alamat = asyncio.run(get_address_from_coordinates(place_info.latitude, place_info.longitude))
    print(alamat)
from django.core.management.base import BaseCommand, CommandError
from sprigs.models import Product
import requests

# Sample of Grocery Merchants
MERCHANTS = ['Loblaw', 'Walmart', 'Metro', 'Costco', 'Freshco', 'NoFrills', 'FoodBasics', 'Independent', 'Zehrs','ShoppersDrugMart', 'ValuMart', 'Sobeys', 'IGA']
# Central Postal Code in Ottawa
LOCATION = ['K1P1J1']

# Initialize variables
product_list = []
classification_list = []
global data

def metadata_request(location, merchant):
    req = requests.get('https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code='+ location + '&radius=50km' + '&q=' + merchant)
    res = req.json()['items']
    return res

def description_request(flyer_item_id):
    req = requests.get('https://backflipp.wishabi.com/flipp/items/'+ str(flyer_item_id))
    res = req.json()['item']['description']
    if res is not None:
        return res.upper()
    else:
        return ""

class Command(BaseCommand):
    help = 'Populates DB with product data'

    def handle(self, *args, **options):
        # retrieve flyer data
        for loc in LOCATION:
            for mer in MERCHANTS:
                data = metadata_request(loc,mer)

                # loop over data, format, and extract values of interest
                for i in data:
                    # if item falls into a poultry category, run additional request to
                    # retrieve description information (specifics on product ie. boneless, skinless etc).
                    pname = i['name'].upper()
                    if 'CHICKEN' in pname or 'TURKEY' in pname or 'DUCK' in pname:
                        full_name = pname + " " + description_request(i['flyer_item_id'])
                    else:
                        full_name = pname
                    
                    # Create product objects, and persist to database
                    Product.objects.bulk_create([
                        Product(
                        flyer_id = i['flyer_item_id'],
                        product_name = full_name,
                        merchant = i['merchant_name'].upper(),
                        sale_price = i['current_price'],
                        price_units = i['post_price_text'],
                        start_date = i['valid_from'],
                        end_date = i['valid_to'],
                    )])
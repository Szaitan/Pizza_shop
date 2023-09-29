import os
import stripe


stripe.api_key = os.environ.get("stripe_api_key")
# x = stripe.Product.list()
# print(x["data"][0])
# print(x["data"][0]["features"][0]["name"])


# for price in x["data"]:
#     list_with_prices.append(stripe.Price.retrieve(price.default_price))
#
#


# y = stripe.Price.retrieve(x["data"][0].default_price)
# print(y)


x = stripe.Price.search(query="lookup_key:'SweetPeperoni_Medium_Thin_No_Chesse'",)
# SweetPeperoni_Medium_Thin_No_Chesse
print(x)
print(x["data"][0]["unit_amount"])
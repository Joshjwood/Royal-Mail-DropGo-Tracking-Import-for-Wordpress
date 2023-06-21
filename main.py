from classes import *

bot = RoyalMailTrackingImporter()

bot.GetTrackingIDs()
#input("Check the listed postcodes for issues and press Enter to proceed:\n")
bot.InputTrackingIDs()

#
# with open("rm_post_dict.json", "r") as postcodes:
#     data = json.load(postcodes)
#
#     for i in data:
#         print(data[i])
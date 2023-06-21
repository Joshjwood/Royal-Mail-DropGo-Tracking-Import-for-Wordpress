# Royal-Mail-DropGo-Tracking-Import-for-Wordpress

This is a custom selenium script that pulls tracking information from Royal Mail's Drop and Go Service and enters it into a Wordpress+Woocommerce website. It does so by capturing the addresses in a dictionary, and then comparing the postcodes in Woocommerce to that dictionary.

This should work for anyone but for one element, we use a custom order status from a free plugin that we've called 'Packed'. You will need to either create this order status or change the word packed in the URL in the classes.py to 'processing'. 

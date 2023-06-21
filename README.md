# Royal-Mail-DropGo-Tracking-Import-for-Wordpress

This is a custom selenium script that pulls tracking information from Royal Mail's Drop and Go Service and enters it into a Wordpress+Woocommerce website. It does so by capturing the addresses in a dictionary, and then comparing the postcodes in Woocommerce to that dictionary.

This should work for anyone but for several elements:
- It assumes you're using the plugin "Advanced Shipment Tracking for WooCommerce"
- On the 'Orders' page you must go to Screen Options and tick to show the 'Shipment Tracking' button, if it is not shown by default
- We use a custom order status from a free plugin that we've called 'Packed' as part of our workflow ("Custom Order Status Manager for WooCommerce"). You will need to either create this order status or change the word packed in the URL in the classes.py to 'processing'. 

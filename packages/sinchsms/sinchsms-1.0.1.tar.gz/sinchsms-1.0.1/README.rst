Python module for sending sms with Sinch
----------------------------------------

Installation
~~~~~~~~~~~~

.. code:: bash

    pip install sinchsms

Usage example
~~~~~~~~~~~~~

.. code:: python

    import time
    from sinchsms import SinchSMS

    number = '+46000000001'
    message = 'Hello from Sinch!'

    client = SinchSMS(your_app_key, your_app_secret)

    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['MessageId']

    response = client.check_status(message_id)
    while response['Status'] != 'Successful':
        print(response['Status'])
        time.sleep(1)
        response = client.check_status(message_id)
    print(response['Status'])

.. note::

    You will need a Sinch account for getting your application key and secret. Visit www.sinch.com to get started.

Using as command line script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    ./sinchsms.py
    usage: sinchsms.py <application key> <application secret> send <number> <message> <from_number>
           sinchsms.py <application key> <application secret> status <message_id>


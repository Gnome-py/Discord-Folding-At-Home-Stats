async def ensure_webhook(channel, name="Folding-Webhook"):
    webhooks = await channel.webhooks()
    if len(webhooks) == 0:  webhook = await channel.create_webhook(name)
    else:   webhook = webhooks[0]

    return webhook

def get_value(dictionary, *nested_values, default_value = None):
    try:
        for value in nested_values:
            dictionary = dictionary[value]
    except (TypeError, AttributeError, KeyError):
        return default_value

    return dictionary

def remove_chars(remove_from, *chars):
    input_string = str(remove_from)
    for char in chars:  input_string = input_string.replace(char, "")

    return input_string

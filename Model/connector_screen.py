from Model.base_model import BaseScreenModel
import os


class ConnectorScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.command_screen.CommandScreen.CommandScreenView` class.
    """
    #

    speed_dial_data = {
        'Add Connector': 'connection',
    }

    connectors_list = [
        ('tripletex', 'https://github.com/sesam-io/tripletex-connector'),
        ('hubspot', 'https://github.com/sesam-io/hubspot-connector'),
        ('superoffice', 'https://github.com/sesam-io/superoffice-connector'),
        ('powerofficego', 'https://github.com/sesam-io/powerofficego-connector'),
        ('wave', 'https://github.com/sesam-io/wave-connector'),
        ('crmoffice', 'https://github.com/sesam-io/crmoffice-connector'),
        ('unieconomy', 'https://github.com/sesam-io/unieconomy-connector'),
        ('freshteam', 'https://github.com/sesam-io/freshteam-connector'),
        ('bigquery', 'https://github.com/sesam-io/bigquery-connector'),
        ('opensesam', 'https://github.com/sesam-io/opensesam-connector'),
        ('zoho', 'https://github.com/sesam-io/zoho-connector'),
        ('wikidata', 'https://github.com/sesam-io/wikidata-connector'),
        ('dbpedia', 'https://github.com/sesam-io/dbpedia-connector'),
        ('difi', 'https://github.com/sesam-io/difi-connector'),
        ('nace', 'https://github.com/sesam-io/nace-connector'),
        ('twelvedata', 'https://github.com/sesam-io/twelvedata-connector')
    ]

    downloaded_connectors = []
    for connector in connectors_list:
        if os.path.exists(os.path.join('core', f"{connector[0]}-connector")):
            downloaded_connectors.append(connector[0])
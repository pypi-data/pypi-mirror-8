Service
=======

User Service CLI Python

Installation:
-------------

Install with pip into virtualenv or globally:

	pip install quantgo-service-cli

To enable autocomplete feature install cli tool and type in console:

	complete -C service_complete service

API client available:

    from qgservice import QuantGoService

    qg = QuantGoService()

    help(QuantGoService)
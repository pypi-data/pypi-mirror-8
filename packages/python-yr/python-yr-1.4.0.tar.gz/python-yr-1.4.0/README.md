python-yr
=================
Library for the norwegian wheather service yr.no in python.

#### Usage
```python
from yr.libyr import Yr

weather = Yr(location_name='Norge/Telemark/Skien/Skien')
now = weather.now(as_json=True)

print(now)
```

#### This returns
```json
{
    "@from": "2014-06-04T08:00:00", 
    "@to": "2014-06-04T12:00:00", 
    "@period": "1", 
    "symbol": {
        "@number": "3", 
        "@numberEx": "3", 
        "@name": "Partly cloudy", 
        "@var": "03d"
    }, 
    "precipitation": {
        "@value": "0", 
        "@minvalue": "0", 
        "@maxvalue": "0.1"
    }, 
    "windDirection": {
        "@deg": "159.4", 
        "@code": "SSE", 
        "@name": "South-southeast"
    }, 
    "windSpeed": {
        "@mps": "1.3", 
        "@name": "Light air"
    }, 
    "temperature": {
        "@unit": "celsius", 
        "@value": "13"
    }, 
    "pressure": {
        "@unit": "hPa", 
        "@value": "1012.1"
    }
}
```

For more usage examples visit folder [examples](/yr/examples) or project [wiki](https://github.com/wckd/python-yr/wiki)

Pull requests are very welcomed! :-)

#### Changelog

1.4.0 (2014 Sep 12)

* Add support for yr.no api service ~> thanks to lucadelu
* Add hourly forecast ~> thanks to antorweep1987

1.3.2 (2014 Jul 11)

* Improved exception-handling, thanks @mbambas!

1.3.1.1 (2014 Jul 10)

* Bugfix: pypi/pip installer in 'setup.py'

1.3.1 (2014 Jul 10)

* Bugfix: caching mechanism in 'is_fresh' function ~> thanks to antorweep
* Improve examples

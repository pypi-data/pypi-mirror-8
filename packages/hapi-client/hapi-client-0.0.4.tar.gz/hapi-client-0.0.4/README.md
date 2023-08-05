
# HAPI Command Line

## Quickstart

1. Clone or install the library
1.1. git clone git@github.com:hyperdns/hyperdns-client-python3
1.2. pip install git+git://github.com/hyperdns/hyperdns-client-python3@initial-import
2. Run ```hapi``` or ```hapi config```
3. Be HAPI


## Configuration File

```
(.python)hapi-client-python3 : cat ~/.hapi
{
    "baseUrl": "http://localhost:5000/my",
    "fname": "/Users/dnsmanager/.hapi",
    "jwt": "xxxxxxxxx"
}
```


# Developing

### Scripts

#### hapi
This is the python3 script.
```
(.python)hapi-client-python3 : hapi
Usage:
    hapi help         [<command> [--examples] ] [--nobold]
    hapi config
    hapi ping         [--config=<path>]
    hapi login        [--config=<path>]
    hapi upload       [--config=<path>] <zonefile>
    hapi download     [--config=<path>] <fqdn>
    hapi zones        [--config=<path>] [<fqdn> [--create]]
    hapi vendor       [--config=<path>] [--available] [[<vendortag> [--remove] [--setup=<path>]]]
    hapi account      [--config=<path>] [--scan | --prune | --validate | --task=<task>]
```

#### devmap
This will contact the dev server and dump out the API
```
(.python)hapi-client-python3 : devmap
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2470  100  2470    0     0   689k      0 --:--:-- --:--:-- --:--:--  804k
        "uri": "/<path:filename>"
        "uri": "/angular/directives.js"
        "uri": "/auth/key"
        "uri": "/client/model/<string:flavor>"
        "uri": "/my"
        "uri": "/my/admins/<string:arg_1>"
        "uri": "/my/vendors/<string:arg_1>"
        "uri": "/my/vendors/<string:arg_1>/history/<string:arg_2>"
        "uri": "/my/zones/<string:arg_1>"
        "uri": "/my/zones/<string:arg_1>/history/<string:arg_2>"
        "uri": "/my/zones/<string:arg_1>/resources/<string:arg_2>"
        "uri": "/site-map"
        "uri": "/system"
        "uri": "/system/accounts/<string:arg_1>"
        "uri": "/system/accounts/<string:arg_1>/admins/<string:arg_2>"
        "uri": "/system/accounts/<string:arg_1>/vendors/<string:arg_2>"
        "uri": "/system/accounts/<string:arg_1>/vendors/<string:arg_2>/history/<string:arg_3>"
        "uri": "/system/accounts/<string:arg_1>/zones/<string:arg_2>"
        "uri": "/system/accounts/<string:arg_1>/zones/<string:arg_2>/history/<string:arg_3>"
        "uri": "/system/accounts/<string:arg_1>/zones/<string:arg_2>/resources/<string:arg_3>"
        "uri": "/system/vendordefs/<string:arg_1>"
```

#### . devup
This will set up the development python virtual environment.  Note that it must be run in the current shell as ". devup" and not as a process or command, as it sets environment variables.

#### . devnew
This will erase and recreate the development python virtual environment.

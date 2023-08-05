# RIPE Atlas Sagan

A parsing library for RIPE Atlas measurement results


## Why this exists

RIPE Atlas generates a **lot** of data, and the format of that data changes over
time.  Often you want to do something simple like fetch the median RTT for each
measurement result between date `X` and date `Y`.  Unfortunately, there are are
dozens of edge cases to account for while parsing the JSON, like the format of
errors and firmware upgrades that changed the format entirely.

To make this easier for our users (and for ourselves), we wrote an easy to use
parser that's smart enough to figure out the best course of action for each
result, and return to you a useful, native Python object.


## How to use it

You can parse a result in a few ways.  You can just pass the JSON-encoded
string:

```python
from ripe.atlas.sagan import PingResult

my_result = PingResult("<result string from RIPE Atlas ping measurement>")

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```

You can do the JSON-decoding yourself:

```python
from ripe.atlas.sagan import PingResult

my_result = PingResult(
    json.dumps("<result string from RIPE Atlas ping measurement>")
)

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```

You can let the parser guess the right type for you, though this incurs a
small performance penalty:

```python
from ripe.atlas.sagan import Result

my_result = Result.get("<result string from RIPE Atlas ping measurement>")

print(my_result.rtt_median)
123.456

print(my_result.af)
6
```


### Which attributes are supported?

Every result type has its own properties, with a few common between all types.

Specifically, these attributes exist on all `*Result` objects:

* `created`  An arrow object (like datetime, but better) of the `timestamp` field
* `measurement_id`
* `probe_id`
* `firmware` An integer representing the firmware version
* `origin`  The `from` attribute in the result
* `is_error` Set to `True` if an error was found

Additionally, each of the result types have their own properties, like
`packet_size`, `responses`, `certificates`, etc.  You can take a look at the
classes themselves, or just look at the tests if you're curious.  But to get you
started, here are some examples:

```python
# Ping
ping_result.packets_sent  # Int
ping_result.rtt_median    # Float, rounded to 3 decimal places
ping_result.rtt_average   # Float, rounded to 3 decimal places

# Traceroute
traceroute_result.af                   # 4 or 6
traceroute_result.total_hops           # Int
traceroute_result.destination_address  # An IP address string

# DNS
dns_result.responses                        # A list of Response objects
dns_result.responses[0].response_time       # Float, rounded to 3 decimal places
dns_result.responses[0].headers             # A list of Header objects
dns_result.responses[0].headers[0].nscount  # The NSCOUNT value for the first header
dns_result.responses[0].questions           # A list of Question objects
dns_result.responses[0].questions[0].type   # The TYPE value for the first question
dns_result.responses[0].abuf                # The raw, unparsed abuf string

# SSL Certificates
ssl_result.af                        # 4 or 6
ssl_result.certificates              # A list of Certificate objects
ssl_result.certificates[0].checksum  # The checksum for the first certificate

# HTTP
http_result.af                      # 4 or 6
http_result.uri                     # A URL string
http_result.responses               # A list of Response objects
http_result.responses[0].body_size  # The size of the body of the first response
```


### "But... I'd rather my code explode when there's an error"

If you'd like Sagan to be less forgiving, you only need to pass
`on_error=Result.ACTION_FAIL` when you're instantiating your object.  To use one
of our previous examples:

```python
from ripe.atlas.sagan import Result

my_result = Result.get(
    '{"dnserr":"non-recoverable failure in name resolution",...}',
    on_error=Result.ACTION_FAIL
)
```

The above will explode with a `ResultParseError`.


## What it supports

Essentially, we tried to support everything.  If you pass in a DNS result
string, the parser will return a `DNSResult` object, which contains a list of
`Response`s, each with an `abuf` property, as well as all of the information in
that abuf: header, question, answer, etc.

```python
from ripe.atlas.sagan import DnsResult

my_dns_result = DnsResult("<result string from a RIPE Atlas DNS measurement>")
my_dns_result.responses[0].abuf  # The entire string
my_dns_result.responses[0].abuf.header.arcount  # Decoded from the abuf
```

We do the same sort of thing for SSL measurements, traceroutes, everything.  We
try to save you the effort of sorting through whatever is in the result.


## What it requires

As you might have guessed, with all of this magic going on under the hood, there
are a few dependencies:

* [arrow](https://pypi.python.org/pypi/arrow)
* [pyOpenSSL](https://pypi.python.org/pypi/pyOpenSSL) (Optional: see "Troubleshooting" below)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)
* [pytz](https://pypi.python.org/pypi/pytz)
* [IPy](https://pypi.python.org/pypi/IPy/)

Additionally, we recommend that you also install
[ujson](https://pypi.python.org/pypi/ujson) as it will speed up the
JSON-decoding step considerably, and [sphinx](https://pypi.python.org/pypi/Sphinx) if you intend to build the
documentation files for offline use.


## How to install

The stable version should always be in PyPi, so you can install it with `pip`:

```bash
$ pip install ripe.atlas.sagan
```


### Troubleshooting

Some setups (like MacOS) have trouble with building the dependencies required
for reading SSL certificates.  If you don't care about SSL stuff and only want
to use sagan to say, parse traceroute or DNS results, then you can tell the
installer to skip building ``pyOpenSSL`` by doing the following:

```bash
$ SAGAN_WITHOUT_SSL=1 pip install ripe.atlas.sagan
```


## Further Documentation

Complete documentation can always be found on
[the RIPE Atlas project page](https://atlas.ripe.net/docs/sagan/), and if you're
not online, the project itself contains a `docs` directory -- everything you
should need is in there.


## Colophon

But why *Sagan*?  The RIPE Atlas team decided to name all of its modules after
explorers, and what better name for a parser than that of the man who spent
decades reaching out to the public about the wonders of the cosmos?


## Changelog

* 0.2.7
    * Made abuf more robust in dealing with truncation.
* 0.2.6
    * Replaced `SslResult.get_checksum_chain()` with the
      `SslResult.checksum_chain` property.
    * Added support for catching results with an `err` property as an actual
      error.
* 0.2.5
    * Fixed a bug in how the `on_error` and `on_malformation` preferences
      weren't being passed down into the subcomponents of the results.
* 0.2.4
    * Support for `seconds_since_sync` across all measurement types
* 0.2.3
    * "Treat a missing Type value in a DNS result as a malformation" (Issue #36)
* 0.2.2
    * Minor bugfixes
* 0.2.1
    * Added a `median_rtt` value to traceroute ``Hop`` objects.
    * Smarter and more consistent error handling in traceroute and HTTP
      results.
    * Added an `error_message` property to all objects that is set to `None`
      by default.
* 0.2.0
    * Totally reworked error and malformation handling.  We now differentiate
      between a result (or portion thereof) being malformed (and therefore
      unparsable) and simply containing an error such as a timeout.  Look for
      an `is_error` property or an `is_malformed` property on every object
      to check for it, or simply pass `on_malformation=Result.ACTION_FAIL` if
      you'd prefer things to explode with an exception.  See the documentation
      for more details
    * Added lazy-loading features for parsing abuf and qbuf values out of DNS
      results.
    * Removed the deprecated properties from `dns.Response`.  You must now
      access values like `edns0` from `dns.Response.abuf.edns0`.
    * More edge cases have been found and accommodated.
* 0.1.15
    * Added a bunch of abuf parsing features from
      [b4ldr](https://github.com/b4ldr) with some help from
      [phicoh](https://github.com/phicoh).
* 0.1.14
    * Fixed the deprecation warnings in `DnsResult` to point to the right
      place.
* 0.1.13
    * Better handling of `DNSResult` errors
    * Rearranged the way abufs were handled in the `DnsResult` class to make
      way for `qbuf` values as well.  The old method of accessing `header`,
      `answers`, `questions`, etc is still available via `Response`, but this
      will go away when we move to 0.2.  Deprecation warnings are in place.
* 0.1.12
    * Smarter code for checking whether the target was reached in
      `TracerouteResults`.
    * We now handle the `destination_option_size` and `hop_by_hop_option_size`
      values in `TracerouteResult`.
    * Extended support for ICMP header info in traceroute `Hop` class by
      introducing a new `IcmpHeader` class.
* 0.1.8
    * Broader support for SSL checksums.  We now make use of `md5` and `sha1`,
      as well as the original `sha256`.


Reflector is a small tool that listens for TCP connections and connects back to
whomever connects to it.

It's mostly meant as an experiment for monitoring purposes. Instead of relying
on other nodes to monitor you (to ensure that your services work over the
network and not just locally), we can use this reflector to monitor ourselves,
but effectively going across the network (and back) to do so.

# StGB

An experiment to make the structure of a long document easier accessible.

![](preview.jpg])

## Build

The easiest way is to build it with Nix (with Flakes enabled):

```
$ nix build github:erictapen/stgb
```


Alternatively clone the repository and build it by hand:


```
$ git clone git@github.com:bundestag/gesetze.git

$ pandoc -t html gesetze/s/stgb/index.md | python3 stgb.py
```

Instead of building, the resulting `stgb.html` and `stgb.json` could also be downloaded fromthe root of the webserver at `https://stgb.erictapen.name/`.

---
title: "How to extract a single rendered file from helm template output with awk"
date: 2026-09-08T10:00:00 +0100
lastmod: 2026-09-08T10:00:00 +0100
draft: false
description: "Slice one rendered manifest out of a multi-document helm template output using a tiny awk flag-toggle idiom - and how the idiom actually works, rule by rule."
author: "Jan Toth"
tags: ["awk", "helm", "kubernetes", "bash"]
categories: ["Linux"]
---

`helm template` dumps every rendered manifest into one long stream, each file
prefixed with a marker comment:

```
# Source: otel-central/charts/opentelemetry-collector/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
...
# Source: otel-central/charts/opentelemetry-collector/templates/service.yaml
apiVersion: v1
kind: Service
...
```

Helm does have `--show-only` for this, but it wants the template path in a very
specific form and (at least with subcharts on some Helm versions) refuses paths
it printed itself. This awk one-liner works regardless:

```bash
helm template ./mychart | awk '/^# Source:/ { show = ($0 ~ /configmap\.yaml$/) } { if (show) print }'
```

Output: only the `configmap.yaml` block - marker line plus everything under it,
stopping exactly at the next `# Source:` marker.

## How it works

awk runs the **whole script once per input line**. Variables are global and
keep their value from line to line - nothing resets them between lines. The
script is two rules:

```awk
/^# Source:/ { show = ($0 ~ /configmap\.yaml$/) }   # rule 1
{ if (show) print }                                 # rule 2
```

**Rule 1** only fires on marker lines (`^# Source:`). Its action evaluates
whether the *current line* (`$0` = the entire line) ends with the wanted
filename - `$0 ~ /regex/` returns `1` on match, `0` otherwise - and stores that
number in `show`. So every marker line re-decides the flag: wanted file → `1`,
anything else → `0`.

**Rule 2** has no pattern, so it runs on *every* line: if `show` currently
holds a non-zero value, print the line. It never inspects the line's content
at all - only the stored flag.

The content lines between markers never match rule 1, so nothing touches
`show` there - it just carries the value the last marker gave it. That's the
entire trick: matching and printing are decoupled, connected only by one
variable acting as an on/off switch. "Stopping at the next file" isn't
special logic - the next `# Source:` line simply re-runs rule 1, the filename
test fails, `show` becomes `0`, and rule 2 goes quiet.

## The idiomatic short form

Seasoned awk scripts compress rule 2 down to a bare variable name:

```bash
awk '/^# Source:/ { show = ($0 ~ /configmap\.yaml$/) } show'
```

A bare expression as a pattern means "test it for truthiness", and a rule with
no action gets the default action `{ print }`. So `show` alone is exactly
`show != 0 { print }`. Same program, fewer characters - use whichever your
future self will read faster.

## Generic template

Nothing here is helm-specific - it extracts any marker-delimited block from
any stream (multi-doc configs, log sections, SQL dumps):

```bash
awk '/^MARKER_PATTERN/ { show = ($0 ~ /WANTED_VALUE/) } { if (show) print }' file
```

Bonus: because every marker re-evaluates the flag, multiple matching blocks
scattered through the file all get printed - no extra logic needed.

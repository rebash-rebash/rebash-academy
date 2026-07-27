#!/bin/sh
# Strip Cursor agent co-author trailers injected by the IDE.
sed -i.bak '/cursoragent@cursor\.com/d' "$1"
rm -f "$1.bak"

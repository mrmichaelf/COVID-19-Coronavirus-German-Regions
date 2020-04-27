rem magick convert -size 480x de-districts-2020-01-28.svg -resize 480x de-districts-2020-01-28.png

magick convert -delay 150x1000 -size 480x out/de-districts/Cases_Last_Week_Per_Million-*.svg -coalesce -fuzz 2% +dither -resize 480x -layers Optimize out/de-districts-Cases_Last_Week_Per_Million.gif

magick convert -delay 150x1000 -size 480x out/de-districts/Deaths_Last_Week_Per_Million-*.svg -coalesce -fuzz 2% +dither -resize 480x -layers Optimize out/de-districts-Deaths_Last_Week_Per_Million.gif

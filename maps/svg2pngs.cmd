rem magick convert -size 480x de-districts-2020-01-28.svg -resize 480x de-districts-2020-01-28.png

magick convert -delay 100x1000 -size 480x out/*.svg -resize 480x -layers Optimize out/ani.gif
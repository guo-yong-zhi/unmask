windres -i ico.rc -o icon.o
gcc .\start-up.c icon.o -o StartUp
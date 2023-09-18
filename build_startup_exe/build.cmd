windres -i heart.rc -o heart.o
gcc .\startup-holly_cloze.c heart.o -o "Holly Cloze"

windres -i magnifying-glass.rc -o magnifying-glass.o
gcc .\startup-words_excluded.c magnifying-glass.o -o "Words Excluded"

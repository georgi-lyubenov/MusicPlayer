Проектът представлява програма, която crawl-ва дадена директория от хард диска за файлове с различни аудио разширения(mp3, ogg), извлича от тях метаданни като дължина,битрейт,име(и др.), записва ги в база данни и предоставя възможността за създаването на плейлист, сортиран по даден критерий(както и оценяване на песните по скала). Плейлиста има опции като Shuffle и Repeat Playlist, освен възможност за възпроизвеждане на стриймове.
Използвани са mutagen,SqlAlchemy, pygame.
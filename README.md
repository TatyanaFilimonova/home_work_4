# home_work_4

Домашняя работа на тему "параллельные потоки"

Файл clean_.py  - исходный код из домашнего задания № 6, где папка с мусором разбирается рекурсивно.

Файл clean_trash - рефакторинг исходного кода, теперь рекурсивный обход папок происходит в параллельных потоках.
Обработку отдельных файлов в параллельных потоках пришлось исключить, потому что падала окорость работы скрипта (в разы).

В clean_trash включены сравнительные тесты скорости работы для однопоточного варианта  с N-поточными.

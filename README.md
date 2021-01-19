﻿
# Пояснительная записка к проекту "Battle City" 

Авторы проекта: Карасев Владислав и Кимейша Артём 


## Идея проекта
 **Главная идея и цель проекта**  - создать правдоподобную ПК версию легендарной игры на NES ''Battle City''.

## Описание технологий

 - **Функции** terminate() - закрывает игру, game_is_over() - загрузка провала игры, load_image() - загрузка картинок из папки assets, load_level() - загружает нужный уровень, load_sound() - добавляет звуки для игры, game() - сам игровой процесс(P.S. Главная функция)
 
 - **Методы**
      - update - универсальная функция для всех классов, которая обновляет каждый класс в соответствии с его назначением.


 ## Библиотеки

1. **Pygame** - библиотека для создания компьютерных игр и мультимедиа - приложений.
**Дополнительные библиотеки Pygame:**
	- pygame - gui - это модуль, который поможет создавать графические пользовательские интерфейсы для игр, написанных на pygame.
3. Встроенные библиотеки **random, os** и **sys**


## Описание реализации
Для реализации основной задачи - создания игры, используем библиотеку **pygame**. Отрисовываем картинки в pygame - gui и заставляем их двигаться с помощью питона.
После этого мы создавали бота, который может сам ездить, стрелять и поворачивать в каком - либо направлении.
В оригинале игры также было много уровней, которые игрок должен был пройти. В связи с поставленными строками мы смогли реализовать лишь 5 уровней, но они получились очень интересными.
У игрока имеется 3 жизни, и если он умрёт более чем 3 раза, то игра закончится и придётся начинать всё заново.
Кроме этого мы сделали режим для двух человек, в которым пользователь, скачавший игру, может подключить геймпад к компьютеру и позвать своего друга попробовать пройти эти 5 уровней вместе.
## Скриншоты приложения
![Imgur](https://i.imgur.com/pV8QuDC.png)
![Imgur](https://imgur.com/ZvfYly3.png)

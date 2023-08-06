=====
Fotorama slider
=====

Фоторама слайдер - это простое приложение для Django,для интеграции js-css галереи Fotorama

Quick start
-----------

1. Добавьте fotorama в файл settings.py в кортеж INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'fotorama',
    )

2. В переменную FOTORAMA_CROP_SIZE - размер кропа для изображений::

    FOTORAMA_CROP_SIZE = '600x300'

3. Запустите `python manage.py syncdb` для создании таблицы в базе данных.

Using
-----

1. Подгрузить CSS и JS файлы фоторамы с помощью шаблонных тегов из библиотеки fotorama, для работы необходим jquery::

    {% load fotorama %}
    <head>
    ...
    {% fotorama_css %}
    {% fotorama_js %}
    </head>

2. В админской панели добавьте фотографии в слайдер

3. Вывести с помощью шаблонного тега fotorama_slider::

    {% fotorama_slider %}

4. Для изменения стандартного шаблона фоторамы - измените /templates/fotorama/default.html::

    {% load cropping thumbnail %}
    <div class="fotorama" data-nav="thumbs">
        {% for slide in slide_list %}
            <a href="{% cropped_thumbnail slide 'cropping' %}"><img src="{% thumbnail slide.image '50x50' %}"></a>
        {% endfor %}
    </div>

5. Будут обновления!
pyramid_soy
-----------

pyramid_soy is a simple wrapper of `Soy` (closure-template-python).

It provides simple cache for soy template file and pyramid directive for convenient.

##Config

Open your project config file `***.ini`.
Add include settings in your config file
```
pyramid.includes =
    pyramid_soy
```
Or include it in your pyramid init script.
```
def includeme(config):
    config.include('pyramid_soy')
```

##Usage
Use `config.add_soy_searchpath` to add search path of complied soy template file(ends with `.py`).

Use `request.soy_render_tostring(template_name, name_space, **data)`

More docs detail in source code.

##About

[Github](https://github.com/winkidney/pyramid_soy)

# Django Boot Core - Starter

[![PyPI - Version](https://img.shields.io/pypi/v/django-boot-core-starter?style=flat-square)](https://pypi.org/project/django-boot-core-starter)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/django-boot/django-boot-core-starter/project-code-standards.yml?style=flat-square)](https://github.com/django-boot/django-boot-core-starter/actions/workflows/project-code-standards.yml)
[![GitHub issues](https://img.shields.io/github/issues/django-boot/django-boot-core-starter?style=flat-square)](https://github.com/django-boot/django-boot-core-starter/issues)
![Static Badge](https://img.shields.io/badge/Status-Under%20Development-yellow?style=flat-square&cacheSeconds=120)


Core starter library for Django Boot.

This library will initialize [Rhazes](https://github.com/django-boot/Rhazes) `ApplicationContext` by default and registers some beans on it.


## Usage

First, add Django Boot Starter to `INSTALLED_APPS`:


```python
INSTALLED_APPS = [
    ...,
    "django_boot_core",
]
```

Then assure you have these two settings in your `settings.py`:

```python
DJANGO_BOOT = {
    "DI_PACKAGES": [],  # packages containing beans which you want to be scanned in your project
    "DI_SCAN_STARTERS": False,
    "APPLICATION_CONFIGURATION": {
        ... # Configuration for ApplicationConfiguration. Read below
    }
}
```

### Application Configuration Parser

Main benefit of using this library is that you will have `ApplicationConfiguration` bean registered for you.

This bean allows you to use configuration files for different services (beans) in your project easily.

`django_boot_core.services.ApplicationConfiguration` is an autoconfigured extension on top of [parse_it](https://github.com/naorlivne/parse_it) library.

To configure `ApplicationConfiguration` (and `ParseIt` class) try changing these values in the settings.

```python
# settings.py

DJANGO_BOOT = {
    "APPLICATION_CONFIGURATION": {
        # Read what blow items do in `parse_it` documentation.
        "LOCATION": os.path.join(BASE_DIR, "application_config"), # Optional, Location to read configuration files from
        "CONFIG_TYPE_PRIORITY": ..., # optional
        "GLOBAL_DEFAULT_VALUE": ..., # optional
        "TYPE_ESTIMATE": ..., # optional
        "RECURSE": ..., # optional
        "FORCE_ENVVARS_UPPERCASE": ..., # optional
        "ENVVAR_PREFIX": ..., # optional
        "SUFFIX_MAPPING": ..., # optional
        "ENVVAR_DIVIDER": ..., # optional
        "NONE_VALUES": ..., # optional
    }
}
```

Default configuration location (directory) (in case `BASE_DIR` is set in `settings.py`) would be `{BASE_DIR}/application_config`.


### Write your own starter apps

You can make Django Boot scan your apps by default without having to add anything specific in settings `DI_PACKAGES` by ending your app names in `_starter`.

To enable this feature you need to specify `DJANGO_BOOT["DI_SCAN_STARTERS"] = True` in settings.

```python
DJANGO_BOOT = {
    "DI_SCAN_STARTERS": True,
    # other configurations here
}
```

**Example:** you have an app called `polls` and it requires some beans to be registered into `ApplicationContext`. You can rename the app to `polls_starter` instead and this library will automatically pick it to scan.

Alternatively (perhaps for performance reasons as well) you can skip this and just let other developers know that which packages then need to add to settings `DI_PACKAGES` after they install your app.

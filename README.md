# ProdSelect

Project with the most imaginative name ever!!1

## Cloud Setup

This app lives on Divio cloud:
 * Staging: https://what-test-stage.eu.aldryn.io/
 * Production: https://what-test.eu.aldryn.io


## Local Setup

### According to Divio

Install the [Divio CLI](https://github.com/divio/divio-cli) to set up your app locally.

Alternatively, build this app locally using Docker:

1. Ensure [Docker](https://docs.docker.com/get-docker/) is installed and running.
2. Clone this repository locally.
3. Build the app with `docker compose build`.
4. Run the migrations with `docker compose run --rm web python manage.py migrate`
5. Create a superuser with `docker compose run --rm web python manage.py createsuperuser`
6. Run the app using `docker compose up`.
7. Open [http://localhost:8000]() to view your app.


### Hybrid Setup

Alternatively alternatively, you can run the app locally while keeping the DB in Docker:

1. Install dependencies with `poetry install`.
    * Works on Python 3.12
    * Note: you can let Poetry handle the virtual environment, or you can use your own (e.g., pyenv).
2. Run the server with `python app/application.py`.
    * Or set up your IDE to do this, otherwise it's simpler to use Docker setup above.
3. Optionally configure Django to connect to Postgres DB on Docker.
    * Run the db using `docker compose up -d database_default`
    * TODO not working yet.
       * needs `ports` in `docker-compose.yml` and probably `DATABASE_URL` in `.env`
       * and `python-dotenv` or similar.

Why? Debugger! It is possible to set up a debugger to work on code running in Docker, but it's not worth the trouble.

## Project Structure

The project is split into two apps:
 * `backend` - Django app with DRF API and the admin.
 * `ui` - Dash app for the UI.

# Production Checklist / TODO

## Remove the "CRAZY" Authentication

Obviously!

Grep for `CRAZY`. It's all in the `crazy_registration` app.

## Allow UI to Load All Products

Currently, when the search field is empty, the UI shows empty table. There is no reason to not load all products
(pagination is in place). It is just a single `if` in the code to remove.

## API Throttling

DRF provides `DEFAULT_THROTTLE_CLASSES` setting.

## Django Checklist

The official checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

## Changelog and Versioning

https://keepachangelog.com/


# Wishlist / Things to Improve

Some random notes about things that could be improved, added, finished, etc.

## Typed Django

Type hints are notoriously difficult with Django, but would be nice to have. Using `django-stubs`.

## Decouple AG Grid UI Actions from API Calls

This would enable, for example, rapid clicking on header columns to change sorting, without waiting for the API to
respond to each change. Debounce, basically.

## We Might Not Need the API

AG Grid is very efficient at handling data. It might be worth it to load all data at once, and then perform
filtering and sorting on the client side. This will be more performant.

The API option is good for large datasets, but could be overkill for small ones.

Since this is a test, it made sense to demonstrate the API use case.

## Fuzzy Search

Could implement fuzzy search. Postgres backend in Django has this built-in, via "trigram" extension.
https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/search/#trigram-similarity

## JS Code in Python

Depending on personal preferences, people might find it weird to have JS code in Python files.

Dash supports writing callback functions in `.js` files, as was done in `auth.js` and `products.js` Both approaches are
present here for demonstration purposes. In real projects, it would be best to stick to one approach, for consistency.


## Pages from `dash-extensions`

Built-in support for multi-page apps in Dash is relatively new. Dash-extensions has had it for a while, and the two
approaches are different:
 * Built-in Dash multi-page apps completely unload other pages when switching.
   * Good for memory usage, but hits the server on every page switch.
 * Dash-extensions keeps all pages loaded, and just hides them.
   * This is better for performance, but worse for memory usage.

I have opted for the built-in solution.

### Cache!

If page layouts are built to be fixed (and data is loaded exclusively via callbacks), then it is possible to cache
the layouts of the pages. This could actually be the best approach, as it would provide the best of both worlds:
 * No need to hit the server on every page switch.
 * No need to keep all pages loaded in memory.
 * We can preload all the pages and do it after page-load (so to not slow down the initial page load).

Caching is implemented (lifted from a community thread, see `pages.Cache.js`). Stripped the preloading part, though,
to keep is simple.

## Pagination Bug

There seems to be an intermittent bug with pagination in AG Grid. Sometimes, the "to" label shows "?" instead of
a number. Seems to be related: https://github.com/ag-grid/ag-grid/issues/4295

## Logging

Configure Python's logging properly.


# Notes / Comments

Here are some even more random notes about decisions made during development, ideally with reasoning behind them.

Things below here are more as a reminder to myself and as a thoughts dump, rather than a coherent text ready for
consumption. Thou hast been warned!

## General

### Project Structure

This project uses:
 * Django with DRF for the API
    * nothing unusual with this...
 * Dash app for the UI
    * This is unusual because Dash is a fully-fledged web framework in itself, and it's not common to see it used
      alongside Django.
    * Here we are using Dash exclusively for the UI.
       * It never interacts with anything else than the DRF API.
    * I love Dash because I can set up the whole project without any frontend machinery (Webpack, vite, etc.)

The two apps are completely independent of each other.
They don't share any code, and they don't interact with each other (except for the API calls).
HOWEVER:
 * They are both served by the same WSGI server.
    * Ideally they would be packaged in separate images (i.e., containers), but that was deemed overkill for this task.
       * (would need two Divio apps, two Dockerfiles, two docker-compose files, etc.)
       * Instead, they are both served by the same WSGI server, in `app/application.py`.
       * However, it is easy to separate them into two separate images, at a later stage.
 * They share the same requirements definition (in `pyproject.toml` and `poetry.lock`).
    * This is not ideal
       * but there are no conflicts, and they are not likely to happen.
    * Separating the requirements would probably be the most non-straightforward part of separating the two apps into
      separate images.


### No Code in Repo Root

I just don't like to have code in project root. One exception to this is any kind of management scripts (like
`manage.py`), btu if there are many of them, I would put them in a `scripts` directory.

Lots of things must go in repo root (`Dockerfile`, `docker-compose.yml`, `.pre-commit-config.yaml`, etc.), so
whatever we can do to reduce the clutter is IMHO good.


## Django Project (App)

(Django "project" is a WSGI "app"... Nomenclature is confusing.)

### Separate Module for Apps

Having all apps in a single module is not the default structure for a Django project, but it's also not that unusual.
Other than having a more verbose `import` statements, I see no downside.

Upside is that we can put other stuff in the project root, like `templates`, `locale`, etc.


### Custom User Model

Not very useful in this test task, but it's a good practice to use a custom user model from the start. Adding it
later on is a pain.


### Serializers in `api` App

Normally, DRF serializers would be in the same app as the models they serialize. However, since the API app is
solely concerned with providing the API, I decided to put them there. I like the separation of concerns here.


## Dash App

### Why?

Mainly:
 * To make it interesting.
 * To see whether this approach is viable.
   * I know it will work, technically.
   * But I'm interested in seeing how it performs and if it is a viable way of setting up more demanding UIs.
 * Dash is built on top of React.JS
   * It is possible to "wrap" most React components in Dash components with relatively little effort.
     * IMHO Dash provides a much more pleasant development experience than React.
       * The concept of "callbacks" (terrible name, BTW!) is very easy to work with, and keeps the code clean.
       * We let Dash handle states, and we only write logic between state changes.
   * We define the layout in Python, which is a huge plus.
      * No JSX, no CSS-in-JS, no Webpack, no Vite, no Babel, no nothing.
      * Just HTML-in-Python.
      * Every "HTML element" defined here is a React.JS component, subject to being modified in a callback if
        needed.
   * Usually the worst part of Dash is performance.
      * This is due to how callbacks are usually made - in PYTHON (the HORROR!!!).
        * However, this is only because (AFAICT) Dash is being marketed primarily towards data scientists, who are
          as a rule good with Python but not with JS.
        * The effect of this is that usually, for _any_ change on the UI, the browser needs to ping the server.
          * E.g.: Clicked the "X" button to close a modal prompt? Wait for the browser to ask the server to run a
            function ("callback") which will (always) return `False`.
        * Dash has a very well-defined way of writing JS callbacks.
          * In this test task, all callbacks will be written in JS.
            * Hopefully, performance will be great!
              * Maybe a bit slow on page-load; this is what I'm most interested in.

### Isn't Dash Just for Data Science?

It is marketed this way. But I genuinely don't think this is the case. Hoping to prove this with this test task.

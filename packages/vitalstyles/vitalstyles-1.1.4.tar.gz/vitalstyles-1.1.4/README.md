# Vitalstyles

Makes it easy to document you LESS/SASS/CSS. You document your styles by inserting markdown with a few extensions to markup examples.


## Goals
Make it easier to document and develop styles.


## Features
- Document your styles with Markdown.
- Create live previews:
    - Inline in the guide for simple examples.
    - Covering the full width of the guide page for more complex examples.
    - Rendered in a full width IFRAME for really complex examples. These examples can also be opened in a separate file.


## Install
```
$ pip install vitalstyles
```

## How it works
You write your css/less/sass like you have always done, but you add markdown in special comments:

``` css
/**
# Buttons

## .fancybutton
A fancy button

$$$
<button class="fancy-button">Click me</button>
$$$
*/
.fancy-button {
}
```

The ``vitalstyles-cli`` can be executed from the directory containing the file with these styles, and it will create a style guide in ``vitalstyles_styleguide/``. By default it will search the current directory recursively for ``*.less``, ``*.sass``, ``*.scss`` and ``*.css`` files.


## Configuration
You can configure vitalstyles through a ``vitalstyles.json`` file. This is the default setting file with defaults:

``` javascript
{
    // Path to your CSS file relative to this settings file (or CWD if no settings file).
    // You have to set this to get previews.
    "preview_cssfile": null,

    // The output directory relative to the settings file (or CWD if no settings file).
    "outdir": "vitalstyles_styleguide",

    // A list of files or directories to parse.
    // Directories is searched recursively for ``.scss``,
    // ``.sass``, ``.css`` and ``.less`` files.
    "inpaths": [],

    // User defined templates directory. You can override any
    // templates in the ``vitalstyles/templates/`` directory
    // (in the repo) by putting them in a directory and specifying
    // the directory here. The path is relative to this settings file.
    "template_dir": null,

    // The title of the guide
    "title": "Vitalstyles style guide",
    
    // Include stock assets? This will add a directory named
    // stock to your assets/ directory, and fill it with assets
    // that you can use in your styleguide.
    'include_stock_assets': false,

    // A list of filesystem directories. The contents of these directories
    // are copied into the assets sub-directory of the ``outdir``.
    // The directory itself is not copied, so if you specify two directories
    // containing the same file, the file from the last directory in the
    // list will overwrite the first.
    'asset_directories': []

}
```


## Embedded previews in the docs
If you want to get previews, you have to configure ``preview_cssfile`` in a ``vitalstyles.json``.


## Bundled stock images
We bundle a set of stock images. The bundled stock images are from https://unsplash.com/ and http://www.gratisography.com/.

To use the bundled stock images, you simply set the ``include_stock_assets`` setting to ``true``. This will copy the images from ``vitalstyles/sock_assets/stock/`` (in the sources of this library) into the ``assets/stock/`` subdirectory of the directory specified in the ``outdir`` setting.


## Adding assets (images, videos, etc)
If using the bundled stock images is not enough, you can include one or more asset directories using the ``asset_directories`` setting. You simply add the path to the directories you want to copy into the ``assets/`` subdirectory of the directory specified in the ``outdir`` setting.  


## Specifying settings using Python or making a custom CLI
If configuring the styleguide using JSON is not enough, you can make a custom CLI script. This is fairly simple, and it is demonstrated in ``examples/custom_vitalstyles_cli.py``.


## Complete example
See the ``examples/`` directory in the source repo. To build the example, install Vitalstyles and GruntJS and run the following::

    $ cd examples/
    $ npm install
    $ grunt

Then open ``vitalstyles_styleguide/index.html``.


## Markdown dialect
The Markdown dialect is more or less the same as the GitHub format, with one additional tag to markup examples.

The Markdown parser is [python-markdown](https://pythonhosted.org/Markdown/), with the following [extensions](https://pythonhosted.org/Markdown/extensions/index.html):

### Fenced code blocks
Makes it possible to use github markdown styled code blocks like:

    ``` javascript
    function add(a, b) {
        return a + b;
    }
    ```

### Smart strong and smart emphasis
Prevents markdown from emphasizing words when you use ``_`` and ``__`` in the middle of a word.

### Definition Lists
Makes it possible to define definition lists with the following markup:

```
Option one
:   This is not a very good option. You should consider
    using _option two_.

Option two
:   This is a really good option.
```

### Tables
Makes it possible to create tables with the following markup:

```
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```


### SmartyPants
Converts ASCII dashes, quotes and ellipses to their HTML entity equivalents


### Sane lists
Renders lists in a saner manner than the original Markdown.

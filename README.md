# webflow2reactnative
Webflow exorted data can be parsed over fairly easily using python. From the HTML and CSS data we can create React Native code. This generated React Native code contains usage of the [`styled-components`](https://www.styled-components.com).

## Install
```console
python3 -m pip install -r requirements.txt
```

## Usage
```console
Usage: python3 w2rn.py <input-dir> <output-dir>
```
### `input-dir`
This is the directory that contains the Webflow extracted data. For example you will see something like this
```
.
+-- css
|   +-- normalize.css
|   +-- ...
+-- icons
|   +-- favicon.ico
|   +-- ...
+-- js
+-- index.html
...
```
### `output-dir`
This is the directory which will house all React Native code generated from the Webflow exported data in `input-dir`. Here is an example of some output:
```
+-- src
|   +-- ui
|   |   +-- views
|   |   |   +-- IndexView.js
|   |   |   +-- ...
```



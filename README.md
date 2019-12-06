# webflow2reactnative
Webflow exorted data can be parsed over fairly easily using python. From the HTML and CSS data we can create React Native code. This generated React Native code contains usage of the [`styled-components`](https://www.styled-components.com).

## Install
```console
python3 -m pip install -r requirements.txt
```

## Usage
```console
Usage: python3 w2rn.py <input-dir> <output-dir> [--lng-file <file-path>]
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

## What do I do with this generated JS?
The JS is ready to be used in a React Native project. We will refer to our `buoyantwallet` repository as this is the first repo to utilize this tool.

`buoyantwallet` contains these generated classes within the `src/ui/components` folder. You will also notice the actual screens that get shown in buoyant wallet within the `src/ui/screens` folder. 

Let's take the `AppAuthentication.js` file in `src/ui/screens`. You will notice in the `render` method of this component that we display the `Authentication` component within `src/ui/components`. The `Authentication` component within `Authentication.js` is what comes out of `w2rn`. 

You will see that I simply define all my state in the `AppAuthentication.js` parent and push everything down to it's child, which is `Authentication.js` 

Convention I have been using in my components has been, if the method has a `_` in front of it then it is a function that is private and only used within the component/class itself. Otherwise, it is called/used externally.

Take note of the `login` function within `AppAuthentication.js`. Notice that in the `render` function I pass all the props and all the state items into `Authentication.js` via the JS spread operator. 


HOWEVER, if you have a behavior that must be passed, the function must be passed as well. See how we set `next` to `this.login`. Notice then in the `Authentication.js` file we have some custom code in there which spreads a JSON object defined in ComponentHelper:
```javascript
{...ComponentHelper.addButtonAttributes(this.props)}
```
Notice in here that we send back:
```javascript
const addButtonAttributes = props => {
  return {
    onPress: props.next,
    disabled: props.disabled
  }
}
```
This is how we can get the views genereated by `w2rn` to contain behaviors.

## Making Changes
This project is a work in progress. There are however certain places to integrate with and some parts that need fixing/updates; all will be outlined below.

### Adding support for new tags/elements
At a high level this project takes HTML and CSS, and converts them into React Native code. To do that we must parse The HTML and once a relevant tag/element is found we must then parse the CSS associated to it. Once we have the hierarchy of HTML and CSS we can create a `styled-component` and set the actual component in it's appropriate location within the `render` method.

The file `w2rn.py` is the main entry point and contains all the Matchers used. A Matcher is an object we are looking for within the HTML. `BeautifulSoup` will parse the HTML for us and we tell it, when you hit a tag I need, then please do something. The way to trigger this is with Matchers.

You will notice the following in w2rn.py
```python
Matcher("a", "class", "w-button", generators.gen_button, sc)
```
Here we are saying...
When you hit the tag/element `a` with `w-button` as an item within the `class` attribute, then call `generators.gen_button`. By item in there, there could be a comma separated list of classes, `w-button` just needs to be one of them. If you look at `generators.gen_button` this will create the `styled-component` and set itself in the heirarchy of components. 

#### Pitfalls you may run into
This section will describe the various things I have come across that will need to be addressed at some point. However, these are my workaround that got me by fine.
##### Unsupported CSS
When you execute after changing there is a possibility that the CSS genereated in the `styled-component` is not supported. You will be notified of this and what field is in the wrong via the React Native red screen of death :). 

Typically, you can remove the CSS as it sometimes is extraneos. However, if you need it, then you must figure out how to do this within the React Native CSS options. See documentation for that.

##### Things are not showing up...???
If things do not show up that can sometimes mean that we still have `flex-direction: row` and it should be `flex-direction: column`. React Native's flex implementation has a different default value for `flex-direction`. If you don't specify for CSS on the web...then `row` is what you get. If you don't specify in React Native, then `column` is your default.

The first thing to try when things don't show up is systematically (from the inside out) removing `flex-direction: row` from the `styled-component`. If that does not work, then it is time to start commenting out sections of code to see if those other sections work...and perhaps the entire piece is not working.

Really, it's down to you playing with the CSS to get thing to show up. This doesn't happen often but does when there are a lot of items on the screen.
### `--lng-file <file-path>`

This option points to a JS file that defines translations in the following format:

```
export default {
  // comment on string
  'my-string' : 'This is my translation'
}
```

Any occurrence of `my-string` will be replaced with `i18n.t('my-string')`.

# <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/regular/comments.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Language changer

Changes languages through Mycroft in MagicMirror and Mycroft.

| Supported Languages |
| ------------------- |
| English |
| Swedish |

## Dependency

The project is built for [OpenTTS](https://github.com/synesthesiam/opentts) as it easens language switching.

It is possible to go without but the code would have to be modified for it as the config management is hard coded.

## Installation

```bash
git clone git@github.com:krukle/language-skill.git ~/mycroft-core/skills/language-skill
```

> **Note**
>
> Change git clone destination according to your setup.

## Config

### MagicMirror

A variable `lang` and an object `translate` has to be added to your `config.js`.
`translate` should contain keys and values on how modules, `locale` and `language` should be translated.

Below is an example `config.js`.

```js
let lang = "en";
let translate = {
  LOCALE: {
    "sv": "sv-SE",
    "en": "en-US"
  },
    NOTES_HEADER: {
    "sv": "Anteckningar",
    "en": "Notepad"
  },
},
let config = {
  language: lang,
  locale: translate.LOCALE[lang],
  modules: [
    {
      module: "MMM-Notes", //module name
      position: "top_left",
      header: translate.NOTES_HEADER[lang]
    },
  ],
}
```

### Mycroft

*OpenTTS* uses the same API as *Marytts*. You therefore prepare the config for *Marytts* but point the `url` to wherever you're hosting *OpenTTS*.

```json
"tts": {
  "marytts": {
    "url": "http://wherever/opentts/is/hosted:portnumber",
    "lang": "en",
    "voice": "nanotts:en-US"
  },
  "module": "marytts"
}
```

## Message

| Message  | About |
| -------  | ----- |
| [configuration.updated](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/message-types#configuration.updated) | Emitted when configuration files has been updated. |

## Command

### Change language

| English | Swedish |
| ------- | ------- |
| "Change language to `language`" | "Byt språk till `language`" |

If `language` is omitted, Mycroft will ask the user which language to change to.

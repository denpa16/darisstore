[Вернуться к структуре](README.md)
# Содержание корневой директории
* `.browserslistrc`
  * Для таргетирования приложения под конкретные браузеры для ускорения работы, дефолтный конфиг
включает улучшенную поддержку двух последних версий современных браузеров
---
* `.editorconfig` и `.jsconfig.json`
  * Файлы конфигурации для тонких настроек **IDE** редакторов
---
* `.gitignore`
  * Список файлов и директорий, которые будут исключатся при коммите в **git**
---
* `.stylelintignore` и `.eslintignore`
  * Список файлов и директорий, которые будут исключатся из проверки линтеров
---
* `.stylelintrc` и `.eslintrc`
  * Конфигурации линтеров, **scss** и **code style** соответственно. [Подробнее про ESLint](https://eslint.org/) и [Stylelint](https://stylelint.io/)
---
* `babel.config.js`
  * Конфигурация для работы компилера [Babel](https://babeljs.io/)
---
* `simple-git-hooks.js` и `lintstagedrc`
  * Для работы **pre-commit** хуков. В момент пуша - в данный момент, запускаются линтеры для проверки,
соответствуют ли изменения нашим стандартам **code style**. [Подробнее о simple-git-hooks ](https://github.com/toplenboren/simple-git-hooks)
---
* `.npmrc`, `.nvmrc`
  * Требуются для проверки версий node/npm и для автоматического переключения на нужную версию
  * [Подробности как переключать версии с помощью nvm](https://www.notion.so/idaproject/node-npm-a730b66532aa494388f968bf4e07aa97) 
---
* `Dockerfile`, `Dockerfile.packages` и `entrypoint.production.sh`
  * Конфигурации для **ci-cd**, фронтам **(!)** руками не трогать
---
* `nuxt.config.js`, `nuxt.dev.config.js` и `nuxt.prod.config.js`
  * Файлы основной конфигурации **Nuxt**, модули, которые подключаются в зависимости от
среды **development**/**production** 
  * Не путать с dev/prod стейджами. development - это всегда локальное окружение, production - после билда, вне зависимости от стейджа 
  * [Документация Nuxt.js](https://nuxtjs.org/docs/directory-structure/nuxt-config/)
---
* `package.json` и `package-lock.json`
  * Список подключаемых node модулей, зависимостей скрипты для запуска и соответственно результат
сгенерированный в файл для работы с **node_modules** в виде **package-lock.json**
  * По правилам **package-lock.json** тоже нужно обязательно пушить, т.к. с каждой новой сборкой - могут подтянуться минорные
обновления зависимостей, которые способны негативно повлиять на работу всего приложения

# 04.09.2023

**Server Middleware:**

+ logger (showing api respond time)
+ headers (detecting yandex heatmap refer)<br>
  **Store:**
+ device (action **setYaMetricsObserverState**)
+ domain (action **changeActiveProtocol**)<br>
  **Directives:**
+ intersect.js (Intersection Observer)<br>
  **Modules:**
+ nuxtDelayHydrationExclude<br>
  **Components:**
+ VRange (v1.0.5: fix работы при параметре single)
+ MediaSlide (загрузка первичного изображения без превью)
+ Visual (генплан)
+ VImage - компонент для отображения изображений (с **ImgProxy** и двухэтапной загрузкой), не
  требующих адаптивов.<br>
  **Pages:**
+ Genplan: генплан, с возможностью "провалиться" вглубь.<br>
  **Utils:**
+ [third-party-scripts.js](https://www.notion.so/idaproject/TBT-0d6140af96774204a74e45b5bc0bab7b)

# 10.06.2023

**Core updates:**

+ node 20
+ nuxt 2.17

# 05.06.2023

**Dependencies:**

+ nuxt-delay-hydration
+ vanilla-lazyload
+ @nuxt/image
+ swiper (^8.4.7)<br>
  **Directives:**
+ vanilla-lazyload (v-lazy)<br>
  **Stores:**
+ header.js
+ device.js<br>
  **Components:**
+ LogoIda
+ TheHeader (store logic)
+ SideMenu (refactor)
+ sliders/HeroBannerSlider
+ sliders/MediaSlide
+ sliders/Navigation<br>
  **Pages:**
+ imgProxy: демо слайдера с двухэтапный lazyLoad
+ ui-kit: base/cards/filters/inputs - разбил навигацию компонентов на категории их применения

# 10.03.2023

**Core updates:**

+ node 16
+ nuxt 2.16.2
+ stylelint 14.16.1<br>
  **Components:**
+ rub (1.0.0): компонент для отображения знака рубля, если он отсутствует в применяемом шрифте. За
  основу взят шрифт 'pt-rouble', описание см. тут frontend/assets/fonts/pt-rouble/PT Rouble.pdf

# 01.02.2023

+ VInputSelect(1.0.1): вариант инпута с подсказками на базе YandexMaps api

# 27.01.2023

+ ProjectsFilterPage(1.0.2): в демке фильтрации проектов, поправил взаимодействие в utm тэгами
+ UiDemo(1.0.2): для отображения подробного описания компонента и примеров кода, теперь в .env
  требуется указать UI_DEMO=True
+ Добавлен middleware для отключения ui-kit на проде (frontend/store/domain.js - требуется в store
  указать боевой домен)
+ ui-kit отсортированы по имени
+ в default layout добавлен meta canonical

# 23.01.2023

+ VSelect(1.0.4): фиксы работы на мобильных устройствах
+ VRange(1.0.4): добавлены пропсы для кастомных лейблов
+ VTabBar(1.0.1): сделан рефактор, добавлено демо и новый тип переключение табов

# 15.01.2023

+ VFile(1.0.0)
+ VSkeleton(1.0.1)
+ VAccordion(1.0.1)
+ VIcon(1.0.1)
+ VBreadcrumbs(1.0.0)
+ VPopover(1.0.0)
+ VCalendar(1.0.0)

# 19.12.2022

+ Release info page
+ new scss mixins
+ mobile view
+ demo-menu (navigation)
+ axios-mock-adapter
+ Examples structure
+ Projects filter (example)
+ VRange(1.0.2) (fix)

# 11.2022

+ Основная структура ui-kit
+ DropdownOption(1.0.0)
+ InputHint(1.0.0)
+ SliderDot(1.0.0)
+ VButton(1.0.0)
+ VCheckbox(1.0.0)
+ VInput(1.0.0)
+ VInputThousands(1.0.0)
+ VRange(1.0.0)
+ VScrollBox(1.0.0)
+ VSelect(1.0.0)
+ VSlider(1.0.0)
+ VSwitch(1.0.0)
+ VTab(1.0.0)
+ VTabBar(1.0.0)

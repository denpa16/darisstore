<script setup
        lang="ts"
>
// #region Imports
// Type
import type { IHeader } from '~/components/layout/types';

// Stores
import { useHeaderStore } from '@/store/header';

// Utils
import { throttle, remToPx } from '@idaproject/core/assets/js/utils/common-utils';

// Components
import LogoIda from '@/components/common/LogoIda.vue';


// #region Interfaces
interface IHeaderData {
    isTicking: boolean,
    lastScroll: number,
    isInit: boolean,
}

// #endregion


// #region Props
const {
    theme = 'light',
} = defineProps<IHeader>();
// #endregion

// #region Data
// Nuxt
const { $device } = useNuxtApp();
const $style = useCssModule();
const headerStore = useHeaderStore();

const data: IHeaderData = reactive({
    burgerIntersection: false,
    isTicking: false,
    lastScroll: 0,
    isInit: false,
});
const throttleScroll = throttle(onScroll, 300) as () => void;

// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style._transparent]: headerStore.isTransparent,
        [$style._scrolled]: headerStore.isScrolled && headerStore.isVisible && !headerStore.isTransparent && !headerStore.isBurgerMenuVisible,
        [$style._hidden]: !headerStore.isVisible && !headerStore.isBurgerMenuVisible,
    },
]);
// #endregion

// #region Methods
/**
 * Отслеживаем, что положение окна ниже положения меню.
 * Для этого получаем данные из _variables.scss с помощью небольшого хака,
 * затем rem конвертируется в px
 * @public
 */
const handleCheckMenu = async () => {
    if (headerStore.isBurgerMenuVisible) {
        return;
    }

    const styleRecords = {
        Desktop: '7.2rem',
        Tablet: '6.8rem',
        Mobile: '6.4rem',
    };

    const menuHeightRem = styleRecords[$device.device];
    const isMoreMenuHeight = document.documentElement.scrollTop >= remToPx(menuHeightRem || '7.2rem');

    if (headerStore.isMenuWithHero) {
        headerStore.setTransparent(!isMoreMenuHeight);
    }

    if (isMoreMenuHeight) {
        if (document.documentElement.scrollTop > data.lastScroll) {
            if (headerStore.isVisible) {
                headerStore.changeVisibility(false);
            }
        } else if (!headerStore.isVisible) {
            headerStore.changeVisibility(true);
        }
        data.lastScroll = document.documentElement.scrollTop;
    } else {
        headerStore.changeVisibility(true);
    }
};

/**
 * Метод отвечающий за изменения состояния меню на скролле
 * Разбито на две хелпера, потому что логика на некоторых порталах достаточно объёмная
 * и с одним будет в этом случае трудно работать
 * @public
 */
const handleUpdateState = async () => {
    await Promise.all([
        headerStore.setScrolled(document.documentElement.scrollTop >= 1),
        handleCheckMenu(),
    ]);

    data.isTicking = false;
};

/**
 * Через requestAnimationFrame оптимизируем изменения состояний
 * @public
 */
function onScroll() {
    if (!data.isTicking) {
        data.isTicking = true;
        requestAnimationFrame(handleUpdateState);
    }
}
// #endregion


// #region Lifecycle
onMounted(() => {
    nextTick(() => {
        data.lastScroll = document.documentElement.scrollTop;
        window.addEventListener('scroll', throttleScroll);
    });
});

onUnmounted(() => {
    if (!throttleScroll) {
        return;
    }

    window.removeEventListener('scroll', throttleScroll);
});
// #endregion

</script>

<template>
    <header
        :class="[$style.TheHeader, classList, 'js-header']"
    >
        <div :class="['container', $style.wrapper]">
            <LogoIda to="/" />

            <div :class="$style.wrapperCenter" >
            </div>
        </div>
    </header>
</template>

<style lang="scss"
       module
>
    .TheHeader {
        position: fixed;
        top: 0;
        z-index: $header-z-index;
        width: 100%;
        max-width: calc(100% - var(--lock-offset, 0));
        height: $header-h;
        box-shadow: 0 .2rem .8rem rgba(0 0 0 / 0%);
        transition: background-color $default-transition, box-shadow $default-transition, transform .3s linear;

        &._light {
            background: $base-0;

            &:after {
                background-color: $base-400;
            }
        }

        &._dark {
            background-color: $base-600;

            &:after {
                background-color: $opacity-white-20;
            }
        }

        &._transparent {
            background-color: transparent;
            box-shadow: none;
        }

        &._scrolled {
            box-shadow: 0 8px 8px rgba(0 0 0 / 8%);
        }

        &._hidden {
            transform: translateY(-100%);
        }

        &:after {
            content: "";
            position: absolute;
            right: 0;
            bottom: 0;
            width: 100%;
            height: 1px;
        }
    }

    .wrapper {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        height: $header-h;
    }

    .wrapperCenter {
        flex: 1;
    }
</style>

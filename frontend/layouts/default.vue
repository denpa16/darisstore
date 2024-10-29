<script setup
        lang="ts"
>
// #region Imports
// Pinia
import { useDomainStore } from '@idaproject/core/store/domain';
import { useDeviceStore } from '@idaproject/core/store/device';

// Components
import TheHeader from '~/components/layout/TheHeader.vue';
import TheFooter from '~/components/layout/TheFooter.vue';
import TheUiKitNavigationEntry
    from '@idaproject/ui-kit/components/navigation/TheUiKitNavigationEntry.vue';

// Composables
import { useThirdPartyScripts } from '~/composables/common/useThirdPartyScripts';

// Utils
// Constants
import { scriptsList } from '@/assets/ts/constants/third-party-scripts'; // #endregion
// #endregion

// #region Data
const domainStore = useDomainStore();
const deviceStore = useDeviceStore();
const route = useRoute();
const siteDomain = computed(() => `https://${domainStore.domainUrl}`);

useHead({
    link: [
        {
            rel: 'canonical',
            href: `${siteDomain.value}${route.fullPath}`,
        },
    ],
    meta: [
        {
            hid: 'og:type',
            name: 'og:type',
            content: 'website',
        },
        {
            hid: 'og:url',
            name: 'og:url',
            content: `${siteDomain.value}${route.fullPath}`,
        },
    ],
    script: [deviceStore?.isRefYandex && scriptsList[0]],
});


onMounted(async () => {
    const {
        handleAddScripts,
    } = useThirdPartyScripts();

    const runtimeConfig = useRuntimeConfig();

    if (!runtimeConfig.public.IS_DEV && !route.query.nometrics) {
        if (deviceStore.isRefYandex) {
            const filteredScripts = [...scriptsList];
            filteredScripts.shift();
            handleAddScripts(filteredScripts);
        } else {
            handleAddScripts(scriptsList);
        }
    }

    await nextTick();

    deviceStore.isTouch = 'ontouchstart' in window ||
        navigator?.maxTouchPoints > 0 ||
        navigator?.msMaxTouchPoints > 0;
});
</script>

<template>
    <div
        id="app"
        :class="$style.DefaultLayout"
    >
        <TheHeader
            theme="light"
        />

        <main :class="$style.main">
            <slot />
        </main>

        <TheFooter />

        <TheUiKitNavigationEntry />

        <div id="yandex-captcha-container"></div>
    </div>
</template>

<style lang="scss"
       module
>
    .DefaultLayout {
        max-width: calc(100% - var(--lock-offset, 0));
    }

    .main {
        position: relative;
        min-height: stretch;
    }

    .styleDisplay {
        z-index: 999;

        @include respond-to(tablet) {
            display: none;
        }
    }
</style>

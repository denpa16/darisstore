<template>
    <div
        id="app"
        :class="$style.DefaultLayout"
    >
        <TheHeader />
        <main :class="$style.main">
            <Nuxt />
        </main>

        <TheModal :class="$style.modal" />
        <TheFooter />
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import TheHeader from '~/components/layout/TheHeader.vue';
import TheModal from '~/components/layout/TheModal.vue';
import TheFooter from '~/components/layout/TheFooter.vue';

// Components

export default {
    name: 'DefaultLayout',
    components: {
        TheHeader,
        TheModal,
        TheFooter,
    },

    head() {
        return {
            link: [
                {
                    rel: 'canonical',
                    href: `${this.siteDomain}${this.$route.path}`,
                },
            ],

            meta: [
                {
                    hid: 'og:url',
                    name: 'og:url',
                    content: `${this.siteDomain}${this.$route.path}`,
                },
                {
                    hid: 'twitter:url',
                    name: 'twitter:url',
                    content: `${this.siteDomain}${this.$route.path}`,
                },
            ],
        };
    },

    computed: {
        ...mapGetters({
            siteDomain: 'domain/getDomainAddress',
        }),
    },

    mounted() {
        this.changeActiveItem(this.$route.path);
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),
    },
};
</script>

<style lang="scss" module>
    .DefaultLayout {
        max-width: calc(100% - var(--lock-offset, 0));
    }

    .main {
        position: relative;
        min-height: 100dvh;

        @include respond-to(tablet) {
            padding-bottom: 3.2rem;
        }
    }

    .modal {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 1000;
    }

    :global {
        #page-top,
        #page-bottom {
            display: block;
            width: 100%;
            height: 1px;
            opacity: 0;
        }
    }
</style>

<template>
    <div :class="$style.IndexPage">
        <h1 class="visually-hidden">{{ title }}</h1>

        <IndexHero v-if="banners?.length" :slides="banners" />

        <IndexHeroBanner :class="$style.banner"/>

        <IndexBenefits id="advantages" />

        <OurCoaches
            id="coaches"
        />

        <IndexMission
            v-if="mainPageData?.about_gallery_images"
            id="about"
            :images="mainPageData.about_gallery_images"
        />

        <IndexGallery v-if="mainPageData?.gallery_images?.length" :images="mainPageData.gallery_images"/>

        <IndexNews v-if="news?.length" :news="news" />

        <IndexFaq v-if="mainPageData?.faqs?.length" :faqs="mainPageData.faqs"/>

        <IndexContacts id="contacts" />
    </div>
</template>

<script>
// Utils
import { scrollTo } from '~/assets/js/utils/common-utils';

// Components
import IndexHero from '~/components/pages/index/hero/IndexHero.vue';
import IndexBenefits from '~/components/pages/index/benefits/IndexBenefits.vue';
import IndexMission from '~/components/pages/index/mission/IndexMission.vue';
import IndexNews from '~/components/pages/index/news/IndexNews.vue';
import IndexContacts from '~/components/pages/index/contacts/IndexContacts.vue';
import IndexHeroBanner from '~/components/pages/index/hero/IndexHeroBanner.vue';
import IndexGallery from '~/components/pages/index/IndexGallery.vue';
import IndexFaq from '~/components/pages/index/IndexFaq.vue';
import OurCoaches from '~/components/pages/index/coaches/OurCoaches.vue';
import { mapState } from 'vuex';
import {
    EMAIL, MAIN_ADDRESS, ORG_NAME,
    PHONE_NUMBER,
    SITE_DESCRIPTION,
    SITE_IMAGE, SITE_PAGE,
    SITE_URL,
} from '~/assets/js/constants/index.js';

export default {
    name: 'IndexPage',

    components: {
        OurCoaches,
        IndexFaq,
        IndexGallery,
        IndexHeroBanner,
        IndexContacts,
        IndexNews,
        IndexMission,
        IndexBenefits,
        IndexHero,
    },

    async asyncData({ app, error }) {
        try {
            const [
                mainPageData,
                news,
            ] = await Promise.all([
                app.$axios.$get(app.$api.mainPage.data),
                app.$axios.$get(app.$api.publications.newsForMainPage),
            ]);

            return {
                mainPageData,
                news: news || [],
            };
        } catch (err) {
            console.warn('[IndexPage/asyncData] request failed: ', err);
            return error({ statusCode: 404 });
        }
    },

    data() {
        return {
            title: SITE_PAGE,
            mainPageData: [],
            news: [],
        };
    },

    head() {
        return {
            script: this.scriptsPrepared,
        };
    },

    computed: {
        ...mapState({
            menuItems: state => state.menu?.menuItems || [],
        }),

        banners() {
            return this.mainPageData?.banners || [];
        },

        scriptsPrepared() {
            return [
                {
                    type: 'application/ld+json',
                    json: {
                        '@context': 'https://schema.org',
                        '@type': 'SportsOrganization',
                        description: SITE_DESCRIPTION,
                        image: SITE_IMAGE,
                        url: SITE_URL,

                        sport: 'Kickboxing',
                        name: ORG_NAME,
                        email: EMAIL,
                        telephone: PHONE_NUMBER,
                        address: {
                            '@type': 'PostalAddress',
                            streetAddress: MAIN_ADDRESS,
                        },

                        contactPoint: [{
                            '@type': 'ContactPoint',
                            telephone: PHONE_NUMBER,
                            contactType: 'Customer Service',
                        }],
                    },
                },
            ];
        },
    },

    watch: {
        '$route.query'(newParams) {
            this.scrollToSection(newParams?.section);
        },
    },

    mounted() {
        const currentSection = this.$route?.query?.section;

        this.scrollToSection(currentSection);
    },

    methods: {
        scrollToSection(sectionId) {
            if (!sectionId) {
                return;
            }

            scrollTo(sectionId, this.$deviceIs.mobile ? 72 : 90);
        },
    },
};
</script>

<style lang="scss" module>
    .IndexPage {
        @include respond-to(mobile) {
            .banner {
                display: none;
            }
        }
    }
</style>

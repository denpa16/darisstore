<template>
    <div :class="$style.NewsDetail">
        <section :class="[$style.detail, 'container']">
            <div :class="$style.titleHeader">
                <div>
                    <h1
                        v-if="news?.title"
                        :class="$style.title"
                    >
                        {{ news.title }}
                    </h1>

                    <VTag
                        v-if="date"
                        :class="$style.date"
                        color="light"
                    >
                        {{ date }}
                    </VTag>
                </div>

                <VImage
                    v-if="news.image"
                    :class="$style.image"
                    :image="news.image"
                    :alt="news?.title"
                />
            </div>

            <div
                v-if="news?.description"
                v-html="news.description"
            />
        </section>

        <IndexNews
            v-if="similar"
            is-similar
            :news="similar"
        />
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

import IndexNews from '~/components/pages/index/news/IndexNews.vue';

export default {
    name: 'NewsDetail',
    components: { IndexNews },

    async asyncData({ app, error, params }) {
        try {
            const slug = params.slug;
            const [news, similar] = await Promise.all([
                app.$axios.$get(app.$api.publications.slug(slug)),
                app.$axios.$get(app.$api.publications.similar(slug)),
            ]);

            return {
                news: news || {},
                similar: similar || [],
            };
        } catch (err) {
            console.warn('[NewsPage/asyncData] request failed: ', err);
            return error({ statusCode: 404 });
        }
    },

    data() {
        return {
            news: {},
            similar: [],
        };
    },

    head() {
        return {
            title: this.metaTitle,

            meta: [
                {
                    hid: 'description',
                    name: 'description',
                    content: this.metaDescription,
                },
                {
                    hid: 'og:title',
                    name: 'og:title',
                    content: this.metaTitle,
                },
                {
                    hid: 'og:description',
                    name: 'og:description',
                    content: this.metaDescription,
                },
                {
                    hid: 'og:image',
                    name: 'og:image',
                    content: this.metaImage,
                },
                {
                    hid: 'twitter:title',
                    name: 'twitter:title',
                    content: this.metaTitle,
                },
                {
                    hid: 'twitter:description',
                    name: 'twitter:description',
                    content: this.metaDescription,
                },
                {
                    hid: 'twitter:image',
                    name: 'twitter:image',
                    content: this.metaImage,
                },
            ],
        };
    },

    computed: {
        ...mapGetters({
            siteDomain: 'domain/getDomainAddress',
        }),

        metaTitle() {
            return this.news.title;
        },

        metaDescription() {
            return this.news.description;
        },

        metaImage() {
            return this.news.image;
        },

        date() {
            if (!this.news?.publication_date) {
                return null;
            }
            return this.news.publication_date.split('-').reverse()
                .join('.');
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .NewsDetail {
        min-height: 100vh;
        margin-bottom: 10rem;

        @include respond-to(mobile) {
            margin-bottom: 2.4rem;
        }
    }

    .detail {
        padding-top: 4rem;
        padding-bottom: 4rem;
    }

    .titleHeader {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 4rem;
        margin-bottom: 5.6rem;

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
            gap: 2.4rem;
            margin-bottom: 4rem;
        }
    }

    .title {
        @include text(h3);

        @include respond-to(mobile) {
            @include text(h4);
        }
    }

    .date {
        margin: 2.4rem 0;

        @include respond-to(mobile) {
            margin: 1.6rem 0 0;
        }
    }

    .image {
        overflow: hidden;
        width: 100%;
        max-height: 40rem;
        border-radius: 1.6rem;
    }

    .description {
        //
    }
</style>

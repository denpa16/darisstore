<template>
    <div :class="[$style.NewsPage, 'container']">
        <h1 :class="$style.title">Новости</h1>

        <div :class="$style.list">
            <IndexNewsCard
                v-for="item in news"
                :key="item.slug"
                :item="item"
            />
        </div>

        <transition
            name="fade-fast"
            mode="out-in"
        >
            <div
                v-if="pageInfo.hasNext"
                :class="$style.btnMore"
            >
                <VButton
                    size="small"
                    @click="loadMore"
                >
                    Загрузить еще
                </VButton>
            </div>
        </transition>
    </div>
</template>

<script>
import IndexNewsCard from '~/components/pages/index/news/IndexNewsCard.vue';

export default {
    name: 'NewsPage',
    components: { IndexNewsCard },

    async asyncData({ app, error }) {
        try {
            const news = await app.$axios.$get(app.$api.publications.list());

            return {
                news: news?.results || [],
                pageInfo: {
                    limit: 16,
                    offset: 0,
                    hasNext: Boolean(news?.next),
                },
            };
        } catch (err) {
            console.warn('[NewsPage/asyncData] request failed: ', err);
            return error({ statusCode: 404 });
        }
    },

    data() {
        return {
            news: [],
            pageInfo: {
                limit: 16,
                offset: 0,
                hasNext: true,
            },
        };
    },

    head() {
        return {
            title: 'Новости | СК ШАГ',

            meta: [
                {
                    hid: 'og:title',
                    name: 'og:title',
                    content: 'Новости | СК ШАГ',
                },
                {
                    hid: 'twitter:title',
                    name: 'twitter:title',
                    content: 'Новости | СК ШАГ',
                },
            ],
        };
    },

    methods: {
        async loadMore() {
            try {
                this.pageInfo.offset += this.pageInfo.limit;
                const res = await this.$axios.$get(this.$api.publications.list(this.pageInfo.limit, this.pageInfo.offset));

                this.news = this.news.concat(res?.results);
                this.pageInfo.hasNext = Boolean(res.next);
            } catch (err) {
                console.warn('[NewsPage/asyncData] request failed: ', err);
            }
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .NewsPage {
        min-height: 100vh;
        padding-bottom: 10rem;

        @include respond-to(mobile) {
            padding-bottom: 2.4rem;
        }
    }

    .title {
        @include text(h2);

        margin: 4rem 0;
        text-transform: uppercase;

        @include respond-to(mobile) {
            @include text(h4);

            margin-bottom: 3.2rem;
        }
    }

    .list {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3.2rem;

        @include respond-to(tablet) {
            grid-template-columns: repeat(2, 1fr);
        }

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
        }
    }

    .btnMore {
        display: flex;
        justify-content: center;
        margin-top: 4rem;

        @include respond-to(mobile) {
            margin-top: 2.4rem;
        }
    }
</style>

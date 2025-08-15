<template>
    <VSection :class="$style.news" :title="title">
        <template #title-aside>
            <VButton
                v-if="!isSimilar"
                :class="$style.btn"
                size="medium"
                @click="handleClick"
            >
                Все новости
            </VButton>
        </template>

        <div :class="$style.wrapper">
            <div :class="$style.list">
                <IndexNewsCard
                    v-for="item in news"
                    :key="item.slug"
                    :item="item"
                />
            </div>

            <VButton
                v-if="!isSimilar"
                :class="$style.allNewsBtn"
                size="medium"
                @click="handleClick"
            >
                Все новости
            </VButton>
        </div>

        <VImage :class="$style.bg" image="/images/index/news/bg.png"/>
        <VImage :class="[$style.bg, $style._mobile]" image="/images/index/news/bg-mobile.png"/>
    </VSection>
</template>

<script>
import IndexNewsCard from './IndexNewsCard.vue';
import { mapActions } from 'vuex';

export default {
    name: 'IndexNews',
    components: {
        IndexNewsCard,
    },

    props: {
        news: {
            type: Array,
            default: () => [],
        },

        isSimilar: {
            type: Boolean,
            default: false,
        },
    },

    computed: {
        title() {
            return this.isSimilar ? 'Похожие новости' : 'Новости';
        },
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),

        handleClick() {
            this.$router.push({
                path: '/blog/news',
            });
            this.changeActiveItem('/blog/news');
        },
    },
};
</script>

<style module lang="scss">
    .news {
        position: relative;

        .btn {
            position: relative;
            z-index: 5;

            @include respond-to(mobile) {
                display: none;
            }
        }

        .allNewsBtn {
            display: none;

            @include respond-to(mobile) {
                display: flex;
                width: 100%;
                margin-top: 3.2rem;
            }
        }
    }

    .bg {
        position: absolute;
        bottom: 0;
        left: 50%;
        z-index: 1;
        width: 100%;
        transform: translateX(-50%);

        &._mobile {
            display: none;
        }

        @include respond-to(mobile) {
            display: none;

            &._mobile {
                top: 50%;
                bottom: auto;
                display: block;
                transform: translate(-50%, -50%);
            }
        }
    }

    .wrapper {
        position: relative;
        z-index: 2;
    }

    .list {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;

        @include respond-to(tablet) {
            grid-template-columns: repeat(2, 1fr);
            gap: 2.4rem;
        }

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
            gap: 2.4rem;
        }
    }

    .allNews {
        display: flex;
        justify-content: center;
        margin-top: 4rem;
    }
</style>

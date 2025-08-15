<template>
    <section :class="[$style.IndexMission, 'container']">
        <div :class="$style.content">
            <h2 :class="$style.title" v-html="content.title"/>

            <div>
                <div :class="$style.description" v-html="content.description"/>

                <div :class="$style.tags">
                    <VTag
                        v-for="(tag, ind) in content.tags"
                        :key="`tag_${ind}`"
                        :class="$style.date"
                        color="light"
                    >
                        {{ tag }}
                    </VTag>
                </div>
            </div>
        </div>

        <transition name="fade-fast" mode="out-in">
            <VSlider
                :key="`slider_${$deviceIs.device}`"
                :class="$style.gallery"
                :slides="images"
                :pagination="!$deviceIs.pc"
                :counter="$deviceIs.pc"
                :navigation="$deviceIs.pc"
                size-buttons="medium"
                disabled-shadow
            />
        </transition>

        <IndexMissionCards :class="$style.cards"/>
    </section>
</template>

<script>
import { intersectionMixin } from '~/mixins/intersectionMixin.js';
import { mapActions } from 'vuex';
import IndexMissionCards from '~/components/pages/index/mission/IndexMissionCards.vue';

export default {
    name: 'IndexMission',

    components: { IndexMissionCards },

    mixins: [intersectionMixin],

    props: {
        images: {
            type: Array,
            default: () => [],
        },
    },

    data() {
        return {
            content: {
                title: `<span class="${this.$style.highlight}">Шаг</span> - это больше, чем&nbsp;тренировки`,
                description: 'Главная цель клуба&nbsp;&mdash; подготовка членов сборных команд Чувашской Республики, Московской области и России по&nbsp;кикбокингу, а&nbsp;также предоставление возможности вести здоровый образ жизни.',
                tags: ['Кикбоксинг', 'Бокс', 'Групповые и персональные тренировки', 'Для новичков и профессионалов', 'Повышение мастерства'],
            },
        };
    },

    watch: {
        isVisible() {
            if (this.isVisible) {
                history.replaceState({}, '', `#${this.$el?.id}`);
                this.changeActiveItem(this.$el?.id);
            }
        },
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),
    },
};
</script>

<style module lang="scss">
    .IndexMission {
        display: grid;
        grid-template-columns: 1fr 62.6rem;
        gap: 4rem;
        padding-top: 6.4rem;
        padding-bottom: 6.4rem;

        @include respond-to(tablet) {
            grid-template-columns: 1fr;
            gap: 4rem;
            padding-top: 3.2rem;
            padding-bottom: 3.2rem;
        }
    }

    .content {
        display: flex;
        flex-direction: column;
        gap: 3.2rem;

        @include respond-to(tablet) {
            gap: 2rem;
        }

        @include respond-to(mobile) {
            overflow: hidden;
        }
    }

    .title {
        @include text(h2);

        text-transform: uppercase;
        color: $base-500;

        @include respond-to(tablet) {
            @include text(h4);
        }
    }

    .highlight {
        color: $base-900;
    }

    .description {
        @include text(r14);

        margin: 0;
        color: $base-500;
    }

    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: .8rem;
        margin-top: 1.6rem;
    }

    .gallery {
        overflow: hidden;
        grid-column: 2/3;
        grid-row: 1/3;
        border-radius: 1.2rem;

        @include respond-to(tablet) {
            grid-column: auto;
            grid-row: auto;
            height: 37.5rem;
        }
    }

    .cards {
        margin-top: auto;
    }
</style>

<template>
    <div :class="$style.IndexHeroFeatures">
        <div :class="$style._mobile">
            <div
                ref="slider"
                :class="[$style.swiper, 'swiper']"
            >
                <div class="swiper-wrapper">
                    <div
                        v-for="(feature, index) in dividedList.list"
                        :key="index"
                        :class="[$style.item, 'swiper-slide']"
                    >
                        <div :class="$style.content">
                            <h3
                                v-if="feature.title"
                                :class="$style.title"
                            >
                                {{ feature.title }}
                            </h3>
                            <div
                                v-if="feature.description"
                                :class="$style.description"
                                v-html="feature.description"
                            />
                        </div>

                        <VImage
                            v-if="feature.image"
                            :class="$style.image"
                            :image="feature.image"
                            :alt="feature.title"
                            :width="450"
                            :height="200"
                        />

                        <VIconButton
                            v-if="feature?.hasBtn"
                            :class="$style.btn"
                            color="secondary"
                            size="small"
                            icon="arrow-right"
                            @click="handleRequest"
                        />
                    </div>
                </div>

                <div :class="[$style.pagination, 'pagination']"/>
            </div>

            <div :class="[$style.item, $style._single, $style._last]">
                <div :class="$style.content">
                    <h3
                        v-if="dividedList.item.title"
                        :class="$style.title"
                    >
                        {{ dividedList.item.title }}
                    </h3>
                    <div
                        v-if="dividedList.item.description"
                        :class="$style.description"
                        v-html="dividedList.item.description"
                    />
                </div>

                <VImage
                    v-if="dividedList.item.image"
                    :class="$style.image"
                    :image="dividedList.item.image"
                    :alt="dividedList.item.title"
                    :width="450"
                    :height="200"
                />

                <VIconButton
                    v-if="dividedList.item?.hasBtn"
                    :class="$style.btn"
                    color="secondary"
                    size="small"
                    icon="arrow-right"
                    @click="handleRequest"
                />
            </div>
        </div>
        <ul :class="$style.list">
            <li
                v-for="(feature, index) in features"
                :key="index"
                :class="[$style.item, {[$style._last]: index === features.length - 1}]"
            >
                <div :class="$style.content">
                    <h3
                        v-if="feature.title"
                        :class="$style.title"
                    >
                        {{ feature.title }}
                    </h3>
                    <div
                        v-if="feature.description"
                        :class="$style.description"
                        v-html="feature.description"
                    />
                </div>

                <VImage
                    v-if="feature.image"
                    :class="$style.image"
                    :image="feature.image"
                    :alt="feature.title"
                    :contain="index !== features.length - 1"
                    :width="450"
                    :height="200"
                />

                <VIconButton
                    v-if="feature?.hasBtn"
                    :class="$style.btn"
                    color="secondary"
                    size="large"
                    icon="arrow-right"
                    @click="handleRequest"
                />
            </li>
        </ul>
    </div>
</template>

<script>
import { lazyLoadSlider } from '~/mixins/lazyLoadSlider.js';

export default {
    name: 'IndexHeroFeatures',

    mixins: [lazyLoadSlider],

    data() {
        return {
            slider: null,
            features: [
                {
                    title: 'Эффективность',
                    description: 'Один из самых эффективных видов единоборств',
                    image: '/images/index/hero/features/image1.png',
                },
                {
                    title: 'Универсальность',
                    description: 'Создан на стыке двух легендарных видов единоборств: бокса и карате',
                    image: '/images/index/hero/features/image2.png',
                },
                {
                    title: 'Купить абонемент',
                    image: '/images/index/hero/features/image3.png',
                    hasBtn: true,
                },
            ],
        };
    },

    computed: {
        dividedList() {
            return {
                list: this.features.slice(0, 2),
                item: this.features.slice(-1)[0],
            };
        },
    },

    mounted() {
        this.$nextTick(() => {
            this.handleInitSlider();
        });
    },

    beforeDestroy() {
        if (this.slider) {
            this.slider.destroy();
        }
    },

    methods: {
        handleInitSlider() {
            if (!this.$refs.slider) {
                this.handleInitLazyLoad(null);
                return;
            }

            const options = {
                modules: [
                    this.$swiperModules.Pagination,
                ],

                pagination: {
                    el: '.pagination',
                    bulletClass: 'pagination-bullet',
                    bulletActiveClass: 'pagination-bullet-active',
                },

                slidesPerView: 1.25,
                spaceBetween: 12,
                observer: true,
                speed: 400,

                ...this.options,
            };

            this.slider = new this.$swiper(this.$refs.slider, options);
        },

        handleRequest() {
            this.$modal.open(() => import('@/components/layout/modals/FormModal.vue'), {
                position: 'right',
            });
        },
    },
};
</script>

<style
    module
    lang="scss"
>
    .IndexHeroFeatures {
        overflow: hidden;
        margin-right: -1.6rem;
        padding-right: 1.6rem;
    }

    ._mobile {
        display: none;

        @include respond-to(mobile) {
            display: flex;
            flex-direction: column;
            gap: 1.6rem;
        }
    }

    .swiper {
        overflow: hidden;
        width: calc(100% + 1.6rem);
        margin-right: -1.6rem;
    }

    .list {
        display: grid;
        grid-template-rows: repeat(3, 1fr);
        gap: 1.2rem;
        height: 100%;

        @include respond-to(tablet) {
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: 1fr;
        }

        @include respond-to(mobile) {
            display: none;
        }
    }

    .item {
        position: relative;
        overflow: hidden;
        display: grid;
        grid-template-columns: 24rem 1fr;
        border-radius: 1.2rem;
        background: $base-150;
        transition: box-shadow $default-transition;
        cursor: pointer;
        user-select: none;

        @include hover {
            box-shadow: $box-shadow-default;
        }

        &._last {
            grid-template-columns: 1fr 5.6rem;
            background: $primary-500;

            .title {
                color: $white;
            }

            .image {
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
                width: 100%;
                height: 100%;
            }
        }

        @include respond-to(tablet) {
            width: 100%;
        }

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
            height: 17.2rem;

            &._single {
                .content {
                    padding: 2.4rem;
                }
            }
        }
    }

    .content {
        position: relative;
        z-index: 2;
        padding: 2.4rem;

        @include respond-to(mobile) {
            padding: 2rem;
        }
    }

    .title {
        @include text(h5);

        margin-bottom: 1.2rem;
        text-transform: uppercase;
        color: $base-700;
    }

    .description {
        @include text(r14);

        color: $base-700;
    }

    .image {
        overflow: hidden;
        align-self: end;
        justify-self: end;
        width: fit-content;
        height: 100%;

        @include respond-to(tablet) {
            width: 7.2rem;
            height: 7.2rem;
        }

        @include respond-to(mobile) {
            position: absolute;
            right: 0;
            bottom: 0;
            width: 10.2rem;
            height: 9.2rem;
        }
    }

    .btn {
        position: relative;
        z-index: 2;
        align-self: end;
        justify-self: end;
        margin: 2.4rem;
    }

    .pagination {
        margin-top: 1.2rem;
    }
</style>

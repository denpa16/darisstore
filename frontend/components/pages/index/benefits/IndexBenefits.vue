<template>
    <VSection
        v-bind="$attrs"
        :class="$style.IndexBenefits"
        title="С нами вы получите"
    >
        <div :class="$style.grid">
            <article :class="[$style.card, $style._open]">
                <VImageSrcSet
                    :class="$style.cardImage"
                    image="/images/index/benefits/image.png"
                    alt="Сообщество и поддержка"
                />
                <div :class="$style.cardContent">
                    <h4 :class="$style.cardTitle">
                        Сообщество и поддержка
                    </h4>
                    <p :class="$style.cardDescription">
                        Спортивный клуб создает дружелюбную и&nbsp;поддерживающую атмосферу, где
                        участники могут обмениваться опытом, поддерживать друг друга и
                        мотивировать на&nbsp;достижения.
                    </p>
                </div>
            </article>

            <article :class="[$style.card, $style._small, $style._smallCenter]">
                <div :class="$style.avatars" aria-hidden="true">
                    <div
                        v-for="(trainer, index) in trainers"
                        :key="index"
                        :class="$style.avatar"
                    >
                        <VImageSrcSet
                            :class="$style.avatarImage"
                            :image="trainer.image"
                            :alt="trainer.alt"
                        />
                    </div>
                </div>
                <h4 :class="$style.cardTitle">Опытные тренеры</h4>
            </article>

            <article :class="[$style.card, $style._small]">
                <VImageSrcSet
                    :class="$style.cardBackground"
                    image="/images/index/benefits/background.png"
                    alt="Командные соревнования"
                />
                <h4 :class="$style.cardTitle">Командные соревнования</h4>
            </article>

            <article
                ref="donutRef"
                :class="[$style.card, $style._large]"
                aria-labelledby="benefit-approach"
            >
                <div :class="$style.cardContent">
                    <h4 :class="$style.cardTitle">Индивидуальный подход</h4>

                    <div :class="$style.percentageCircle">
                        <VDonut
                            :size="203"
                            :value="donutValue"
                            :start-angle="-120"
                            :stroke-width="15"
                            :animation-duration="donutAnimationDuration"
                        />

                        <VCounter
                            :class="$style.percentageText"
                            :value="donutValue"
                            :duration="donutAnimationDuration"
                            append="%"
                        />
                    </div>
                    <p :class="$style.cardDescription">
                        участников отмечают значительное улучшение своих результатов
                        в течение первых трех месяцев тренировок
                    </p>
                </div>
            </article>
        </div>

        <VImage :class="$style.bg" image="/images/index/benefits/bg.png"/>
        <VImage :class="[$style.bg, $style._mobile]" image="/images/index/benefits/bg-mobile.png"/>
    </VSection>
</template>

<script>
import { intersectionMixin } from '~/mixins/intersectionMixin.js';
import { mapActions } from 'vuex';

export default {
    name: 'IndexBenefits',

    mixins: [intersectionMixin],

    data() {
        return {
            donutValue: 0,
            targetDonutValue: 92,
            donutAnimationDuration: 3000,

            trainers: [
                {
                    image: '/images/index/benefits/trainer-1.png',
                    alt: 'Тренер 1',
                },
                {
                    image: '/images/index/benefits/trainer-2.png',
                    alt: 'Тренер 2',
                },
                {
                    image: '/images/index/benefits/trainer-3.png',
                    alt: 'Тренер 3',
                },
                {
                    image: '/images/index/benefits/trainer-4.png',
                    alt: 'Тренер 4',
                },
            ],
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

    mounted() {
        setTimeout(this.initAnimation, 0);
    },

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),

        initAnimation() {
            this.$gsap.timeline({
                scrollTrigger: {
                    trigger: this.$refs.donutRef,
                    start: 'center bottom',

                    onEnter: self => {
                        this.donutValue = this.targetDonutValue;
                        self.disable();
                    },
                },
            });
        },
    },
};
</script>

<style module lang="scss">
    .IndexBenefits {
        position: relative;
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

    .grid {
        position: relative;
        z-index: 2;
        display: grid;
        grid-template:
            "community trainers approach" 1fr
            "community competition approach" 1fr / 1.56fr 1fr 1.56fr;
        gap: 2rem;
        width: 100%;

        @include respond-to(tablet) {
            grid-template:
                "community"
                "trainers"
                "competition"
                "approach"
                / 1fr;
            gap: 2.4rem;
        }
    }

    .card {
        position: relative;
        overflow: hidden;
        padding: 2.4rem;
        border-radius: 1.2rem;
        background-color: $base-150;
        text-align: center;

        &._open {
            grid-area: community;
            padding: initial;
            text-align: initial;

            .cardContent {
                padding: 2.4rem;

                @include respond-to(tablet) {
                    padding: 2rem;
                }
            }

            .cardImage {
                width: 100%;
                aspect-ratio: 478 / 364;
                border-radius: 1.2rem;

                @include respond-to(tablet) {
                    aspect-ratio: 343 / 200;
                }
            }

            .cardTitle {
                margin-bottom: 1.2rem;
            }

            .cardDescription {
                @include respond-to(tablet) {
                    line-height: 2rem;
                }
            }
        }

        &._small {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2.4rem;
            min-height: 20rem;

            &._smallCenter {
                justify-content: center;
            }

            .cardTitle {
                width: 80%;

                @include respond-to(tablet) {
                    width: 100%;
                }
            }
        }

        &._large {
            grid-area: approach;
            padding-top: 4rem;
            padding-bottom: 4rem;

            @include respond-to(tablet) {
                padding: 2.4rem;
            }

            .cardContent {
                align-items: center;
                justify-content: space-between;
                gap: 3.2rem;
                height: 100%;
            }

            .cardTitle {
                width: 60%;

                @include respond-to(tablet) {
                    width: 100%;
                }
            }

            .cardDescription {
                width: 80%;

                @include respond-to(tablet) {
                    @include text(r16);

                    width: 100%;
                    line-height: 1.8rem;
                }
            }
        }
    }

    .cardContent {
        display: flex;
        flex-direction: column;
    }

    .cardTitle {
        @include text(h4);

        text-transform: uppercase;
        color: $base-700;

        @include respond-to(tablet) {
            @include text(h5);
        }
    }

    .cardImage {
        overflow: hidden;
        display: block;
    }

    .cardBackground {
        position: absolute;
        inset: 0;
    }

    .cardDescription {
        @include text(r16);

        color: $base-500;

        @include respond-to(tablet) {
            @include text(r14);
        }
    }

    .avatars {
        display: flex;
    }

    .avatar {
        position: relative;
        overflow: hidden;
        width: 7.2rem;
        height: 7.2rem;
        border-radius: 50%;
        border: .8rem solid $base-150;

        &:not(:first-child) {
            margin-left: -1.6rem;
        }
    }

    .avatarImage {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 130%;
        height: 130%;
        object-fit: cover;
        transform: translate(-50%, -50%);
    }

    .percentageCircle {
        position: relative;
        width: 20.3rem;
        height: 20.3rem;
    }

    .percentageText {
        @include text(h2);

        position: absolute;
        top: 50%;
        left: 50%;
        color: $base-700;
        transform: translate(-50%, -50%);
    }
</style>

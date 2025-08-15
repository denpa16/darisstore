<template>
    <div
        :class="$style.CoachCard"
        @click="handleClick"
    >
        <div :class="$style.imageWrapper">
            <VImage
                v-if="coach.image"
                :class="$style.image"
                :image="coach.image"
                :width="500"
                :height="550"
            />
        </div>
        <div>
            <h3
                :class="$style.fio"
                v-html="coach.fio"
            />
            <div
                :class="$style.position"
                v-html="coach.position"
            />
            <a
                :href="coach.branch.value"
                target="_blank"
                :class="$style.link"
            >
                <VIcon
                    size="xsmall"
                    name="map-pin"
                />
                {{ coach.branch.label }}
            </a>
            <div :class="$style.tags">
                <VTag
                    v-for="tag in coach.tags"
                    :key="`tag_${tag}`"
                    color="light"
                >
                    {{ tag }}
                </VTag>
            </div>
        </div>

        <div
            ref="content"
            :class="$style.content"
        >
            <div :class="$style.times">
                <p>Расписание тренировок:</p>
                <div v-html="coach.times" />
            </div>
        </div>

        <div
            :key="`btn_${isOpen}`"
            :class="[$style.dropdown, {[$style._open]: isOpen}]"
        >
            <span :class="$style._front">Подробнее</span>
            <span :class="$style._back">Свернуть</span>
            <VIcon :class="$style.arrow" name="arrow-down" />
        </div>

        <VButton
            :class="$style.btn"
            size="medium"
            @click="handleRequest"
        >
            Записаться на тренировку
        </VButton>
    </div>
</template>

<script>
import VImage from '~/components/ui/images/VImage.vue';
import VButton from '~/components/ui/button/VButton.vue';
import { gsap } from 'gsap';
import VIcon from '~/components/ui/icon/VIcon.vue';

export default {
    name: 'CoachCard',

    components: { VIcon, VButton, VImage },

    props: {
        coach: {
            type: Object,
            default: () => ({}),
        },
    },

    data() {
        return {
            isOpen: false,
        };
    },

    methods: {
        handleRequest() {
            if (this.coach.tg) {
                const link = `https://t.me/${this.coach.tg}?&text=Здравствуйте! Хочу записаться на тренировку в спортивный клуб "Шаг". Пожалуйста, свяжитесь со мной для уточнения деталей. Спасибо!`;
                window.open(link, '_blank');
            } else {
                this.$modal.open(() => import('@/components/layout/modals/FormModal.vue'), {
                    position: 'right',
                });
            }
        },

        handleClick() {
            this.animate();
        },

        animate() {
            if (!this.$refs.content) {
                return;
            }

            this.isOpen = !this.isOpen;

            if (this.isOpen) {
                gsap.to(this.$refs.content, {
                    duration: .4,
                    height: 'auto',
                });
            } else {
                gsap.to(this.$refs.content, {
                    duration: .4,
                    height: 0,
                });
            }
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .CoachCard {
        display: flex;
        flex-direction: column;
        height: 64rem;
        user-select: none;

        @include hover {
            .image {
                img {
                    transform: scale(1.1);
                }
            }
        }

        @include respond-to(mobile) {
            height: 56rem;
        }
    }

    .imageWrapper {
        position: relative;
        overflow: hidden;
        width: 100%;
        height: 100%;
        max-height: 33.8rem;
        border-radius: 1.2rem;
    }

    .image {
        position: absolute;
        width: 100%;

        img {
            transition: $default-transition;
        }
    }

    .fio {
        @include text(h5);

        margin-top: 1.6rem;
        font-weight: 700;
    }

    .position {
        @include text(m16);

        font-weight: 700;
        color: $base-500;
    }

    .content {
        overflow: hidden;
        flex-shrink: 0;
        height: 0;
    }

    .link {
        @include text(m12);

        display: flex;
        align-items: center;
        gap: .8rem;
        margin-top: 1.6rem;
        font-weight: 700;
    }

    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: .8rem;
        margin-top: 1.2rem;
    }

    .times {
        @include text(r14);

        margin-top: 1.6rem;
        color: $base-500;

        p {
            margin-bottom: 1rem;
        }

        div {
            font-weight: 400;
        }
    }

    .dropdown {
        position: relative;
        display: flex;
        align-items: center;
        gap: .8rem;
        padding: 1.6rem 0;
        transition: $default-transition;
        cursor: pointer;

        & ._front {
            //
        }

        & ._back {
            position: absolute;
            opacity: 0;
        }

        &._open {
            transform: rotateX(-180deg);
            transition: $default-transition;

            & ._front {
                opacity: 0;
                transition: $default-transition;
            }

            & ._back {
                opacity: 1;
                transform: rotateX(-180deg);
                transition: $default-transition;
            }
        }
    }

    .btn {
        flex-shrink: 0;
        margin-top: auto;
    }
</style>

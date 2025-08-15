<template>
    <VSection :class="$style.IndexContacts" title="Контакты">
        <div :class="$style.wrapper">
            <VImageSrcSet :class="$style.image" image="/images/index/contacts/image.png" />

            <div :class="$style.content">
                <div :class="$style.contentWrapper">
                    <div
                        v-for="(column, columnIndex) in content"
                        :key="columnIndex"
                        :class="$style.column"
                    >
                        <div :class="$style.columnTitle">{{ column.title }}</div>
                        <VInfoOption
                            v-for="(option, optionIndex) in column.options"
                            :key="optionIndex"
                            :class="$style.option"
                            :name="option.name"
                            :content-items="option.contentItems"
                        />
                    </div>
                </div>
            </div>
        </div>
    </VSection>
</template>

<script>
import { EMAIL, PHONE_NUMBER } from '~/assets/js/constants/index.js';
import { intersectionMixin } from '~/mixins/intersectionMixin.js';
import { mapActions } from 'vuex';
import { branches } from '~/assets/js/constants/branches.js';

export default {
    name: 'IndexContacts',

    mixins: [intersectionMixin],

    data() {
        return {
            phone: PHONE_NUMBER,
            email: EMAIL,

            content: [
                {
                    title: 'Залы',
                    options: [
                        {
                            name: branches.main.shortLabel,
                            contentItems: [
                                {
                                    text: branches.main.address,
                                    href: branches.main.value,
                                },
                                { text: 'Пт-Сб, 08:00-22:00' },
                            ],
                        },
                        {
                            name: branches.branch1.shortLabel,
                            contentItems: [
                                {
                                    text: branches.branch1.address,
                                    href: branches.branch1.value,
                                },
                                { text: 'Пт-Сб, 10:00-20:00' },
                            ],
                        },
                        {
                            name: branches.branch2.shortLabel,
                            contentItems: [
                                {
                                    text: branches.branch2.address,
                                    href: branches.branch2.value,
                                },
                                { text: 'Пт-Сб, 10:00-20:00' },
                            ],
                        },
                        {
                            name: branches.branch3.shortLabel,
                            contentItems: [
                                {
                                    text: branches.branch2.address,
                                    href: branches.branch2.value,
                                },
                                { text: 'Пт-Сб, 10:00-20:00' },
                            ],
                        },
                    ],
                },
                {
                    title: 'Контакты',
                    options: [
                        {
                            name: 'Номер телефона',
                            contentItems: [
                                { text: PHONE_NUMBER, href: PHONE_NUMBER, isPhone: true },
                            ],
                        },
                        {
                            name: 'Почта',
                            contentItems: [
                                { text: EMAIL, href: EMAIL, isEmail: true },
                            ],
                        },
                    ],
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

    methods: {
        ...mapActions({
            changeActiveItem: 'menu/changeActiveItem',
        }),
    },
};
</script>

<style lang="scss" module>
    .IndexContacts {
        //
    }

    .wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;

        @include respond-to(tablet) {
            grid-template-columns: 1fr;
        }
    }

    .image {
        overflow: hidden;
        width: 100%;
        aspect-ratio: 635 / 500;
        border-radius: $radius-lg;

        @include respond-to(tablet) {
            aspect-ratio: 343 / 270;
            border-radius: $radius-md;
        }
    }

    .content {
        display: flex;
        align-items: center;

        @include respond-to(tablet) {
            display: block;
        }
    }

    .contentWrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        width: 100%;

        @include respond-to(tablet) {
            grid-template-columns: 1fr;
        }
    }

    .columnTitle {
        @include text(s24);

        margin-bottom: 2.4rem;
        padding-bottom: 2.4rem;
        border-bottom: .1rem solid $base-300;

        @include respond-to(tablet) {
            @include text(s20);

            margin-bottom: 1.6rem;
            padding-bottom: 1.2rem;
        }
    }

    .option {
        &:not(:last-child) {
            margin-bottom: 3.2rem;

            @include respond-to(tablet) {
                margin-bottom: 2rem;
            }
        }
    }
</style>

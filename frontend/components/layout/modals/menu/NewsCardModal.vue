<template>
    <div :class="$style.IndexNewsModal">
        <div :class="$style.wrapper">
            <VIconButton
                :class="$style.button"
                icon="close"
                color="primary"
                @click="$emit('close')"
            />

            <div :class="$style.content">
                <VTag color="light">{{ formattedDate }}</VTag>
                <h3 :class="$style.title">{{ item.title }}</h3>
                <div :class="$style.description" v-html="item.description"></div>
            </div>

            <VImageSrcSet
                v-if="item.image"
                :class="$style.image"
                :image="item.image"
                :alt="item.title"
            />
        </div>
    </div>
</template>

<script>
import { formatDateTime } from '~/assets/js/utils/date-time-utils.js';

export default {
    name: 'IndexNewsModal',

    props: {
        item: {
            type: Object,
            default: () => ({}),
        },
    },

    computed: {
        formattedDate() {
            return formatDateTime(this.item?.publication_date, '$d.$m.$y');
        },
    },
};
</script>

<style lang="scss" module>
    .IndexNewsModal {
        padding: 4.8rem 3.2rem 3.2rem;

        @include respond-to(tablet) {
            padding: 4rem 2.4rem 2.4rem;
        }
    }

    .wrapper {
        position: relative;
    }

    .button {
        position: absolute;
        top: -1.6rem;
        right: 0;
    }

    .content {
        margin-bottom: 2rem;
    }

    .title {
        @include text(h4);

        width: 90%;
        margin-top: 2.4rem;
        color: $base-900;

        @include respond-to(tablet) {
            @include text(h5);

            margin-top: 1.6rem;
        }
    }

    .description {
        @include text(r16);

        margin-top: 1.6rem;
        color: $base-500;

        @include respond-to(tablet) {
            @include text(r14);

            margin-top: 1.2rem;
            line-height: 2rem;
        }

        p {
            margin: 0 0 1.2rem 0;

            @include respond-to(tablet) {
                margin-bottom: .8rem;
            }
        }
    }

    .image {
        overflow: hidden;
        width: 100%;
        height: auto;
        margin-top: 3.2rem;
        border-radius: $radius-lg;
        transition: transform $default-transition;
    }
</style>

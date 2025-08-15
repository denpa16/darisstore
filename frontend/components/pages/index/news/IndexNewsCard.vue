<template>
    <div :class="$style.IndexNewsCard">
        <div>
            <div :class="$style.imageWrapper">
                <VImageSrcSet
                    v-if="item.image"
                    :class="$style.image"
                    :image="item.image"
                    :alt="item.title"
                />
                <VTag
                    v-if="formattedDate"
                    :class="$style.date"
                    color="light"
                >
                    {{ formattedDate }}
                </VTag>
            </div>
            <div :class="$style.content">
                <h3 :class="$style.title">{{ item.title }}</h3>
                <div
                    :class="$style.description"
                    v-html="item.description"
                >
                </div>
            </div>
        </div>
        <a
            :class="$style.link"
            :href="`/blog/news/${item.slug}`"
            target="_blank"
        />
    </div>
</template>

<script>
import { formatDateTime } from '~/assets/js/utils/date-time-utils.js';

export default {
    name: 'IndexNewsCard',
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

<style
    module
    lang="scss"
>
    .IndexNewsCard {
        position: relative;
        border-radius: 1.2rem;
        background: $white;
        cursor: pointer;
        user-select: none;

        @include hover {
            .image {
                transform: scale(1.1);
            }
        }
    }

    .link {
        position: absolute;
        inset: 0;
        z-index: 5;
    }

    .imageWrapper {
        position: relative;
        overflow: hidden;
        border-radius: 1.2rem;
        aspect-ratio: 312 / 208;

        @include respond-to(tablet) {
            aspect-ratio: 343 / 208;
        }
    }

    .image {
        width: 100%;
        height: 100%;
        transition: transform $default-transition;
    }

    .date {
        position: absolute;
        top: 1.2rem;
        left: 1.2rem;
    }

    .content {
        padding: 1.6rem;
    }

    .title {
        @include text(m16);
        @include text-clamp(2);

        color: $base-900;
    }

    .description {
        @include text(r14);
        @include text-clamp(2);

        margin-top: 1.2rem;
        color: $base-500;
    }
</style>

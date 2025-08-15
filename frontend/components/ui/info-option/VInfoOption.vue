<template>
    <component :is="tag" :class="$style.VInfoOption">
        <span :class="$style.name" v-html="name"></span>
        <span :class="$style.content">
            <VLink
                v-for="(item, index) in contentItems"
                :key="index"
                :class="$style.item"
                :href="item.href"
                :is-email="item.isEmail"
                :is-phone="item.isPhone"
                default-inline
                v-html="item.text"
            ></VLink>
        </span>
    </component>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'VInfoOption',

    props: {
        tag: {
            type: String,
            default: 'div',
        },

        name: {
            type: String,
            default: '',
        },

        contentItems: {
            type: Array,
            default: () => [],
        },
    },
});
</script>

<style lang="scss" module>
    .VInfoOption {
        display: flex;
        flex-direction: column;

        .name {
            @include text(s16);

            margin-bottom: 1.2rem;
        }

        .content {
            @include text(m16);

            display: flex;
            flex-direction: column;
            color: $base-500;

            @include respond-to(mobile) {
                @include text(m14);
            }
        }

        .item {
            margin-bottom: .8rem;

            @include respond-to(mobile) {
                margin-bottom: .4rem;
            }

            &:last-child {
                margin-bottom: 0;
            }
        }
    }
</style>

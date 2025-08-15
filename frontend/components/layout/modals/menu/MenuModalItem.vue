<template>
    <div
        v-if="item"
        :class="$style.MenuModalItem"
        @click="onClick"
    >
        <span :class="$style.label">{{ item.label }}</span>

        <VIcon
            :class="$style.icon"
            name="arrow-right"
            size="medium"
        />
    </div>
</template>

<script>
// Components
import VIcon from '~/components/ui/icon/VIcon.vue';

export default {
    name: 'MenuModalItem',
    components: { VIcon },

    props: {
        item: {
            type: Object,
            default: null,
        },
    },

    methods: {
        onClick() {
            this.$emit('click', this.item);
        },
    },
};
</script>

<style lang="scss" module>
    .MenuModalItem {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1.2rem;
        color: $base-700;

        .label {
            @include text(m16);
        }
    }
</style>

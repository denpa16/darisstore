<template>
    <div :class="$style.MenuModal">
        <div :class="$style.wrapper">
            <VScrollBox :class="$style.scrollbox" resizable>
                <div :class="$style.items">
                    <MenuModalItem
                        v-for="item in items"
                        :key="item.value"
                        :class="$style.item"
                        :item="item"
                        @click="onClick"
                    />
                </div>
            </VScrollBox>

            <div :class="$style.buttons">
                <VIconButton
                    :class="$style.button"
                    icon="telegram"
                    size="medium"
                    color="secondary"
                />

                <VIconButton
                    :class="$style.button"
                    icon="whatsapp"
                    size="medium"
                    color="secondary"
                />
            </div>
        </div>
    </div>
</template>

<script>
// Components
import MenuModalItem from '~/components/layout/modals/menu/MenuModalItem.vue';

export default {
    name: 'MenuModal',

    components: {
        MenuModalItem,
    },

    props: {
        items: {
            type: Array,
            default: () => [],
        },
    },

    methods: {
        onClose() {
            this.$emit('close');
        },

        onClick(slug) {
            this.$emit('change', slug);
            this.onClose();
        },
    },
};
</script>

<style lang="scss" module>
    .MenuModal {
        height: 100%;
        padding: 2.4rem 1.6rem;
        background: $base-150;

        .wrapper {
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .scrollbox {
            flex: 1;
            margin-right: -1.6rem;
        }

        .items {
            padding-right: 1.6rem;
        }

        .item {
            margin-bottom: 2.4rem;

            &:last-child {
                margin-bottom: 0;
            }
        }

        .logo {
            width: 8rem;
            height: 8rem;
            margin: 4.95rem auto;
        }

        .buttons {
            display: flex;
            justify-content: center;
            gap: .8rem;
            width: 100%;
        }
    }
</style>

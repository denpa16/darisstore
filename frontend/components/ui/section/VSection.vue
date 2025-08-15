<template>
    <section :class="[$style.VSection, 'container']">
        <div :class="$style.titleHeader">
            <h2 :class="$style.title">{{ title }}</h2>

            <slot name="title-aside"></slot>
        </div>

        <slot></slot>
    </section>
</template>

<script>
export default {
    name: 'VSection',

    props: {
        title: {
            type: String,
            default: '',
        },
    },
};
</script>

<style lang="scss" module>
    .VSection {
        padding-top: 6.4rem;
        padding-bottom: 6.4rem;

        @include respond-to(mobile) {
            padding-top: 3.2rem;
            padding-bottom: 3.2rem;
        }

        .titleHeader {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 4rem;

            @include respond-to(mobile) {
                margin-bottom: 3.2rem;
            }
        }

        .title {
            @include text(h3);

            text-transform: uppercase;

            @include respond-to(mobile) {
                @include text(h4);
            }
        }
    }
</style>

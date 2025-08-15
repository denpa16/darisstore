<template>
    <div :class="[$style.VImageSrcSet, {[$style._contain]: contain}]">
        <img
            v-lazy="handleLazyLoaded"
            :alt="alt"
            v-bind="handleImgAttrs()"
            class="lazy"
        />
    </div>
</template>

<script>
/**
 * Позволяет отображать изображения, используя ImgProxy и двухэтапную загрузку (twoSteps).
 * Компонент, предназначен для изображений зависящих от адаптива
 * Если изображения НЕ зависят от адаптива, то следует использовать VImage
 *
 * @version 1.0
 * @displayName VImageSrcSet
 */
export default {
    name: 'VImageSrcSet',

    props: {
        image: {
            type: String,
            required: true,
        },

        alt: {
            type: String,
            default: 'image',
        },

        sizes: {
            type: String,
            default: 'mobile:100vw tablet:100vw laptop:100vw desktop:100vw',
        },

        modifiers: {
            type: Object,
            default: () => ({}),
        },

        previewW: {
            type: Number,
            default: 400,
        },

        previewH: {
            type: Number,
            default: 0,
        },

        previewQB: {
            type: Array,
            default: () => [20, 30],
            validator: arr => arr.length === 2 && arr.every(item => isFinite(item) && item > 10),
        },

        contain: Boolean,

        twoSteps: Boolean,

        prePreview: {
            type: String,
            default: 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        },
    },

    computed: {
        sizeOptions() {
            const options = {
                sizes: this.sizes,
                modifiers: { ...this.modifiers },
            };

            return this.$img.getSizes(this.image, options);
        },

        previewImg() {
            const options = {
                width: this.previewW,
                height: this.previewH,
                quality: this.previewQB[0],
                blur: this.previewQB[1],
            };

            return this.$img(this.image, options);
        },
    },

    methods: {
        handleImgAttrs() {
            const propsAttrs = {};

            if (this.twoSteps) {
                propsAttrs['data-src'] = this.previewImg;
                propsAttrs['data-lazy-sizes'] = this.sizeOptions.sizes;
                propsAttrs['data-lazy-srcset'] = this.sizeOptions.srcset;
            } else {
                propsAttrs['data-sizes'] = this.sizeOptions.sizes;
                propsAttrs['data-srcset'] = this.sizeOptions.srcset;
            }

            return { src: this.twoSteps ? this.prePreview : this.previewImg, ...propsAttrs };
        },

        handleLazyLoaded(el) {
            this.$emit('load', el);
        },
    },
};
</script>

<style lang="scss" module>
    .VImageSrcSet {
        img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        &._contain img {
            object-fit: contain;
        }
    }
</style>

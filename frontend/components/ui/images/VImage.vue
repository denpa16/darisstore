<template>
    <div :class="[$style.VImage, {[$style._contain]: contain}]">
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
 * Компонент, предназначен для изображений, НЕ СИЛЬНО зависящих от адаптива
 * Если изображения ЗАВИСЯТ от адаптива, то следует использовать VImageSrcSet
 *
 * @version 1.0
 * @displayName VImage
 */
export default {
    name: 'VImage',

    props: {
        image: {
            type: String,
            required: true,
        },

        alt: {
            type: String,
            default: 'image',
        },

        width: {
            type: Number,
            default: 0,
        },

        height: {
            type: Number,
            default: 0,
        },

        quality: {
            type: Number,
            default: 80,
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
        previewImg() {
            const options = {
                width: this.previewW,
                height: this.previewH,
                quality: this.previewQB[0],
                blur: this.previewQB[1],
            };

            return this.$img(this.image, options);
        },

        img() {
            const options = {
                width: this.width,
                height: this.height,
                quality: this.quality,
                ...this.modifiers,
            };

            return this.$img(this.image, options);
        },
    },

    methods: {
        handleImgAttrs() {
            const propsAttrs = {};

            if (this.twoSteps) {
                propsAttrs['data-src'] = this.previewImg;
                propsAttrs['data-lazy-src'] = this.img;
            } else {
                propsAttrs['data-src'] = this.img;
            }

            return { src: this.twoSteps ? this.prePreview : this.previewImg, ...propsAttrs };
        },

        handleLazyLoaded(el) {
            this.$emit('load', el);
            if (this.$config.IS_DEV) {
                console.warn('loaded:', el);
            }
        },
    },
};
</script>

<style lang="scss" module>
    .VImage {
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

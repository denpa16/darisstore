import Vue from 'vue';

import ClickOutside from '~/directives/clickoutside';
import LazyLoad from '~/directives/vanilla-lazyload';
import Intersect from '~/directives/intersect';

Vue.directive('clickoutside', ClickOutside);
Vue.directive('lazy', LazyLoad);
Vue.directive('intersect', Intersect);

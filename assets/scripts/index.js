window.$ = window.jQuery = require('jquery')

require('bootstrap')
require('admin-lte')
require('icheck')

import { enableLiveView } from "./utils/live";

window.EmailHunter = (() => {
    $('.carousel').carousel()
    return {
        tools: {
            enableLiveView
        }
    }
})()
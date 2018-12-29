window.$ = window.jQuery = require('jquery')

require('bootstrap')
require('admin-lte')
require('icheck')

import { enableLiveView } from "./utils/live";

window.EmailHunter = (() => {
    return {
        tools: {
            enableLiveView
        }
    }
})()
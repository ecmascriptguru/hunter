import { sendRequest } from "./ajax";

/**
 * Function to enable live feature
 * @param {String} selector jQuery selector
 * @param {Number} interval interval in second
 */
export const enableLiveView = (
        selector = '#live-view-container',
        interval = 5
    ) => {
    const url = window.location.href

    return window.setInterval(() => {
        sendRequest(`${url}#`, 'GET', {}, (res) => {
            const $container = $(selector)
            $container.children().remove()
            $container.append($(res))
        })
    }, interval * 1000)
}
/**
 * Function to get cookie value
 * @param {String} name 
 */
export const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Function to send ajax request.
 * @param {string} url 
 * @param {string} method 
 * @param {JSON} params 
 * @param {Function} success 
 * @param {Function} failure 
 */
export const sendRequest = (url, method = 'GET', params = {}, success, failure) => {
    $.ajax({
        url: url,
        method: method,
        cache: false,
        data: params,
        success: (res) => {
            if (typeof success === 'function') success(res)
        },
        error: () => {
            if (typeof failure === 'function') failure()
        }
    })
}
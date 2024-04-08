/**
 * Caching of layouts of Dash pages.
 *
 * Interesting. Would need to look into this more before using it for anything serious,
 * but it seems straightforward enough.
 *
 * From: https://community.plotly.com/t/page-layout-caching/77237
 */
((window, undefined) => {
    const {fetch: originalFetch} = window;

    const EXCLUDED_PAGES = [];

    const stored_data = {};

    const CACHE = "PAGE_CACHE";

    function updateCache(request, response) {
        if (window.location.href.substr(0, 4).toLowerCase() == 'https' || window.location.href.includes('127.0.0.1')) {
            caches.open(CACHE).then(function (cache) {
                cache.put(request, response);
            });
        } else {
            stored_data[request] = response
        }
    }

    async function testCache(url, that, args, cache_loc = CACHE) {
        var cachedResponse;
        if (window.location.href.substr(0, 4).toLowerCase() == 'https' || window.location.href.includes('127.0.0.1')) {
            const cache = await caches.open(cache_loc)
            cachedResponse = await cache.match(url)
        } else {
            cachedResponse = stored_data[url]
        }

        // Return a cached response if we have one
        if (cachedResponse) {
            savedResponse = cachedResponse.clone()
            return savedResponse;
        }

        const result = originalFetch(that, args);

        result.then((response) => {
            if (response.ok) {
                updateCache(url, response.clone())
            }
        })
        return result
    }

    window.fetch = async (event, payload) => {
        var result;
        // store all pages
        if (event === '/_dash-update-component') {
            const data = payload.body
            if (data.includes('_pages_store')) {
                const loc = JSON.parse(data)['inputs'][0].value.toLowerCase()
                if (!EXCLUDED_PAGES.includes(loc)) {
                    result = await testCache(loc, event, payload)
                }
            }
        }

        if (!result) {
            result = originalFetch(event, payload)
        }

        return result
    }
})(window);

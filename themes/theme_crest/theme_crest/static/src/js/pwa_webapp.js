/** @odoo-module **/

if ('serviceWorker' in navigator) { 
    navigator.serviceWorker.register('/pwa/service_worker').then(res => {
        console.info('service worker registered : ', res)}
    ).catch(error => {
      console.log('ServiceWorker registration failed: ', error)
    });
} 
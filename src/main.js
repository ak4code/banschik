import { createApp } from 'vue'
import store from './store'

createApp({
    data() {
        return { count: 1 }
      },
      created() {
        // `this` points to the vm instance
        console.log('count is: ' + this.count) // => "count is: 1"
      }
}).use(store).mount('#app')

import {createApp} from 'vue'
import store from './store'
import Test from './components/Test'

createApp({
    data() {
        return {count: 1}
    },
    components: {
        Test
    },
    created() {
        // `this` points to the vm instance
        console.log('count is: ' + this.count) // => "count is: 1"
    }
}).use(store).mount('#b-app')

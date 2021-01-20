import {createApp} from 'vue'
import store from './store'
import Test from './components/Test'
import UIkit from 'uikit'
import '@/assets/styles/styles.scss'
import Icons from 'uikit/dist/js/uikit-icons'

UIkit.use(Icons)
window.UIkit = UIkit

createApp({
    components: {
        Test
    }
}).use(store).mount('#b-app')

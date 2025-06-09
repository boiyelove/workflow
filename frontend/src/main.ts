import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faHome, faUser, faUsers, faProjectDiagram, 
  faCalendarAlt, faChartLine, faCog, faSignOutAlt,
  faPlus, faEdit, faTrash, faCheck, faTimes,
  faArrowUp, faArrowDown, faSearch, faBell
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faHome, faUser, faUsers, faProjectDiagram, 
  faCalendarAlt, faChartLine, faCog, faSignOutAlt,
  faPlus, faEdit, faTrash, faCheck, faTimes,
  faArrowUp, faArrowDown, faSearch, faBell
)

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')

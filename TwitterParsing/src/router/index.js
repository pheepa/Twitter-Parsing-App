import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from "../views/Main.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import CheckText from "../components/CheckText.vue"
import Data from "../components/Data.vue"
import Writings from "../components/Writings.vue"
import Inquiries from "../components/Inquiries.vue"
import Accounts from "../components/Accounts.vue"


Vue.use(VueRouter)
  const routes = [
    {
        path:'/login',
        name: 'Login',
        component: Login
    },
    {
        path:'/register',
        name: 'Register',
        component: Register
    },
    {
        path:'/',
        name: 'Main',
        component: Main,
        children:[
          {
              path:'',
              component: CheckText
          },
          {
              path:'data/',
              component: Data,
              children:[
              {
                  path:'writings',
                  component: Writings
              },
              {
                  path:'accounts',
                  component: Accounts
              },
              {
                  path:'inquiries',
                  component: Inquiries
              },  
            ]
          },
        ]
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router

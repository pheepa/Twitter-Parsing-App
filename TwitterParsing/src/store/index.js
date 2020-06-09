import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersist from 'vuex-persist';
import router from '../router'
import axios from 'axios'
import moment from 'moment'
import swal from 'sweetalert'

Vue.use(Vuex)

const vuexLocalStorage = new VuexPersist({
    key: 'vuex', 
    storage: window.localStorage, 
})

var port ="http://84.201.133.212/apipy/"
port ="http://127.0.0.1:8000/apipy/"

export default new Vuex.Store({
    state: {
        writings:[],
        inquiries:[],
        accounts:[],
        byteImage:null,
    user :{
        id:null,
        token:null,
        name: null,
        email:null
    },
    tab:0
    },

    mutations: {
        setTab(state,newTab){
            state.tab = newTab;
        },
        setUser(state,newTab){
            state.user = newTab;
        },
        setWritings(state,newTab){
            state.writings = newTab;
        },
        setAccounts(state,newTab){
            state.accounts = newTab;
        },
        setInquiries(state,newTab){
            state.inquiries = newTab;
        },
        setImage(state,newTab){
            state.byteImage = newTab
        }
    },

    actions: {
        async ChartingAccount(state, form){ 
            const data={
                'name': form.name,
                'months':form.months}
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.post(port +'twitter/charting/account/',data,config).then(response =>{
                this.commit('setImage',response.data)
            }).catch(function(e){alert("Вам нужно авторизоваться");console.log(e)});     
        },

        async ChartingHashtag(state, form){ 
            const data={
                'title': form.name,
                'months':form.months}
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.post(port + 'twitter/charting/hashtag/',data,config).then(response =>{
                this.commit('setImage',response.data)
            }).catch(function(e){alert("Вам нужно авторизоваться");console.log(e)});     
        },

        async GetInquiries(){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.get(port + 'twitter/inquiry/all/',config).then(response =>{
                this.commit('setInquiries',response.data.reverse())
            }).catch(function(e){console.log(e)});
        },

        async DeleteInquiry(state,id){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.delete(port + 'twitter/inquiry/detail/'+ id + '/',config).then(() =>{
                this.dispatch('GetInquiries')
            }).catch(function(e){console.log(e)}); 
        },

        async AddInquiry(state, form){
            const data={
                'hashtag':form.hashtag,
                'number_tweets':+form.number_tweets,
                'from_date':moment(form.from_date).format('YYYY-MM-DD'),
                'until_date':moment(form.until_date).format('YYYY-MM-DD')
            }
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.post(port +'twitter/inquiry/create/',data,config).then(() =>{
                this.dispatch('GetInquiries')
            }).catch(function(e){alert("Вам нужно авторизоваться");console.log(e)});  
        },


        async AddAccount(state, form){ 
            const data={
                'name': form.name,
                'number_tweets':+form.limit
            }
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.post(port + 'twitter/account/create/',data,config).then(() =>{
                this.dispatch('GetAccounts')
            }).catch(function(e){alert("Вам нужно авторизоваться");console.log(e)});     
        },

        async GetAccounts(){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.get(port + 'twitter/account/all/',config).then(response =>{
                this.commit('setAccounts',response.data.reverse())  
            }).catch(function(e){console.log(e)});
        },

        async DeleteAccount(state,id){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.delete(port +'twitter/account/detail/'+ id + '/',config).then(() =>{
                this.dispatch('GetAccounts')
            }).catch(function(e){this.error = e;});  
        },

        async AddWriting(state,form){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            const data={
                'text':form.text,
                'title':form.name}
            await axios.post(port + 'twitter/writing/create/',data,config).then(() =>{
                this.dispatch('GetWritings')
            }).catch(function(e){alert("чо то случилось");console.log(e)});
        },

        async GetWritings(){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.get(port + 'twitter/writing/all/',config).then(response =>{
                this.commit('setWritings', response.data.reverse())    
            }).catch(function(e){console.log(e)});
        },

        async DeleteWriting(state,id){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            await axios.delete(port +'twitter/writing/detail/'+ id + '/',config).then(() =>{
                this.dispatch('GetWritings')
            }).catch(function(e){console.log(e)});   
        },

        async EditWriting(state,item){
            var config ={   headers:{Authorization :"Token "+ this.state.user.token}}
            const data={
                "id": item.id,
                "title": item.title,
                "text": item.text,
                'date': moment()}
            await axios.put(port +'twitter/writing/detail/'+ item.id + '/',data,config).then(()=>{
                this.dispatch('GetWritings')
            }).catch(function(e){ console.log(e)});    
        },

        async SignUp(state,form){
            const data={
                'email':form.email,
                'username': form.name,
                'password': form.password};
            await axios.post(port + 'twitter/user/create/',data).then(() =>{
                this.dispatch('LogIn',form)
            }).catch(function(e){
                swal({
                    icon: 'error',
                    title: 'Error',
                    text: 'This name is already in use',
                })
            console.log(e)});
        },

        async LogIn(state,form){
            const data={
                'username': form.name,
                'password': form.password};
            await axios.post(port + 'twitter/login/',data).then(response =>{
                this.commit('setUser',{id:response.data.id_user , name:response.data.username, token: response.data.token, email: response.data.email})
                router.push("/")
            }).catch(function(e){
              swal("Error", "Incorrect data", "error");
              console.log(e)
            });
        },

        async LogOut(){
            this.commit('setUser',{id:null , name:null, token: null, email: null})  
        },

        Change(state,t){
            if(t==0|| t==null){
                if(router.history.current.path !="/data/inquiries"){
                    this.commit("setTab",0)
                    router.push("/data/inquiries")
                }
            }
            else if (t==1){
                if(router.history.current.path !="/data/accounts"){
                    this.commit("setTab",1)
                    router.push("/data/accounts")
                }        
            }
            else{
                if(router.history.current.path !="/data/writings"){
                    this.commit("setTab",2)
                    router.push("/data/writings")
              }        
            }
        },
    },

    plugins: [vuexLocalStorage.plugin]
})
   


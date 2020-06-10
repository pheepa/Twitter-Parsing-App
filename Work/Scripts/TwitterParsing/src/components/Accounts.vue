<template>
  <v-data-table
    :headers="headers"
    :items="this.$store.state.accounts"
    :fixed-header="true"
    sort-by="!id"
    class="elevation-0"
    height="480px"
    :items-per-page="9"
    show-expand
  >

   <template  v-slot:expanded-item="{ headers, item }" >
      <td   :colspan="headers.length">
          <div class="pl-2 pr-2 pt-2 font-weight-bold ">
                <span class="mr-2">{{item.Atweets.length}} tweets </span>
                <hr class="mb-0" v-if="item.number_tweets!=0">
          </div>
           <v-list two-line subheader>
              <v-list-item
              class="px-2"
                v-for="(tweet,i) in item.Atweets"
                :key="i"
              >
                <v-list-item-content class="m-0" >
                    <div class="m-1 p-2" :style="tweet.negative==false?'background-color:rgba(244,67,54,0.2)':'background-color:rgba(76,175,80,0.2)'"  style="font-size:16px">
                        <span class="mr-1 "> {{i+1}}.</span>
                        <span> {{tweet.text}}</span>
                    </div>
                </v-list-item-content>
              </v-list-item>
            </v-list>
       </td>
    </template>

    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:item.negative="{ item }">
      <v-chip v-if="item.negative>0" :color="getColor(item.negative)" dark>{{  item.negative}}%</v-chip>
      <v-chip v-if="item.negative<0" color="blue-grey darken-1" dark>
        Not found
      </v-chip>
    </template>

     <template v-slot:item.dates="{ item }">
      <div>{{ getDate(item) }}</div>
     </template>
  </v-data-table>
</template>


<script>
import swal from 'sweetalert'
import moment from 'moment'

  export default {
    data: () => ({
      dialog: false,
      headers: [
        { text: 'Name', align: 'start', value: 'name', },
        { text: 'Value tweets', value: 'number_tweets' },
        { text: 'Result', value: 'negative' },
        { text: 'Action', value: 'actions', sortable: false },
        { text: '', value: 'data-table-expand' },
      ],
      desserts: [],
    }),

    watch: {
      dialog (val) {
        val || this.close()
      },
    },

    created () {
      this.initialize()
    },

    methods: {
      getDate(item){
         return moment(item.from_date).format('l') +" ~ " +  moment(item.until_date).format('l')
      },
         getColor (calories) {
        if (calories <50) return 'red'
        else return 'green'
      },

      initialize () {
          this.$store.dispatch('GetAccounts')
      },

    
      deleteItem (item) {
        swal({
          title: "Are you sure?",
          text: "Once deleted, you will not be able to recover this record !",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
        .then((willDelete) => {
          if (willDelete) {
              this.$store.dispatch('DeleteAccount',item.id)
               swal("Poof! Your record has been deleted!", {
                    icon: "success",
            });
          } else {
            swal("Your record is safe!");
          }
        });
      },

    },
  }
</script>
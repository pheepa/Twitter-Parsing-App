<template>
    <v-data-table
        :headers="headers"
        :items="this.$store.state.writings"
        :fixed-header="true"
        height="480px"
        :items-per-page="9"
        sort-by="calories"
        class="elevation-0"
        :single-expand="singleExpand"
        :expanded.sync="expanded"
        show-expand
    >
        <template v-slot:top>
            <v-toolbar  height="0px" color="white">
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                    <v-card>
                        <v-card-text>
                            <v-container>
                                <v-row >
                                    <v-col cols="12">
                                        <v-text-field v-model="editedItem.title" label="Title "></v-text-field>
                                    </v-col>
                                    <v-col cols="12" >
                                        <v-textarea
                                            outlined
                                            name="input-7-1"
                                            label="Text"
                                            v-model="editedItem.text"
                                            hint="Hint text"
                                        ></v-textarea>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                            <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-toolbar>
        </template>

        <template v-slot:item.negative="{ item }">
            <v-chip :color="getColor(item.negative)" dark>{{ item.negative==true? 'positive':'negative' }}</v-chip>
        </template>

        <template v-slot:item.date="{ item }">
            <div  dark>{{ getDate(item.date) }}</div>
        </template>

        <template  v-slot:expanded-item="{ headers, item }">
            <td  :colspan="headers.length">
                <div class="m-1" style="width:90%;position:relative">
                    <v-tooltip  bottom>
                        <template v-slot:activator="{ on }">
                            <v-icon @click="DownloadWriting(item)" style="position:absolute;right:-50px" color="green" dark v-on="on">mdi-file-download-outline</v-icon>
                        </template>
                        <span>Download .txt</span>
                    </v-tooltip>
                    {{ item.text }}
                </div>    
            </td>
        </template>

        <template v-slot:item.actions="{ item }">
            <v-icon
                small
                class="mr-2"
                @click="editItem(item)"
            >mdi-pencil
            </v-icon>
            <v-icon
                small
                @click="deleteItem(item)"
            >mdi-delete
            </v-icon>
        </template>

        <template v-slot:no-data></template>
    </v-data-table>
</template>




<script>
import swal from 'sweetalert'
import moment from 'moment'

export default {
    data: () => ({
        expanded: [],
        singleExpand: false,
        dialog: false,
        headers: [
            {text: 'Title',align: 'start',value: 'title'},
            { text: 'Date', value: 'date', sortable: false },
            { text: 'Result', value: 'negative' },
            { text: 'Actions', value: 'actions', sortable: false },
            { text: '', value: 'data-table-expand' },
        ],
        editedIndex: -1,
        editedItem: {
            title: '',
            text: '',
        },
    }),

    computed: {
        formTitle () {
            return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
        },
    },

    watch: {
        dialog (val) {
            val || this.close()
        },
    },

    created () {
        this.initialize()
    },

    methods: {
        getDate(date){
            return moment(date).format("l")
        },

        getColor (calories) {
            if (calories ==false) return 'red'
            else return 'green'
        },

        initialize () {
            this.$store.dispatch('GetWritings')
        },

        editItem (item) {
            this.editedIndex = this.$store.state.writings.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },

        async  deleteItem (item) {
            swal({
                title: "Are you sure?",
                text: "Once deleted, you will not be able to recover this record !",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    this.$store.dispatch('DeleteWriting',item.id)
                    swal("Poof! Your record has been deleted!", {
                        icon: "success",
                    });
                } else {
                    swal("Your record is safe!");
                }
            });
        },

        close () {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem)
                this.editedIndex = -1
            })
        },

        save () {
            if (this.editedIndex > -1) {
                this.$store.dispatch('EditWriting',this.editedItem)
            } 
            this.close()
        },

        DownloadWriting(item){
            let format
            format ="txt"
            const text = item.text
            const element = document.createElement('a');
            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + text);
            element.setAttribute('download', item.title+'.'+format);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        },
    },
}
</script>
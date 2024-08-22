function init() {
    return {
        listOfArticles: [],
        editable: false,
        selectedArticle: {"title":"", "link":"https://"},

        async loadList() {
            console.log('Loading List');
            this.listOfArticles= await (await fetch('/api/listAll')).json();
            console.log(this.listOfArticles);
            this.editable = false;
        },

        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms))
        },
          

        async saveArticle() {
            console.log('Saving Article');
            
                var _id = this.selectedArticle._id.$oid;
                delete this.selectedArticle._id;

                console.log(this.selectedArticle);
                await fetch('/api/save/'+_id, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.selectedArticle)
                });
                this.editable = false;
                await this.loadList();
        },

        async newArticle() {
            console.log('New Stream');
            editable = false;
            this.selectedArticle = await (await fetch('/api/new')).json();
            this.editable = true;
        },

    }
}
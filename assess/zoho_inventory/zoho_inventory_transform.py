import os, json, time
from store.sdk.inv.inv_wrapper import inv_document
from django.apps import apps
from uuid import uuid4

get_model = apps.get_model

#print(os.path.join(os.getcwd(), "sales_mania", "pickel"))


class zit(inv_document):

    def __init__(self, login_store, cache_store, user_id,
                 password, data_center, org_id, docs_sync,
                 docs_segment) -> None:
        
        """
            docs which have to be synced 
        """
        
        self.cache_store = cache_store
        self.docs_sync = docs_sync
        self.org_id = org_id
        self.docs_segment = docs_segment
        
        super().__init__(login_store, cache_store, user_id, password, data_center, org_id)



    def count_rounds(self, fetch_count, segment, start):

        #determing start

        if start <= segment:

            start_page = 1

        else:
            
            start_page = int(start/segment) + 1


        #determining end

        if fetch_count <= segment:

            end_index = 1

        else:

            end_count = (start + fetch_count)/segment
            end_round = round(end_count)
            end_index = end_round + 1 if end_count > end_round else end_round

        
        #since range works till [index} so

        end_page = end_index + 1


         

        return start_page, end_page


    def transform_items(self, uuid, start, end):

        
        for round in range(start, end):
            
            file_path = os.path.join(self.cache_store, f"items_{round}_{uuid}.json")

            with open(file_path, "r") as f:

                items_data = json.load(f)


                #transform_logic

                #load logic

            os.remove(file_path)
                




    def fetch_docs(self, document_ids = {}):

        pass


    def sync_masters(self):

        for doc in self.docs_sync:

            row_count = self.get_document_count(doc)
            segment = self.docs_segment.get(doc, 200)

            start, end = self.count_rounds(fetch_count=row_count,
                                           segment=segment,
                                           start=1)
            

            file_prefix = str(uuid4())

            for round in range(start, end):
                
                item_data = self.get_document_page_n(document=doc, segment=segment, round=round)

                with open(os.path.join(self.cache_store, f"{doc}_{round}_{file_prefix}.json"), "w+") as f:

                    json.dump(item_data, f)

            
            time.sleep(0.5)


                
            



    def sync_beacon(self, beacon):

        pass



    


    def select_sync_action(self):

        sync_beacon = self.find_sync()
        
        if sync_beacon is False:
            
            self.sync_masters()

        else:

            self.sync_incremental(sync_beacon)





    def find_sync(self):

        sync_stamp = False
        zi_sync_master = get_model("zoho_inventory", "zi_sync_master")
        stamp = zi_sync_master.objects.filter(zi_org=self.org_id)
        
        if stamp.exists():

            sync_stamp = stamp[0]

            
        return sync_stamp




t_data = zit(login_store = os.path.join(os.getcwd(), "stores", "pickel"),
                        cache_store = os.path.join(os.getcwd(), "stores", "cache"),
                        user_id = "it.kvtek@outlook.com", password = "IT4kvtek",
                        data_center = ".in", org_id = "60008720898", docs_sync=["items"], docs_segment={"items":10})
t_data.sync_masters()

""" 
document = inv_document(login_store = os.path.join(os.getcwd(), "stores", "pickel"),
                        cache_store = os.path.join(os.getcwd(), "stores", "cache"),
                        user_id = "it.kvtek@outlook.com", password = "IT4kvtek",
                        data_center = ".in", org_id = "60008720898")

 """
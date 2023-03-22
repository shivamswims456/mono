from django.db import models
from django.conf import settings
import copy

def safe_save(cls, **kwargs):

    slaves = settings.REPLICATED_DATABASE_SLAVES
    result = __os(cls, **kwargs)

    if 'Migration' not in str(cls):
        
        if kwargs['using'] not in slaves:
            #migrate --database error save

            kls = copy.deepcopy(cls) 

            for slave in slaves:

                kwargs['using'] = slave
                __os(kls, **kwargs)

        


        
    return result

def safe_dels(cls, **kwargs):
    
    oldId = getattr(cls, "id", False)
    result = __od(cls, **kwargs)

    if oldId is not False:
        
        slaves = settings.REPLICATED_DATABASE_SLAVES
        
        if kwargs.get('using', True):
            #migrate --database error save
            
            for slave in slaves:
                cls.id = oldId    
                kwargs['using'] = slave
                __od(cls, **kwargs)

    return result

def safe_q_delete(args, **kwargs):
    
    slaves = settings.REPLICATED_DATABASE_SLAVES
    for slave in slaves:
        kls = copy.deepcopy(args)
        kls._db = slave
        __md(kls, **kwargs)

    result = __md(args, **kwargs)

    return result

__od = models.Model.delete 
__os = models.Model.save_base
__md = models.query.QuerySet.delete   
models.Model.save_base = safe_save
models.Model.delete = safe_dels
models.query.QuerySet.delete = safe_q_delete
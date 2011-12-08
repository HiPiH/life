def cp_config(req):
    from apps.config import aggregator
    return {"cp_config":aggregator}
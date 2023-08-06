import orb
from orb import Query as Q

def collect_params(request):
    try:
        return dict(request.json_body)
    except ValueError:
        return dict(request.params)

def collect_query_info(model, request):
    """
    Processes the inputed request object for search terms and parameters.

    :param      request | <pyramid.request.Request>

    :return     (<orb.LookupOptions>, <orb.DatabaseOptions>, <str> search terms, <dict> orignal options)
    """
    params = collect_params(request)

    # generate a simple query object
    q_build = {col: params[col] for col in params if model.schema().column(col)}
    if q_build:
        params['where'] = Q.build(q_build)

    # create the lookup information
    params.setdefault('inflated', False)

    if 'columns' in params:
        params['columns'] = params['columns'].split(',')

    terms = params.pop('terms', '')
    db_options = orb.DatabaseOptions(**params)
    lookup = orb.LookupOptions(**params)

    # returns the lookup, database options, search terms and original options
    return {'lookup': lookup, 'options': db_options, 'terms': terms}
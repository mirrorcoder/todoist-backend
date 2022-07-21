def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def calc_pages(model, page, count_per_page):
    count_pages = int(model.query.count()/count_per_page) + (1 if model.query.count() % count_per_page else 0)
    pages = {
        'start': None,
        'next': None,
        'prev': None,
        'last': None
    }
    if count_pages > 1:
        if page > 0:
            pages['start'] = 1
            pages['prev'] = page
        if page < (count_pages-1):
            pages['next'] = page + 2
            pages['last'] = count_pages
    return pages
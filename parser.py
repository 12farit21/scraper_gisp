def parse_product(product_json):
    """Extract required fields from product JSON response"""
    return {
        'id': product_json.get('id'),
        'company_id': product_json.get('company', {}).get('id'),
        'name': product_json.get('name'),
        'createdAt_gisp': product_json.get('createdAt'),
        'updatedAt_gisp': product_json.get('updatedAt')
    }

def parse_company(product_json):
    """Extract company fields from product JSON response"""
    company = product_json.get('company', {})
    return {
        'id': company.get('id'),
        'catalogId': company.get('catalogId'),
        'gispId': company.get('gispId'),
        'name': company.get('name'),
        'inn': company.get('inn'),
        'ogrn': company.get('ogrn'),
        'regionId': company.get('regionId'),
        'contactFio': company.get('contactFio')
    }

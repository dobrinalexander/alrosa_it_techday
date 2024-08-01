

def prepare_data_to_insert(raw_data: dict) -> dict:
    max_cursor = "1337"
    out_data = {
        'id': []
        ,'ticker': []
        ,'columns_insert': ['id', 'ticker', 'inserted'
            ,'price', 'nickname' ,'likesCount'
            ,'content', 'max_cursor'] # for insert columns list tech field
        ,'values_insert': [] # all json text tech filed
    }

    id = raw_data.get('id')
    ticker = raw_data.get('instruments')[0].get('ticker')
    inserted = raw_data.get('inserted')
    price = raw_data.get('instruments')[0].get('price')
    nickname = raw_data.get('nickname')
    likesCount = raw_data.get('likesCount')
    # reactions = i.get('instruments')[0].get('reactions')
    content = raw_data.get('content').get('text')
    out_data['id'].append(id)
    out_data['ticker'].append(ticker)
    out_data['values_insert'].append((
        id, ticker, inserted
        ,price, nickname ,likesCount
        ,content, max_cursor))
    
    return out_data
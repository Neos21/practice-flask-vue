from decimal import Decimal, getcontext, ROUND_HALF_UP

from flask import Blueprint, request
from flask_restful import Api, Resource
import pybitflyer  # http://wolfin.hatenablog.com/entry/2016/08/29/010112

# BitFlyer API を用意する
bit_flyer_api = pybitflyer.API()

# Blueprint を作成する
blueprint_api = Blueprint('api', __name__, url_prefix = '/api')
api = Api(blueprint_api)

# レート
class Rate(Resource):
  def get(self, code):
    try:
      if(code == 'btc'):
        return { 'code': code, 'bid': str(bit_flyer_api.ticker(product_code = 'BTC_JPY')['best_bid']) }   # https://futurismo.biz/archives/6401
      if(code == 'eth'):
        return { 'code': code, 'bid': str(bit_flyer_api.ticker(product_code = 'ETH_JPY')['best_bid']) }
      
      # https://inokara.hateblo.jp/entry/2016/10/01/123923 https://qiita.com/mink0212/items/52e0ebd66bd94e1303c1 https://stackoverflow.com/questions/44430906/flask-api-typeerror-object-of-type-response-is-not-json-serializable
      return { 'message': 'Unknown code' }, 403  # Flask API の場合は直接レスポンスして良い
    except:
      return { 'message': 'Failed to get board' }, 500
api.add_resource(Rate, '/rate/<string:code>')  # https://kazuhira-r.hatenablog.com/entry/2019/08/14/235805

# 計算
@blueprint_api.route('/calculator', methods = ['POST'])
def calculator():
  # リクエストの連想配列 : ex. { btc: '0.1', eth: '0.5' }
  data = request.get_json()
  if(not data):
    return { 'message': 'Invalid request' }, 403
  
  # Decimal の有効桁数を10桁にする
  getcontext().prec = 10
  # Decimal の丸め方を四捨五入にする
  getcontext().rounding = ROUND_HALF_UP
  # 結果オブジェクト
  response = {}
  
  # 資産額を Decimal で取得する・Decimal に変換できない場合は None となる
  def get_balance(balance):
    try:
      return Decimal(balance)
    except:
      return None
  
  # レートを取得する
  def get_rate(code):
    bid = None
    
    try:
      if(code == 'btc'):
        bid = bit_flyer_api.ticker(product_code = 'BTC_JPY')['best_bid']
      elif(code == 'eth'):
        bid = bit_flyer_api.ticker(product_code = 'ETH_JPY')['best_bid']
    except:
      pass  # 何もしない
    
    if(bid is None):
      return None
    
    return Decimal(bid)
  
  # Decimal を計算し結果を文字列型で返す
  def calc(decimal_balance, decimal_rate):
    decimal_result = decimal_balance * decimal_rate
    return str(decimal_result)
  
  # 取得データごとに処理する
  for code, balance in data.items():
    # 資産額
    decimal_balance = get_balance(balance)
    if(decimal_balance is None):
      print(code, 'Invalid balance, response is Zero')
      response[code + '_jpy'] = '0'
      continue
    
    # レートを取得する
    decimal_rate = get_rate(code)
    if(decimal_rate is None):
      print(code, 'Cannot get ticker, response is Zero')
      response[code + '_jpy'] = '0'
      continue
    
    # 計算する
    result = calc(decimal_balance, decimal_rate)
    print(code, result)
    response[code + '_jpy'] = result
  
  # 合計額を算出・追加する
  total_jpy_balance = Decimal('0')
  for jpy_balance in response.values():
    total_jpy_balance += Decimal(jpy_balance)
  response['total_jpy'] = str(total_jpy_balance)
  print('Total JPY', response.get('total_jpy'))
  
  # ex. { 'btc_jpy': '10000.1', 'eth_jpy': '200.1', 'total_jpy': '10200.2' }
  return response

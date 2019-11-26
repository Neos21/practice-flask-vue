from decimal import Decimal, getcontext, ROUND_HALF_UP

from flask import Blueprint, request
from flask_restful import Api, Resource

# Blueprint を作成する
blueprint_api = Blueprint('api', __name__, url_prefix = '/api')
api = Api(blueprint_api)

# レート情報
# TODO : 何らかの API 経由で最新の値を取得したい
rates = [
  { 'market_code': 'btc_jpy', 'price': '789313.67' },  # 1 BTC = 789,313.67 JPY
  { 'market_code': 'eth_jpy', 'price':  '16207.43' }   # 1 ETH =  16,207.43 JPY
]

# 資産
class Balance(Resource):
  # TODO : DB とかに保存する (面倒ならファイルでも良い気がする)
  # TODO : PUT で資産を更新できるようにしたい
  def get(self):
    return {
      'btc': '0.00313149',
      'eth': '0.0299'
    }
api.add_resource(Balance, '/balance')

# レート
class Board(Resource):
  def get(self):
    return rates
api.add_resource(Board  , '/board')

# 計算
@blueprint_api.route('/calculator', methods = ['POST'])
def calculator():
  data = request.get_json()
  result = {}
  
  # Decimal の有効桁数を10桁にする
  getcontext().prec = 10
  # Decimal の丸め方を四捨五入にする
  getcontext().rounding = ROUND_HALF_UP
  
  # 資産額を取得する
  def getDecimalBalance(balance):
    return Decimal(balance)
  
  # レート情報から価格を取得する
  def getDecimalPrice(currencyCode):
    rateInfo = next((item for item in rates if item['market_code'] == currencyCode + '_jpy'), None)
    if(rateInfo is None): return None
    rawPrice = rateInfo.get('price')
    if(rawPrice is None): return None
    return Decimal(rawPrice)
  
  # 計算する
  def calc(decimalBalance, decimalPrice):
    decimalResult = decimalBalance * decimalPrice
    return str(decimalResult)
  
  # 取得データごとに処理する
  # TODO : 小数以下の桁数を揃えたい
  for currencyCode, balance in data.items():
    # 入力値がなければ計算結果は 0 とする
    if not balance:
      print(currencyCode, 'Input is null or empty, result is Zero')
      result[currencyCode + '_jpy'] = '0'
      continue
    
    decimalBalance = getDecimalBalance(balance)
    decimalPrice = getDecimalPrice(currencyCode)
    if not decimalPrice:
      print(currencyCode, 'Cannot get price data, result is Zero')
      result[currencyCode + '_jpy'] = '0'
      continue
    
    strResult = calc(decimalBalance, decimalPrice)
    print(currencyCode, strResult)
    result[currencyCode + '_jpy'] = strResult
  
  # 合計額を算出・追加する
  decimalJpyBalance = Decimal('0')
  for jpyBalance in result.values():
    decimalJpyBalance += Decimal(jpyBalance)
  result['total_jpy'] = str(decimalJpyBalance)
  print('Total', result.get('total_kpy'))
  
  return result
